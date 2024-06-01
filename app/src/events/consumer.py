import pika  # type: ignore
import json
import threading

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class Consumer:
    def __init__(self, queue_name=settings.QUEUE_NAME):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.BROKER_HOST, port=settings.BROKER_PORT
            )
        )
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def consume(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True
        )
        log.info("Consuming messages...")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
        log.info("Connection closed")

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        log.info(f"Received message: {message}")


def start_consumer(queue_name=settings.QUEUE_NAME):
    consumer = Consumer(queue_name=queue_name)
    consumer_thread = threading.Thread(target=consumer.consume)
    consumer_thread.start()
    return consumer
