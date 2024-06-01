import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.sample import insert_sample_data
from database.session import db

from events.consumer import start_consumer
from events.publisher import start_publisher

from routes.graphql import graphql_router
from routes.consumer import consumer_router
from routes.health import health_router

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # As many consumers as needed can be started here and need to be closed when the app is closed
    consumer = start_consumer("match-events")
    publisher = start_publisher()
    try:
        await db.create_database()
        async with db.get_db() as session:
            await insert_sample_data(session)
        yield
    finally:
        consumer.close()
        publisher.close()
        await db.close_database()


def init_app():
    log.info("Creating application...")
    log.info(f"Image: {settings.IMAGE_NAME}:{settings.IMAGE_VERSION}")
    log.info(f"Author: {settings.AUTHOR}")
    log.info(f"License: {settings.LICENSE}")
    log.info(f"Application module: {settings.APP_MODULE}")
    log.info(f"Application port: {settings.APP_PORT}")
    log.info(f"Application host: {settings.APP_HOST}")
    log.info(f"Application description: {settings.APP_DESCRIPTION}")
    log.info(f"API prefix: {settings.API_PREFIX}")
    log.info(f"Documentation URL: {settings.DOC_URL}")
    log.info(f"Database URI: {settings.SQLALCHEMY_DATABASE_URI}")

    app = FastAPI(
        title=settings.IMAGE_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.IMAGE_VERSION,
        openapi_url=None,
        docs_url=None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8081"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(graphql_router(), prefix=settings.API_PREFIX)
    app.include_router(consumer_router, prefix=settings.API_PREFIX)

    log.info("Application created successfully")

    return app


app = init_app()

if __name__ == "__main__":
    log.info("Starting application...")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
    log.info("Application started")
