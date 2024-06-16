import aio_pika  # type: ignore
from aio_pika import ExchangeType, connect_robust
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
        exchange_name: str = settings.EXCHANGE_NAME,
    ):
        self.exchange_name = exchange_name
        self.connection = connection
        self.channel = None
        self.exchange = None

    async def connect(self):
        self.channel = await self.connection.channel()
        await self._declare_exchange()
        log.info(f"Connected to exchange {self.exchange_name}")

    async def _declare_exchange(self):
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT, durable=True)


    async def publish(self, message: Dict[str, Any]):
        if not self.exchange:
            raise ConnectionError("Exchange is not initialized. Call connect() first.")
        await self.exchange.publish(
            aio_pika.Message(body=json.dumps(message, cls=DateTimeEncoder).encode()),
            routing_key="",
        )
        log.info(f"Published message to exchange {self.exchange_name}: {message}")


    async def close(self):
        if self.connection:
            await self.connection.close()
            log.info(f"Connection to exchange {self.exchange_name} closed")


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
