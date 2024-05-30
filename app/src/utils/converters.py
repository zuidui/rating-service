from typing import Optional

from model.user_model import User
from api.schema import UserType


def convert_user_to_usertype(user: Optional[User]) -> UserType:
    if user is None:
        raise ValueError("Cannot convert None to UserType")

    return UserType(
        id=int(user.id),
        name=str(user.name),
        email=str(user.email),
        password=str(user.password),
    )
