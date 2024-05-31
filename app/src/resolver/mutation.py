import strawberry

from service.user_service import UserService

from resolver.schema import UserType, UserInput


@strawberry.type
class Mutation:
    @strawberry.mutation(name="create", description="Create a new user")
    async def create(self, user_data: UserInput) -> UserType:
        return await UserService.create(user_data)

    @strawberry.mutation(name="update", description="Update an existing user")
    async def update(self, user_id: int, user_data: UserInput) -> UserType:
        return await UserService.update(user_id, user_data)

    @strawberry.mutation(name="delete", description="Delete an existing user")
    async def delete(self, user_id: int) -> bool:
        return await UserService.delete(user_id)
