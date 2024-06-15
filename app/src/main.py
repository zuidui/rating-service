import uvicorn
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from data.sample import insert_sample_scores, insert_sample_player_ratings
from data.session import db

from events.consumer import start_consumer
from events.publisher import Publisher, start_publisher

from routes.graphql_router import graphql_app, graphql_router
from routes.health_router import health_router

from utils.logger import logger_config

from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    consumer = await start_consumer(loop, app)
    publisher = await start_publisher(loop)
    try:
        await db.create_database()
        async with db.get_db() as session:
            await insert_sample_player_ratings(session)
            await insert_sample_scores(session)
        app.state.consumer = consumer
        app.state.publisher = publisher
        yield
    finally:
        await consumer.close()
        await publisher.close()
        await db.close_database()


async def get_context(request: Request) -> dict:
    return {"publisher": request.app.state.publisher}


def init_app():
    log.info("Creating application...")
    log.info(f"Image: {settings.IMAGE_NAME}:{settings.IMAGE_VERSION}")
    log.info(f"Author: {settings.DOCKERHUB_USERNAME}")
    log.info(f"Debug mode: {settings.DEBUG}")
    log.info(f"Debug port: {settings.DEBUG_PORT}")
    log.info(f"Application module: {settings.APP_MODULE}")
    log.info(f"Application port: {settings.APP_PORT}")
    log.info(f"Application host: {settings.APP_HOST}")
    log.info(f"Application description: {settings.APP_DESCRIPTION}")
    log.info(f"API prefix: {settings.API_PREFIX}")
    log.info(
        f"Service API: http://{settings.IMAGE_NAME}:{settings.APP_PORT}{settings.API_PREFIX}/graphql"
    )
    log.info(
        f"Service health-check: http://{settings.IMAGE_NAME}:{settings.APP_PORT}/health"
    )
    log.info(f"Service schema: http://{settings.IMAGE_NAME}:{settings.APP_PORT}/schema")
    log.info(f"Database URL: {settings.SQLALCHEMY_DATABASE_URI}")
    log.info(f"API Gateway URL: {settings.API_GATEWAY_URL}")
    log.info(f"Broker: {settings.BROKER_URL}/{settings.QUEUE_NAME}")

    app = FastAPI(
        title=settings.IMAGE_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.IMAGE_VERSION,
        openapi_url=None,
        docs_url=None,
        lifespan=lifespan,
    )

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.router.lifespan_context = lifespan
    app.include_router(health_router)
    app.include_router(graphql_router)
    app.include_router(graphql_app(get_context), prefix=settings.API_PREFIX)

    log.info("Application created successfully")

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
