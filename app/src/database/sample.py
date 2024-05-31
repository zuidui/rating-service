from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model.user_model import User


async def insert_sample_data(session: AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()

    if not users:
        sample_users = [
            User(name="Alice", email="alice@example.com", password="alice123"),
            User(name="Bob", email="bob@example.com", password="bob123"),
            User(name="Charlie", email="charlie@example.com", password="charlie123"),
        ]
        session.add_all(sample_users)
        await session.commit()
