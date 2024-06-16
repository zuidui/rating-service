import strawberry
from typing import Annotated, Optional

from resolver.player_rating_schema import PlayerRatingInput, PlayerRatingType

from service.rating_service import RatingService


@strawberry.type
class Query:
    @strawberry.field(name="get_player_rating")
    async def get_player_rating(
        self,
        player: Annotated[PlayerRatingInput, strawberry.argument(name="player")],
    ) -> Optional[PlayerRatingType]:
        return await RatingService.get_player_rating(player)
