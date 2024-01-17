from ast import Str
import os
from pathlib import Path
import shutil
import string
from fastapi import UploadFile

class PictureService:
    PICTURES_FOLDER_RELATIVE_PATH = os.environ.get('PICTURES_FOLDER_RELATIVE_PATH', 'pictures')

    def calculate_picture_folder():
        return os.path.join(os.environ.get('ROOT_DIR'), PictureService.PICTURES_FOLDER_RELATIVE_PATH)

    def calculate_picture_path(filename):
        return os.path.join(PictureService.calculate_picture_folder(), filename)

    def save_upload_file(upload_file: UploadFile, destination: str) -> None:
        # Creating a new picture folder if it doesn't exist
        Path(PictureService.calculate_picture_folder()).mkdir(parents=True, exist_ok=True)

        path = Path(destination)

        try:
            with path.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()