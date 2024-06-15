import strawberry


@strawberry.type
class RatingType:
    player_id: int = strawberry.field(name="player_id")
    player_team_id: int = strawberry.field(name="player_team_id")
    player_average_score: float = strawberry.field(name="player_average_score")


@strawberry.input
class PlayerRatingInput:
    player_id: int = strawberry.field(name="player_id")
    player_team_id: int = strawberry.field(name="player_team_id")
    player_score: int = strawberry.field(name="player_score")
