import pika  # type: ignore
import json
import threading
import asyncio

from service.rating_service import RatingService

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class Consumer:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = self._create_connection()
        self.channel = self._create_channel()
        self._declare_queue()

    def _create_connection(self):
        return pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.BROKER_HOST, port=settings.BROKER_PORT
            )
        )

    def _create_channel(self):
        return self.connection.channel()

    def _declare_queue(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def consume(self):
        try:
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=self._callback, auto_ack=True
            )
            log.info(f"Starting to consume messages from {self.queue_name}")
            self.channel.start_consuming()
        except Exception as e:
            log.error(f"Error consuming messages: {e}")
        finally:
            self.close()

    def close(self):
        if self.connection.is_open:
            self.connection.close()
            log.info("Connection closed")

    def _callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            asyncio.run(self._process_message(message))
            log.info(f"Received message: {message}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode message: {body} - Error: {e}")

    async def _process_message(self, message):
        await RatingService.handle_message(message)


def start_consumer(queue_name: str = settings.QUEUE_NAME) -> Consumer:
    consumer = Consumer(queue_name=queue_name)
    consumer_thread = threading.Thread(target=consumer.consume, daemon=True)
    consumer_thread.start()
    return consumer
