import strawberry
from strawberry.types import Info
from typing import Annotated, Optional

from service.rating_service import RatingService

from resolver.score_schema import ScoreInput, ScoreType

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation(name="create_score")
    async def create_score(
        self,
        info: Info,
        new_score: Annotated[ScoreInput, strawberry.argument(name="new_score")],
    ) -> Optional[ScoreType]:
        publisher = info.context["publisher"]
        log.info(f"Creating score: {new_score}")
        return await RatingService.create_score(new_score, publisher)
