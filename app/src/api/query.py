import strawberry

from service.user_service import UserService

from .schema import UserType


@strawberry.type
class Query:
    @strawberry.field(name="get_all", description="Get all users")
    async def get_all(self) -> list[UserType]:
        return await UserService.get_all()

    @strawberry.field(name="get_by_id", description="Get user by id")
    async def get_by_id(self, user_id: int) -> UserType:
        return await UserService.get_by_id(user_id)
