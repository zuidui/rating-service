import strawberry

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def placeholder(self) -> str:
        return "placeholder"
