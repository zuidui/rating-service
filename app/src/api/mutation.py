import strawberry

from service.user_service import UserService

from .schema import UserType, UserInput


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, user_data: UserInput) -> UserType:
        return await UserService.create(user_data)

    @strawberry.mutation
    async def update_user(self, user_id: int, user_data: UserInput) -> UserType:
        return await UserService.update(user_id, user_data)

    @strawberry.mutation
    async def delete_user(self, user_id: int) -> bool:
        return await UserService.delete(user_id)
