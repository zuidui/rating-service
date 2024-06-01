from fastapi import APIRouter, Depends

from events.consumer import Consumer

from utils.logger import logger_config

log = logger_config(__name__)
consumer_router = APIRouter()


@consumer_router.post("/start-consumer")
async def start_consumer(consumer: Consumer = Depends(Consumer)):
    log.info("Starting RabbitMQ consumer...")
    consumer.consume()
    return {"message": "Consumer started"}


@consumer_router.post("/stop-consumer")
async def stop_consumer(consumer: Consumer = Depends(Consumer)):
    log.info("Stopping RabbitMQ consumer...")
    consumer.close()
    return {"message": "Consumer stopped"}
