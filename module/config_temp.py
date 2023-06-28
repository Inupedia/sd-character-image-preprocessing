IMAGE_CONFIG = {
    "REMBG_MODEL": "u2net",
    "IMAGE_PREFIX": "illust",
    "CROP_INPUT_DIR": "./src/rm_bg_output/",
    "CROP_OUTPUT_DIR": "./src/crop_output/",
    "SMARTCROP_INPUT_DIR": "./src/rm_bg_output/",
    "SMARTCROP_OUTPUT_DIR": "./src/smartcrop_output/",
    "KEYWORD_ORDER": True,  # True: popular / False: latest
    "KEYWORD_N_PAGES": 5,  # 1 page = 60 images
    "KEYWORD_MODE": "safe",  # safe / r18 / all
    "IMAGE_RESIZE_DIR": "./src/input/",
    "MODEL_TYPE": 0,
    "IMAGE_SCALE": 4,
}

OUTPUT_CONFIG = {
    # verbose / simplified output
    "VERBOSE": False,
    "PRINT_ERROR": False,
}

NETWORK_CONFIG = {
    # proxy setting
    #   you should customize your proxy setting accordingly
    #   default is for clash
    "PROXY": {"https": "127.0.0.1:7890"},
    # common request header
    "HEADER": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    },
}

USER_CONFIG = {
    # user id
    #   access your pixiv user profile to find this
    #   e.g. https://www.pixiv.net/users/xxxx
    "USER_ID": "YOUR_USER_ID",
    "COOKIE": "YOUR_COOKIE",
}


DOWNLOAD_CONFIG = {
    # image save path
    #   NOTE: DO NOT miss "/"
    "STORE_PATH": "./src/input/",
    # abort request / download
    #   after 10 unsuccessful attempts
    "N_TIMES": 10,
    # waiting time (s) after failure
    "FAIL_DELAY": 1,
    # max parallel thread number
    "N_THREAD": 12,
    # waiting time (s) after thread start
    "THREAD_DELAY": 1,
}
