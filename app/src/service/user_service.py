from model.user_model import User

from resolver.schema import UserType, UserInput

from repository.user_repository import UserRepository

from utils.logger import logger_config
from utils.converters import convert_user_to_usertype

log = logger_config(__name__)


class UserService:
    @staticmethod
    async def get_all() -> list[UserType]:
        log.info("Getting users")

        users = await UserRepository.get_all()

        log.info(f"Users: {users}")

        return [
            user_type
            for user in users
            if (user_type := convert_user_to_usertype(user)) is not None
        ]

    @staticmethod
    async def create(user_data: UserInput) -> UserType:
        log.info(f"Creating user {user_data}")

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
        )

        await UserRepository.create(user)

        log.info(f"User created: {user}")

        return convert_user_to_usertype(user)

    @staticmethod
    async def get_by_id(user_id: int) -> UserType:
        log.info(f"Getting user with id {user_id}")

        user = await UserRepository.get_by_id(user_id)

        log.info(f"User: {user}")

        return convert_user_to_usertype(user)

    @staticmethod
    async def update(user_id: int, user_data: UserInput) -> UserType:
        log.info(f"Updating user with id {user_id} to {user_data}")

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
        )
        await UserRepository.update(user_id, user)

        log.info(f"User updated: {user}")

        return convert_user_to_usertype(user)

    @staticmethod
    async def delete(user_id: int) -> bool:
        log.info(f"Deleting user with id {user_id}")

        await UserRepository.delete(user_id)

        log.info(f"User deleted: {user_id}")

        return True
