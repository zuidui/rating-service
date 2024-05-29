import databases
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()

database = databases.Database(
    settings.SQLALCHEMY_DATABASE_URI,
    ssl=settings.SQLALCHEMY_SSL,
    min_size=settings.SQLALCHEMY_MIN_POOL,
    max_size=settings.SQLALCHEMY_MAX_POOL,
)

metadata = db.MetaData()

engine = db.create_engine(str(database.url))

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
