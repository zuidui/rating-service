import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from database.sample import insert_sample_data

from database.session import db

from resolver.query import Query
from resolver.mutation import Mutation

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.create_database()
        async with db.get_db() as session:
            await insert_sample_data(session)
        yield
    finally:
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

    schema = Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema, path="/graphql")
    app.include_router(graphql_app, prefix=settings.API_PREFIX)

    log.info("Application created successfully")

    return app


app = init_app()

if __name__ == "__main__":
    log.info("Starting application...")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
    log.info("Application started")
