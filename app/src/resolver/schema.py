from strawberry import Schema

from resolver.player_rating_query import PlayerRatingQuery
from resolver.player_rating_mutation import PlayerRatingMutation
from resolver.score_query import ScoreQuery
from resolver.score_mutation import ScoreMutation


class Query(PlayerRatingQuery, ScoreQuery):
    pass


class Mutation(PlayerRatingMutation, ScoreMutation):
    pass


schema = Schema(query=Query, mutation=Mutation)
