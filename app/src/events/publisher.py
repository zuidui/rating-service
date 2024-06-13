import pika  # type: ignore
import time
import json
import threading
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker
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
        self.message_queue: Queue[Dict[str, Any]] = Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        self.connect()

    def connect(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=settings.BROKER_HOST, port=settings.BROKER_PORT,
                        heartbeat=settings.BROKER_HEARTBEAT,
                        connection_attempts=settings.BROKER_CONNECTION_ATTEMPTS,
                        retry_delay=settings.BROKER_ATTEMPT_DELAY,
                        blocked_connection_timeout=settings.BROKER_CONNECTION_TIMEOUT,
                    )
                )
                self.channel = self.connection.channel()
                self._declare_queue()
                break
            except AMQPConnectionError as e:
                log.error(f"Connection error: {e}, retrying in 5 seconds...")
                time.sleep(5)

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
            if self.connection.is_closed or self.channel.is_closed:
                self.connect()
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message, cls=DateTimeEncoder),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
            log.info(f"Published message to {self.queue_name}: {message}")
        except (AMQPConnectionError, ChannelClosedByBroker) as e:
            log.error(f"Failed to publish message due to connection error: {e}, reconnecting...")
            self.connect()
            self._publish(message)
        except Exception as e:
            log.error(f"Failed to publish message: {message} - Error: {e}")


    def publish(self, message: Dict[str, Any]):
        self.message_queue.put(message)

    def close(self):
        self.message_queue.put(None)
        self.thread.join()
        if self.connection and self.connection.is_open:
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
