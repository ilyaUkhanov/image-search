from functools import partial
from pathlib import Path
import threading
from typing import Union
from app.Models.Picture import Picture
from fastapi import FastAPI, UploadFile

import sys

# Import all the Models before the DatabaseService, otherwise the relationships won't work
# @ref https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.Models.Picture import Picture
from app.Models.Tag import Tag

from app.Services.DatabaseService import DatabaseService
from app.Services.PictureService import PictureService
from app.Services.MessagingService import MessagingService

print(sys.path)

app = FastAPI()

# Start the RabbitMQ listener in a separate Thread
threading.Thread(target=MessagingService.consume_message, daemon=True).start()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    filepath = PictureService.calculate_picture_path(file.filename)

    PictureService.save_upload_file(file, filepath)

    picture = Picture(file.filename, filepath, [])        
    session = DatabaseService.session_factory()
    session.add(picture)
    session.commit()

    MessagingService.send_message(str(picture.id))
    session.close()

    return {"filename": file.filename}


@app.get("/")
def read_root():
    session = DatabaseService.session_factory()
    picture_query = session.query(Picture)
    session.close()
    return picture_query.all()