from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from resolver.schema import schema


def graphql_app(get_context):
    return GraphQLRouter(schema, path="/graphql", context_getter=get_context)


graphql_router = APIRouter()


@graphql_router.get(
    "/schema", tags=["Sanity check"], responses={200: {"description": "Get the schema"}}
)
def get_schema():
    return schema.as_str()
