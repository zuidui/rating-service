from database.data import get_db, users

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


async def get_user(id: int):
    db = get_db()
    user = await db.execute(users.select().where(users.c.id == id)).fetchone()
    db.close()
    return user

async def create_user(name: str, email: str, password: str):
    db = get_db()
    user = {"name": name, "email": email, "password": password}
    await db.execute(users.insert().values(user))
    db.close()
    return user

async def update_user(id: int, name: str, email: str, password: str):
    db = get_db()
    user = {"name": name, "email": email, "password": password}
    await db.execute(users.update().values(user).where(users.c.id == id))
    db.close()
    return user

async def delete_user(id: int):
    db = get_db()
    await db.execute(users.delete().where(users.c.id == id))
    db.close()
    return True
