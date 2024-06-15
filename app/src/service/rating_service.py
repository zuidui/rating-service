from fastapi import FastAPI
from typing import Any, Dict, Optional
import httpx

from datetime import datetime, timezone

from repository.player_rating_repository import PlayerRatingRepository
from repository.score_repository import ScoreRepository

from model.score_model import Score
from model.player_rating_model import PlayerRating

from resolver.score_schema import ScoreInput, ScoreType
from resolver.player_rating_schema import PlayerRatingInput, RatingType

from events.publisher import Publisher, publish_event

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()

class RatingService:
    @staticmethod
    async def send_to_api_gateway(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            log.debug(
                f"Sending request to {settings.API_GATEWAY_URL} with payload: {payload}"
            )
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.API_GATEWAY_URL}", json=payload
                )
                response.raise_for_status()
                log.debug(f"Response received: {response.json()}")
                return response.json().get("data")
        except httpx.HTTPStatusError as e:
            log.error(
                f"Request failed with status {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            log.error(f"An error occurred while requesting {e.request.url!r}.")
        except Exception as e:
            log.error(f"Unexpected error: {e}")
        return None

    @staticmethod
    async def handle_message(app: FastAPI, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        publisher = app.state.publisher
        event_type = message["event_type"]
        data = message["data"]
        if event_type == "create_player":
            player_team_id = data["player_team_id"]
            player_id = data["player_id"]

            new_score = ScoreInput(
                player_id=player_id,
                team_id=player_team_id,
                player_score=5,
            )
            await RatingService.create_score(new_score, publisher)
        elif event_type == "create_score":
            player_team_id = data["player_team_id"]
            player_id = data["player_id"]
            score_value = data["player_score"]
            score = Score(
                player_id=player_id,
                player_team_id=player_team_id,
                score_value=score_value,
            )
            await RatingService.update_rating(score, publisher)
        elif event_type == "create_rating" or event_type == "update_rating":
            player_team_id = data["player_team_id"]
            player_id = data["player_id"]
            player_score = data["player_average_score"]
            query = f"""
            query {{
                player_rating_info(
                    player_id: {player_id}, 
                    player_team_id: {player_team_id},
                    player_score: {player_score} 
                ) 
                {{
                    player_id
                    player_team_id
                    player_average_score
                }}
            }}
            """
            payload = {"query": query}
            log.info(f"Sending GraphQL query: {query}")
            await RatingService.send_to_api_gateway(payload)
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
            if not await RatingService.rating_exists_by_player_id( 
                new_score.player_id, new_score.team_id
            ):
                log.info(
                    f"Player rating for player_id: {new_score.player_id} and team_id: {new_score.team_id} does not exist. Creating new player rating."
                )
                new_rating = PlayerRating(
                    player_id=new_score.player_id,
                    team_id=new_score.team_id,
                    average_score=new_score.score,
                    total_of_scores=1,
                    last_updated=datetime.now(timezone.utc),
                )

                rating = (await PlayerRatingRepository.create(new_rating)).to_dict()
                rating_created = RatingType(
                    player_id=rating["player_id"],
                    player_team_id=rating["team_id"],
                    player_average_score=rating["average_score"],
                )

                log.info(
                    f"Publishing event: create_rating with data: {{'player_id': {rating_created.player_id}, 'team_id': {rating_created.player_team_id}, 'player_average_score': {rating_created.player_average_score}}}"
                )
                await publish_event(
                    publisher,
                    "create_rating",
                    {
                        "player_id": rating_created.player_id,
                        "team_id": rating_created.player_team_id,
                        "player_average_score": rating_created.player_average_score,
                    },
                )
            else:
                log.info(f"Player rating exists for player_id: {new_score.player_id} - Creating new score.")
                score = (await ScoreRepository.create(new_score)).to_dict()
                score_created = ScoreType(
                    player_id=score["player_id"],
                    team_id=score["team_id"],
                    player_score=score["score"],
                )

                log.info(
                    f"Publishing event: create_score with data: {{'player_id': {score_created.player_id}, 'team_id': {score_created.team_id}, 'score': {score_created.player_score}}}"
                )

                await publish_event(
                    publisher,
                    "create_score",
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
    async def update_rating(
        rating_data: PlayerRatingInput,
        publisher: Publisher,
    ) -> Optional[RatingType]:
        log.info(f"Updating score: {rating_data}")

        if not await RatingService.rating_exists_by_player_id(
            rating_data.player_id, rating_data.player_team_id
        ):
            log.info(
                f"Player rating for player_id: {rating_data.player_id} and team_id: {rating_data.player_team_id} does not exist. Creating new player rating."
            )
            new_rating = PlayerRating(
                player_id=rating_data.player_id,
                team_id=rating_data.player_team_id,
                average_score=rating_data.player_score,
                total_of_scores=1,
                last_updated=datetime.now(timezone.utc),
            )

            try:
                rating = (await PlayerRatingRepository.create(new_rating)).to_dict()
                rating_created = RatingType(
                    player_id=rating["player_id"],
                    player_team_id=rating["team_id"],
                    player_average_score=rating["average_score"],
                )

                log.info(
                    f"Publishing event: create_rating with data: {{'player_id': {rating_created.player_id}, 'team_id': {rating_created.player_team_id}, 'player_average_score': {rating_created.player_average_score}}}"
                )
                await publish_event(
                    publisher,
                    "create_rating",
                    {
                        "player_id": rating_created.player_id,
                        "team_id": rating_created.player_team_id,
                        "player_average_score": rating_created.player_average_score,
                    },
                )
            except Exception as e:
                log.error(f"Error creating rating: {e}")
                raise e
            return rating_created
        else:
            log.info(
                f"Player rating for player_id: {rating_data.player_id} and team_id: {rating_data.player_team_id} exists. Updating player rating."
            )
            player_rating = await PlayerRatingRepository.get_rating_by_player_id(
                rating_data.player_id, rating_data.player_team_id
            )

            if player_rating is None:
                raise Exception("Error updating rating")

            new_rating = PlayerRating(
                player_id=player_rating.player_id,
                team_id=player_rating.team_id,
                total_of_scores=player_rating.total_of_scores + 1,
                average_score=(player_rating.average_score + rating_data.player_score)
                / (player_rating.total_of_scores + 1),
                last_updated=datetime.now(timezone.utc),
            )

            try:
                rating = (await PlayerRatingRepository.update(new_rating)).to_dict()

                rating_updated = RatingType(
                    player_id=rating["player_id"],
                    player_team_id=rating["team_id"],
                    player_average_score=rating["average_score"],
                )

                log.info(
                    f"Publishing event: update_rating with data: {{'player_id': {rating_updated.player_id}, 'team_id': {rating_updated.player_team_id}, 'player_average_score': {rating_updated.player_average_score}}}"
                )
                await publish_event(
                    publisher,
                    "update_rating",
                    {
                        "player_id": rating_updated.player_id,
                        "team_id": rating_updated.player_team_id,
                        "player_average_score": rating_updated.player_average_score,
                    },
                )
            except Exception as e:
                log.error(f"Error updating rating: {e}")
                raise e
            return rating_updated

    @staticmethod
    async def get_player_rating(player: PlayerRatingInput) -> Optional[RatingType]:
        player_rating = await PlayerRatingRepository.get_rating_by_player_id(
            player.player_id, player.player_team_id
        )
        if player_rating is not None:
            return RatingType(
                player_id=player_rating["player_id"],
                player_team_id=player_rating["team_id"],
                player_average_score=player_rating["average_score"],
            )
        return None
