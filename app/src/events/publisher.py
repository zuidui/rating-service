import aio_pika  # type: ignore
from aio_pika import connect_robust
import json
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
    def __init__(
        self,
        connection: aio_pika.RobustConnection,
        queue_name: str = settings.QUEUE_NAME,
    ):
        self.queue_name = queue_name
        self.connection = connection
        self.channel = None

    async def connect(self):
        self.channel = await self.connection.channel()
        await self._declare_queue()
        log.info(f"Connected to {self.queue_name}")

    async def _declare_queue(self):
        await self.channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, message: Dict[str, Any]):
        if not self.channel:
            raise ConnectionError("Channel is not initialized. Call connect() first.")
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message, cls=DateTimeEncoder).encode()),
            routing_key=self.queue_name,
        )
        log.info(f"Published message to {self.queue_name}: {message}")

    async def close(self):
        if self.connection:
            await self.connection.close()
            log.info(f"Connection to {self.queue_name} closed")


async def start_publisher(loop):
    connection = await connect_robust(
        host=settings.BROKER_HOST,
        port=settings.BROKER_PORT,
        loop=loop,
        heartbeat=settings.BROKER_HEARTBEAT,
        connection_attempts=settings.BROKER_CONNECTION_ATTEMPTS,
        connection_timeout=settings.BROKER_CONNECTION_TIMEOUT,
        attempt_delay=settings.BROKER_ATTEMPT_DELAY,
    )
    publisher = Publisher(connection)
    await publisher.connect()
    return publisher


async def publish_event(
    publisher: Publisher, event_type: str, data: Dict[str, Any]
) -> bool:
    event = {"event_type": event_type, "data": data}
    await publisher.publish(event)
    return True
