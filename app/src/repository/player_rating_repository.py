from typing import Optional
from sqlalchemy.future import select as sql_select
from model.player_rating_model import PlayerRating
from data.session import db
from utils.logger import logger_config

log = logger_config(__name__)


class PlayerRatingRepository:
    @staticmethod
    async def create(player_rating: PlayerRating) -> PlayerRating:
        async with db.get_db() as session:
            async with db.commit_rollback(session):
                session.add(player_rating)
                await session.flush()
                await session.refresh(player_rating)
                log.info(f"Player rating created in repository: {player_rating}")
        return player_rating

    @staticmethod
    async def get_rating_by_player_id(
        player_id: int, team_id: int
    ) -> Optional[PlayerRating]:
        async with db.get_db() as session:
            stmt = sql_select(PlayerRating).where(
                PlayerRating.player_id == player_id, PlayerRating.team_id == team_id
            )
            result = await session.execute(stmt)
            player_rating = result.scalars().first()
            if player_rating:
                log.info(f"Player rating found in repository: {player_rating}")
        return player_rating
