from sqlalchemy import update as sql_update, delete as sql_delete
from sqlalchemy.future import select as sql_select
from model.user_model import User
from database.session import db
from utils.logger import logger_config

log = logger_config(__name__)


class UserRepository:
    @staticmethod
    async def create(user_data: User):
        async with db.get_db() as session:
            async with db.commit_rollback(session):
                session.add(user_data)

    @staticmethod
    async def get_by_id(user_id: int):
        async with db.get_db() as session:
            stmt = sql_select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
        return user

    @staticmethod
    async def get_all():
        async with db.get_db() as session:
            stmt = sql_select(User)
            result = await session.execute(stmt)
            users = result.scalars().all()
        return users

    @staticmethod
    async def update(user_id: int, user_data: User):
        async with db.get_db() as session:
            stmt = sql_select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user:
                user.name = user_data.name
                user.email = user_data.email
                user.password = user_data.password

                query = (
                    sql_update(User)
                    .where(User.id == user_id)
                    .values(
                        name=user_data.name,
                        email=user_data.email,
                        password=user_data.password,
                    )
                )
                await session.execute(query)
                await session.commit()

    @staticmethod
    async def delete(user_id: int):
        async with db.get_db() as session:
            query = sql_delete(User).where(User.id == user_id)
            await session.execute(query)
            await session.commit()
