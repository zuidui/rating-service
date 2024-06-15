import strawberry


@strawberry.type
class ScoreType:
    team_id: int = strawberry.field(name="team_id")
    player_id: int = strawberry.field(name="player_id")
    player_score: int = strawberry.field(name="player_score")


@strawberry.input
class ScoreInput:
    team_id: int = strawberry.field(name="player_team_id")
    player_id: int = strawberry.field(name="player_id")
    player_score: int = strawberry.field(name="player_score")
