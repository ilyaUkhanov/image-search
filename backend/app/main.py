from functools import partial
import json
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from sqlalchemy  import select
from shlex import join
import threading
from typing import Union
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

# TODO : add date to pictures, so you can orderby pictures
@app.get("/searchfile/")
async def search_file(search = None, page=0, per_page=10):
    session = DatabaseService.session_factory()
    statement = session.query(Picture.filename).join(Tag, Picture.id == Tag.id, isouter=True)

    # Search by captions generated by the AI
    if search is not None:
        statement = statement.where( Picture.tags.any(Tag.name.contains("dog")) )

    # Pagination of the query
    statement = statement.limit(limit=per_page).offset(page*per_page)
    
    pictures = session.execute(statement).all()
    result = []
    for picture in pictures:
        relative_path = os.environ.get("PICTURES_MOUNT_URL", "/pictures") + "/" + picture[0]
        result.append(relative_path)
    
    session.close()

    # Do not serialize dates and other complex objects with this method
    return json.dumps(result)


# A mount that serves the uploaded pictures to the frontend
app.mount(
    os.environ.get("PICTURES_MOUNT_URL", "/pictures"),
    StaticFiles(directory="app/" + os.environ.get("PICTURES_FOLDER_RELATIVE_PATH", "pictures")), name="pictures"
)

@app.get("/")
def read_root():
    session = DatabaseService.session_factory()
    picture_query = session.query(Picture)
    session.close()
    return picture_query.all()