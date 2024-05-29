import strawberry
from typing import Optional

from schema.user_schema import UserType
from service.user_service import create_user, update_user, delete_user

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str, password: str) -> UserType:
        user = await create_user(name, email, password)
        return UserType(id=user["id"], name=user["name"], email=user["email"], password=user["password"])

    @strawberry.mutation
    async def update_user(self, id: int, name: Optional[str], email: Optional[str], password: Optional[str]) -> UserType:
        user = await update_user(id, name, email, password)
        return UserType(id=user["id"], name=user["name"], email=user["email"], password=user["password"])

    @strawberry.mutation
    async def delete_user(self, id: int) -> bool:
        return await delete_user(id)
