from typing import Optional
from sqlalchemy.future import select as sql_select
from models.score_model import Score
from data.session import db
from utils.logger import logger_config

log = logger_config(__name__)


class ScoreRepository:
    @staticmethod
    async def create(score: Score) -> Score:
        async with db.get_db() as session:
            async with db.commit_rollback(session):
                session.add(score)
                await session.flush()
                await session.refresh(score)
                log.info(f"Score created in repository: {score}")
        return score

    @staticmethod
    async def get_by_player_id(player_id: int) -> Optional[Score]:
        async with db.get_db() as session:
            stmt = sql_select(Score).where(Score.player_id == player_id)
            result = await session.execute(stmt)
            score = result.scalars().first()
            if score:
                await session.refresh(score)
                log.info(f"Score retrieved from repository: {score}")
        return score
