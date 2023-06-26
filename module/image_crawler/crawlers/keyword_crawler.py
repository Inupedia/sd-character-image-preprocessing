import concurrent.futures as futures
from typing import Set

from ..collector.collector import Collector
from ..collector.collector_unit import collect
from ..collector.selectors import selectKeyword
from ...config import DOWNLOAD_CONFIG, USER_CONFIG, IMAGE_CONFIG
from ..downloader.downloader import Downloader
from tqdm import tqdm
from ..utils import printInfo
import urllib.parse as urlparse


class KeywordCrawler:
    """[summary]
    download search results of a keyword
    """

    def __init__(
        self,
        keyword: str,
        capacity=1024,
    ):
        self.keyword = keyword
        self.order = IMAGE_CONFIG["KEYWORD_ORDER"]
        self.mode = IMAGE_CONFIG["KEYWORD_MODE"]
        self.n_page = IMAGE_CONFIG["KEYWORD_N_PAGES"]
        self.downloader = Downloader(capacity)
        self.collector = Collector(self.downloader)

    def collect(self):
        """[summary]
        collect illust_id from keyword result
        url sample: "https://www.pixiv.net/ajax/search/artworks/{xxxxx}?
            word={xxxxx}&order=popular_d&mode=all&p=1&s_mode=s_tag_full&type=all&lang=zh"
        """

        # NOTE: each keyword.json contains 60 artworks

        printInfo(f"===== start collecting {self.keyword} =====")

        urls: Set[str] = set()
        url = (
            "https://www.pixiv.net/ajax/search/artworks/"
            + "{}?word={}".format(
                urlparse.quote(self.keyword, safe="()"), urlparse.quote(self.keyword)
            )
            + "&order={}".format("popular_d" if self.order else "date_d")
            + f"&mode={self.mode}"
            + "&p={}&s_mode=s_tag&type=all&lang=zh"
        )
        for i in range(self.n_page):
            urls.add(url.format(i + 1))

        n_thread = DOWNLOAD_CONFIG["N_THREAD"]
        with futures.ThreadPoolExecutor(n_thread) as executor:
            with tqdm(total=len(urls), desc="collecting ids") as pbar:
                additional_headers = {"COOKIE": USER_CONFIG["COOKIE"]}
                for image_ids in executor.map(
                    collect,
                    zip(
                        urls,
                        [selectKeyword] * len(urls),
                        [additional_headers] * len(urls),
                    ),
                ):
                    if image_ids is not None:
                        self.collector.add(image_ids)
                    pbar.update()

        printInfo(f"===== collect {self.keyword} complete =====")
        printInfo(f"downloadable artworks: {len(self.collector.id_group)}")

    def run(self):
        self.collect()
        self.collector.collect()
        return self.downloader.download()
