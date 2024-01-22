import os
import pika
from app.Models.Picture import Picture
from app.Models.Tag import Tag
from app.Services.DatabaseService import DatabaseService
from app.Services.PictureService import PictureService

# TODO make connection more solid - retry & reconnect
class MessagingService:
    EXCHANGE = "exchange_picture_annotation"
    ROUTING_KEY = "pipe_picture_annotation"

    def __connection_factory():
        params = pika.URLParameters(os.environ.get('MQ_CONNECTION_STRING', 'amqp://guest:guest@localhost:5672/%2F'))
        connection = pika.BlockingConnection(params)
        return connection

    def send_message(message):
        connection = MessagingService.__connection_factory()
        connection.channel().queue_declare(queue=MessagingService.ROUTING_KEY)
        connection.channel().basic_publish(exchange=MessagingService.EXCHANGE, routing_key=MessagingService.ROUTING_KEY, body=message)
        connection.close()

    def on_picture_annotation(delivery_tag, app_id, body):
        id = int(body)
        session = DatabaseService.session_factory()
        picture = session.get(Picture, id)

        if(picture is not None):
            captions = PictureService.generate_captions(picture.filename, picture.path)
            for prediction in captions['predictions']:
                caption = prediction["caption"]
                tag = Tag(caption)
                picture.tags.append(tag)

        session.commit()
        session.close()