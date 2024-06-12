import pika  # type: ignore
import json
import threading
from queue import Queue
from datetime import datetime
from typing import Any, Dict

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class Publisher:
    def __init__(self, queue_name: str = settings.QUEUE_NAME):
        self.queue_name = queue_name
        self.connection = self._create_connection()
        self.channel = self._create_channel()
        self._declare_queue()
        self.message_queue: Queue[Dict[str, Any]] = Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

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

    def _run(self):
        while True:
            message = self.message_queue.get()
            if message is None:
                break
            self._publish(message)

    def _publish(self, message: Dict[str, Any]):
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message, cls=DateTimeEncoder),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
            log.info(f"Published message to {self.queue_name}: {message}")
        except Exception as e:
            log.error(f"Failed to publish message: {message} - Error: {e}")

    def publish(self, message: Dict[str, Any]):
        self.message_queue.put(message)

    def close(self):
        self.message_queue.put(None)
        self.thread.join()
        if self.connection.is_open:
            self.connection.close()
        log.info(f"Connection to {self.queue_name} closed")


def start_publisher(queue_name: str = settings.QUEUE_NAME) -> Publisher:
    return Publisher(queue_name=queue_name)


async def publish_event(
    publisher: Publisher, event_type: str, data: Dict[str, Any]
) -> bool:
    event = {"event_type": event_type, "data": data}
    publisher.publish(event)
    return True
