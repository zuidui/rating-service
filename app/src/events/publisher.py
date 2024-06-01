import pika  # type: ignore
import json
import threading
from queue import Queue

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class Publisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.BROKER_HOST, port=settings.BROKER_PORT
            )
        )
        self.queue_name = settings.QUEUE_NAME
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.message_queue = Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            message = self.message_queue.get()
            if message is None:
                break
            self._publish(message)

    def _publish(self, message):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        log.info(f"Published message to {self.queue_name}: {message}")

    def publish(self, message):
        self.message_queue.put(message)

    def close(self):
        self.message_queue.put(None)
        self.thread.join()
        self.connection.close()
        log.info(f"Connection to {self.queue_name} closed")


def start_publisher():
    return Publisher()
