import os
import secrets

from dotenv import load_dotenv

from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))


class Settings(BaseSettings):
    DEV: bool
    DEBUG: bool
    DOCKERHUB_USERNAME: str
    AUTHOR: str
    LICENSE: str
    IMAGE_NAME: str
    IMAGE_VERSION: str
    APP_MODULE: str
    APP_PORT: int
    APP_HOST: str
    APP_DESCRIPTION: str
    API_PREFIX: str
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    DOC_URL: str
    DEPENDENCIES: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    API_GATEWAY_HOST: str
    API_GATEWAY_PORT: int
    BROKER_HOST: str
    BROKER_PORT: int
    QUEUE_NAME: str

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def API_GATEWAY_URL(self):
        return f"http://{self.API_GATEWAY_HOST}:{self.API_GATEWAY_PORT}{self.API_PREFIX}/graphql"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings():
    return Settings()
