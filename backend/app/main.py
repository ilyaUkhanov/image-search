from typing import Union
from app.Models.Picture import Picture
from fastapi import FastAPI, UploadFile

# Import all the Models before the DatabaseService, otherwise the relationships won't work
# @ref https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.Models.Picture import Picture
from app.Models.Tag import Tag

from app.Services.DatabaseService import DatabaseService
from app.Services.PictureService import PictureService

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    filepath = PictureService.calculate_picture_path(file.filename)
    picture = Picture(file.filename, filepath, [])

    session = DatabaseService.session_factory()
    session.add(picture)
    session.commit()
    session.close()

    return {"filename": file.filename}


@app.get("/")
def read_root():
    return {"Hello": "World"}