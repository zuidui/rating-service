from typing import Annotated, Optional
import strawberry

from resolver.player_rating_schema import TeamRatingInput, TeamRatingOutput
from service.rating_service import RatingService

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation(name="rate_players")
    async def rate_players(
        self,
        info: strawberry.Info,
        team_rating: Annotated[
            TeamRatingInput, strawberry.argument(name="team_rating")
        ],
    ) -> Optional[TeamRatingOutput]:
        publisher = info.context["publisher"]
        log.info(f"Rating players for team {team_rating.team_id}")
        return await RatingService.rate_players(publisher, team_rating)
