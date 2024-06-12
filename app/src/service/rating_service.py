from typing import Any, Dict, Optional
import httpx

from repository.player_rating_repository import PlayerRatingRepository

from utils.logger import logger_config
from utils.config import get_settings

log = logger_config(__name__)
settings = get_settings()


class RatingService:
    @staticmethod
    async def handle_message(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        event_type = message["event_type"]
        data = message["data"]
        if event_type == "create_player":
            player_name = data["player_name"]
            player_team_id = data["player_team_id"]
            player_id = data["player_id"]
            if not all([player_name, player_team_id, player_id]):
                log.error("Missing required fields to get player rating")
                return None
            player_rating = await PlayerRatingRepository.get_rating_by_player_id(
                player_id, player_team_id
            )
            query = f"""
            query {{
                player_rating(player_id: {player_id}, 
                player_name: {player_name}, 
                player_rating: {player_rating}) 
                {{
                    player_id
                    player_name
                    player_rating
                }}
            }}
            """
            payload = {"query": query}
        log.debug(f"Sending GraphQL: {payload['query']}")
        return await RatingService.send_to_api_gateway(payload)

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
