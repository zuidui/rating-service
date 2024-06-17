from typing import List
import strawberry


@strawberry.type
class PlayerRatingType:
    player_id: int = strawberry.field(name="player_id")
    player_team_id: int = strawberry.field(name="player_team_id")
    player_average_rating: float = strawberry.field(name="player_average_rating")


@strawberry.input
class PlayerRatingInput:
    player_id: int = strawberry.field(name="player_id")
    player_team_id: int = strawberry.field(name="player_team_id")
    player_score: int = strawberry.field(name="player_score")


@strawberry.type
class PlayerRatingOutput:
    player_id: int = strawberry.field(name="player_id")
    player_average_rating: float = strawberry.field(name="player_average_rating")


@strawberry.type
class PlayerRatingList:
    team_id: int = strawberry.field(name="team_id")
    players_data: List[PlayerRatingOutput] = strawberry.field(name="players_data")
