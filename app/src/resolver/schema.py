import strawberry

from typing import Optional


@strawberry.type
class UserType:
    id: Optional[int]
    name: str
    email: str
    password: str


@strawberry.input
class UserInput:
    name: str
    email: str
    password: str
