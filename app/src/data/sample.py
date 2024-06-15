from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from model.score_model import Score
from model.player_rating_model import PlayerRating

from utils.logger import logger_config

log = logger_config(__name__)


async def insert_sample_data(session: AsyncSession, model, sample_data):
    result = await session.execute(select(model))
    records = result.scalars().all()

    if not records:
        session.add_all(sample_data)
        await session.commit()


async def insert_sample_scores(session: AsyncSession):
    sample_scores = [
        Score(
            player_id=1,
            team_id=1,
            score=10,
            created_at=datetime.now(timezone.utc),
        ),
        Score(
            player_id=1,
            team_id=1,
            score=9,
            created_at=datetime.now(timezone.utc),
        ),
        Score(
            player_id=1,
            team_id=1,
            score=8,
            created_at=datetime.now(timezone.utc),
        ),
        Score(
            player_id=2,
            team_id=1,
            score=7,
            created_at=datetime.now(timezone.utc),
        ),
        Score(
            player_id=2,
            team_id=1,
            score=6,
            created_at=datetime.now(timezone.utc),
        ),
        Score(
            player_id=2,
            team_id=1,
            score=5,
            created_at=datetime.now(timezone.utc),
        ),
    ]

    await insert_sample_data(session, Score, sample_scores)


async def insert_sample_player_ratings(session: AsyncSession):
    sample_player_ratings = [
        PlayerRating(
            player_id=1,
            team_id=1,
            average_score=9,
            total_of_scores=3,
            last_updated=datetime.now(timezone.utc),
        ),
        PlayerRating(
            player_id=2,
            team_id=1,
            average_score=6,
            total_of_scores=3,
            last_updated=datetime.now(timezone.utc),
        ),
    ]

    await insert_sample_data(session, PlayerRating, sample_player_ratings)
