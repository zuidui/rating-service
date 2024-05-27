from fastapi import FastAPI

from demo.routers import users
from demo.internal import admin

from demo.internal.logger import logger_config
from demo.internal.config import get_settings

log = logger_config(__name__)
settings = get_settings()

log.info("Creating application...")

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url=settings.DOC_URL,
    debug=settings.ENV,
)

app.include_router(users.router, prefix=settings.PREFIX)
app.include_router(admin.router)

log.info("Application created")
log.info(f"Application name: {settings.APP_NAME}")
log.info(f"Application version: {settings.VERSION}")
log.info(f"Application environment: {settings.ENV}")
log.info(f"Application prefix: {settings.PREFIX}")
log.info(f"Application docs url: {settings.DOC_URL}")
log.info(f"Application description: {settings.DESCRIPTION}")
