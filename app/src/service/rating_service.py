from fastapi import FastAPI
from typing import Any, Dict, Optional
import httpx

from datetime import datetime, timezone

from repository.player_rating_repository import PlayerRatingRepository
from repository.score_repository import ScoreRepository

from model.score_model import Score
from model.player_rating_model import PlayerRating

from resolver.score_schema import ScoreInput, ScoreType
from resolver.player_rating_schema import (
    PlayerRatingInput,
    PlayerRatingList,
    PlayerRatingOutput,
    PlayerRatingType,
)

from events.publisher import Publisher, publish_event

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class RatingService:
    @staticmethod
    async def handle_message(
        app: FastAPI, message: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        publisher = app.state.publisher
        event_type = message["event_type"]
        data = message["data"]
        if event_type == "player_created":
            player_team_id = data["team_id"]
            player_id = data["player_id"]

            new_score = ScoreInput(
                player_id=player_id,
                team_id=player_team_id,
                player_score=5,
            )
            await RatingService.create_score(new_score, publisher)
        # elif event_type == "create_score":
        #    player_team_id = data["player_team_id"]
        #    player_id = data["player_id"]
        #    score_value = data["player_score"]
        #    score = Score(
        #        player_id=player_id,
        #        player_team_id=player_team_id,
        #        score_value=score_value,
        #    )
        #    await RatingService.update_rating(score, publisher)
        else:
            log.info(f"Event type {event_type} consumed but not handled.")
        return data

    @staticmethod
    async def rating_exists_by_player_id(player_id: int, team_id: int) -> bool:
        player_rating = await PlayerRatingRepository.get_rating_by_player_id(
            player_id, team_id
        )
        return player_rating is not None

    @staticmethod
    async def create_score(
        score_data: ScoreInput,
        publisher: Publisher,
    ) -> Optional[ScoreType]:
        log.info(f"Creating score: {score_data}")

        new_score = Score(
            player_id=score_data.player_id,
            team_id=score_data.team_id,
            score=score_data.player_score,
            created_at=datetime.now(timezone.utc),
        )

        try:
            player_id = int(new_score.player_id)
            team_id = int(new_score.team_id)
            player_score = int(new_score.score)
            if not await RatingService.rating_exists_by_player_id(player_id, team_id):
                log.info(
                    f"Player rating for player_id: {new_score.player_id} and team_id: {new_score.team_id} does not exist. Creating new player rating."
                )
                new_rating = PlayerRatingInput(
                    player_id=player_id,
                    player_team_id=team_id,
                    player_score=player_score,
                )
                await RatingService.create_rating(new_rating, publisher)
            score = (await ScoreRepository.create(new_score)).to_dict()
            score_created = ScoreType(
                player_id=score["player_id"],
                team_id=score["team_id"],
                player_score=score["score"],
            )

            log.info(
                f"Publishing event: score_created with data: {{'player_id': {score_created.player_id}, 'team_id': {score_created.team_id}, 'score': {score_created.player_score}}}"
            )

            await publish_event(
                publisher,
                "score_created",
                {
                    "player_id": score_created.player_id,
                    "team_id": score_created.team_id,
                    "score": score_created.player_score,
                },
            )
            return score_created
        except Exception as e:
            log.error(f"Error creating score: {e}")
            raise e

    @staticmethod
    async def create_rating(
        new_score: PlayerRatingInput, publisher: Publisher
    ) -> Optional[PlayerRatingType]:
        new_rating = PlayerRating(
            player_id=new_score.player_id,
            team_id=new_score.player_team_id,
            average_score=new_score.player_score,
            total_of_scores=1,
            last_updated=datetime.now(timezone.utc),
        )

        rating = (await PlayerRatingRepository.create(new_rating)).to_dict()
        rating_created = PlayerRatingType(
            player_id=rating["player_id"],
            player_team_id=rating["team_id"],
            player_average_rating=rating["average_score"],
        )

        log.info(
            f"Publishing event: rating_updated with data: {{'team_id': {rating_created.player_team_id}}}"
        )
        await publish_event(
            publisher,
            "rating_updated",
            {
                "team_id": rating_created.player_team_id,
            },
        )
        return rating_created

    @staticmethod
    async def get_players_rating(team_id: int) -> PlayerRatingList:
        players = await PlayerRatingRepository.get_players_by_team_id(team_id)
        players_dict = [player.to_dict() for player in players]
        if players:
            players_data = [
                PlayerRatingOutput(
                    player_id=player["player_id"],
                    player_average_rating=player["average_score"],
                )
                for player in players_dict
            ]
            return PlayerRatingList(team_id=team_id, players_data=players_data)
        raise Exception("No players found")
