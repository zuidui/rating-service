from strawberry import Schema

from resolver.mutation import Mutation
from resolver.query import Query

schema = Schema(query=Query, mutation=Mutation)
