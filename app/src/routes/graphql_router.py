from strawberry.fastapi import GraphQLRouter

from resolver.schema import schema


def graphql_router(get_context):
    return GraphQLRouter(schema, path="/graphql", context_getter=get_context)
