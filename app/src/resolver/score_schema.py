import strawberry


@strawberry.type
class ScoreType:
    team_id: int = strawberry.field(name="team_id")
    player_id: int = strawberry.field(name="player_id")
    player_score: float = strawberry.field(name="player_score")
