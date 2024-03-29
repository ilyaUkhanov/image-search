import json
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from shlex import join
import threading
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc

# Import all the Models before the DatabaseService, otherwise the relationships won't work
# @ref https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.Models.Picture import Picture
from app.Models.Tag import Tag

from app.Services.DatabaseService import DatabaseService
from app.Services.PictureService import PictureService
from app.Services.MessagingService import MessagingService
from app.Services.MQConsumer import ReconnectingMQConsumer

app = FastAPI()

# Configuring the CORS Middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.environ.get("FRONTEND_APP_ORIGIN")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start the RabbitMQ listener in a separate Thread
def start_mq_consumer():
    amqp_url = 'amqp://guest:guest@localhost:5672/%2F'
    consumer = ReconnectingMQConsumer(amqp_url)
    consumer.run(MessagingService.on_picture_annotation)

# MessagingService.consume_message
threading.Thread(target=start_mq_consumer, daemon=True).start()

# A mount that serves the uploaded pictures to the frontend
Path(PictureService.calculate_picture_folder()).mkdir(parents=True, exist_ok=True)
app.mount(
    os.environ.get("PICTURES_MOUNT_URL", "/pictures"),
    StaticFiles(directory=PictureService.calculate_picture_folder()), name="pictures"
)

@app.post("/api/pictures/upload/")
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

@app.get("/api/pictures/search/")
async def search_file(search = None, page=0, per_page=10):
    session = DatabaseService.session_factory()
    statement = session.query(Picture.filename).join(Tag, Picture.id == Tag.id, isouter=True)

    # Search by captions generated by the AI
    if search is not None:
        statement = statement.where( Picture.tags.any(Tag.name.contains(search)) )

    # Pagination of the query
    statement = statement.order_by(desc(Picture.creation_date)).limit(limit=per_page).offset(page*per_page)
    
    pictures = session.execute(statement).all()
    result = []
    for picture in pictures:
        relative_path = os.environ.get("PICTURES_MOUNT_URL", "/pictures") + "/" + picture[0]
        result.append(relative_path)
    
    session.close()

    # Do not serialize dates and other complex objects with this method
    return json.dumps(result)


@app.get("/")
def read_root():
    session = DatabaseService.session_factory()
    picture_query = session.query(Picture)
    session.close()
    return picture_query.all()