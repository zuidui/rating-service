from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from resolver.query import Query
from resolver.mutation import Mutation


def graphql_router():
    schema = Schema(query=Query, mutation=Mutation)
    return GraphQLRouter(schema, path="/graphql")
