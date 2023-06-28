import cv2
import os
from PIL import Image
from tqdm import tqdm
from ..config import IMAGE_CONFIG


class SmartCropper:
    def __init__(self, cascade_file="lbpcascade_animeface.xml"):
        cascade_path = os.path.join(os.path.dirname(__file__), cascade_file)
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def calculate_crop_coordinates(
        self, face_x, face_y, face_width, face_height, image_width, image_height
    ):
        face_center_x = face_x + face_width // 2
        face_center_y = face_y + face_height // 2
        distance = max(face_width, face_height)

        top = max(0, face_center_y - distance)
        bottom = min(image_height, face_center_y + distance)
        left = max(0, face_center_x - distance)
        right = min(image_width, face_center_x + distance)

        return left, top, right - left, bottom - top

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for idx, (x, y, w, h) in enumerate(faces):
            image_height, image_width = image.shape[:2]
            crop_x, crop_y, crop_width, crop_height = self.calculate_crop_coordinates(
                x, y, w, h, image_width, image_height
            )
            cropped = image[crop_y : crop_y + crop_height, crop_x : crop_x + crop_width]

            # Check if cropped image size is larger than 512x512
            if cropped.shape[0] > 512 or cropped.shape[1] > 512:
                # Resize the cropped image to 512x512
                resized = cv2.resize(cropped, (512, 512))
                filename, ext = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(
                    IMAGE_CONFIG["SMART_CROP_OUTPUT_DIR"],
                    f"{filename}_smart_crop_{idx}{ext}",
                )
                cv2.imwrite(output_path, resized)
            else:
                filename, ext = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(
                    IMAGE_CONFIG["SMART_CROP_OUTPUT_DIR"],
                    f"{filename}_smart_crop_{idx}{ext}",
                )
                cv2.imwrite(output_path, cropped)

    def load_all_images(self):
        self.image_files = []
        all_files = os.listdir(self.image_directory)
        for filename in all_files:
            try:
                Image.open(
                    os.path.join(self.image_directory, filename)
                )  # Try to open the file with PIL
                self.image_files.append(
                    filename
                )  # If it succeeds, add the filename to the list
            except IOError:
                pass  # If it fails, ignore the file

    def crop_and_save_all(self):
        self.image_directory = IMAGE_CONFIG["SMART_CROP_INPUT_DIR"]
        self.load_all_images()
        for filename in tqdm(self.image_files, desc="Processing images"):
            self.process_image(os.path.join(self.image_directory, filename))
