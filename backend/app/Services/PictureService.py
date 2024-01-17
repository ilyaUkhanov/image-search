import os

class PictureService:
    PICTURES_FOLDER_RELATIVE_PATH = os.environ.get('PICTURES_FOLDER_RELATIVE_PATH', 'pictures')

    def calculate_picture_path(filename):
        return os.path.join(os.environ.get('ROOT_DIR'), PictureService.PICTURES_FOLDER_RELATIVE_PATH, filename)