from datetime import datetime
import json
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.score_model import Score
from models.player_rating_model import PlayerRating

from utils.logger import logger_config

log = logger_config(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))


async def insert_sample_data(session: AsyncSession, model, sample_data):
    result = await session.execute(select(model))
    records = result.scalars().all()

    if not records:
        session.add_all(sample_data)
        await session.commit()


async def insert_sample_scores(session: AsyncSession):
    with open(os.path.join(current_directory, "scores.json"), "r") as f:
        sample_scores = json.load(f)
    for score in sample_scores:
        score["created_at"] = datetime.fromisoformat(score["created_at"])
    scores = [Score(**score) for score in sample_scores]
    await insert_sample_data(session, Score, scores)


async def insert_sample_player_ratings(session: AsyncSession):
    with open(os.path.join(current_directory, "player_ratings.json"), "r") as f:
        sample_player_ratings = json.load(f)
    for rating in sample_player_ratings:
        rating["last_updated"] = datetime.fromisoformat(rating["last_updated"])
    player_ratings = [PlayerRating(**rating) for rating in sample_player_ratings]
    await insert_sample_data(session, PlayerRating, player_ratings)
