from pathlib import Path
import shutil
import os
import requests

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
    
    def generate_captions(pictureName, picturePath):
        files = {'image': (pictureName, open(picturePath,'rb'), 'image/jpeg')}
        response = requests.post(os.environ.get("IMAGE_CAPTIONS_PREDICTION_ROUTE", 
                                                "http://127.0.0.1:5000/model/predict"), 
                                                files=files)
        return response.json()