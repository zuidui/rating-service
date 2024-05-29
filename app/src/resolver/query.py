import strawberry
from typing import Optional

from schema.user_schema import UserType
from service.user_service import get_user


@strawberry.type
class Query:
    @strawberry.field
    async def resolve_user(self, id: int) -> Optional[UserType]:
        user_data = await get_user(id)
        if user_data:
            return UserType(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
            )
        return None
