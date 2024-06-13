import strawberry


@strawberry.type
class Query:
    @strawberry.field(name="get_player_score")
    def get_player_score(self, team_id: int, player_id: int) -> str:
        return f"Player rating for team_id: {team_id}, player_id: {player_id} is 8.5"
