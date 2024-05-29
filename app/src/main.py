import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from utils.logger import logger_config
from utils.config import get_settings
from resolver.query import Query
from resolver.mutation import Mutation

log = logger_config(__name__)
settings = get_settings()

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
log.info(f"SQLAlchemy URI: {settings.SQLALCHEMY_DATABASE_URI}")
log.info(f"SQLAlchemy SSL: {settings.SQLALCHEMY_SSL}")
log.info(f"SQLAlchemy min pool: {settings.SQLALCHEMY_MIN_POOL}")
log.info(f"SQLAlchemy max pool: {settings.SQLALCHEMY_MAX_POOL}")


app = FastAPI(
    title=settings.IMAGE_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.IMAGE_VERSION,
    openapi_url=None,
    docs_url=None,
)

origins = [
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = Schema(query=Query, mutation=Mutation)

app.include_router(GraphQLRouter(schema, path="/graphql"), prefix=settings.API_PREFIX)

if __name__ == "__main__":
    log.info("Starting application...")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
    log.info("Application started")
