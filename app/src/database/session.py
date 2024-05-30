from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from contextlib import asynccontextmanager

from typing import AsyncGenerator

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()

Base = declarative_base()


class DatabaseSession:
    def __init__(self):
        self.engine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            echo=True,
        )

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
        )

        self.metadata = Base.metadata

    async def create_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def drop_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.drop_all)

    async def close_database(self):
        await self.engine.dispose()

    async def __aenter__(self) -> AsyncSession:
        self.db = self.SessionLocal()
        return self.db

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.close()

    @asynccontextmanager
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.SessionLocal() as db:
            yield db

    @asynccontextmanager
    async def commit_rollback(self, session: AsyncSession):
        try:
            yield
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


db = DatabaseSession()
