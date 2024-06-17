import strawberry
from typing import Annotated, Optional

from resolver.player_rating_schema import PlayerRatingList

from service.rating_service import RatingService

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class Query:
    @strawberry.field(name="get_players_rating")
    async def get_players_rating(
        self,
        team_id: Annotated[int, strawberry.argument(name="team_id")],
    ) -> Optional[PlayerRatingList]:
        log.info(f"Getting players rating for team_id: {team_id}")
        return await RatingService.get_players_rating(team_id)
