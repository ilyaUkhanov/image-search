import os
import pika
from app.Models.Picture import Picture
from app.Services.DatabaseService import DatabaseService
from app.Services.PictureService import PictureService

class MessagingService:
    PIPE_NAME = "pipe_picture_annotation"

    def __connection_factory():
        params = pika.URLParameters(os.environ.get('MQ_CONNECTION_STRING', 'amqp://guest:guest@localhost:5672/%2F'))
        connection = pika.BlockingConnection(params)
        return connection

    def send_message(message):
        connection = MessagingService.__connection_factory()
        connection.channel().queue_declare(queue=MessagingService.PIPE_NAME)
        connection.channel().basic_publish(exchange='', routing_key=MessagingService.PIPE_NAME, body=message)
        connection.close()
    
    def consume_message():
        connection = MessagingService.__connection_factory()
        channel_request = connection.channel()
        channel_request.queue_declare(MessagingService.PIPE_NAME)

        def on_message_callback(channel, method, properties, body):
            print(body)

        channel_request.basic_qos(prefetch_count=1) 
        channel_request.basic_consume(on_message_callback=on_message_callback, 
                                      auto_ack=True, 
                                      queue=MessagingService.PIPE_NAME)

        print('Listening')
        channel_request.start_consuming() 