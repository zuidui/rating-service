import strawberry

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class ScoreMutation:
    @strawberry.mutation
    def create_score(self, team_id: int, player_id: int, player_score: float) -> str:
        log.info(
            f"Creating score for team_id: {team_id}, player_id: {player_id}, player_score: {player_score}"
        )
        return "Score created successfully"
