from fastapi import APIRouter

from demo.internal.logger import logger_config

router = APIRouter()

log = logger_config(__name__)


@router.get("/users", tags=["users"])
async def get_users():
    log.debug("Received GET request")
    return [{"username": "johndoe"}, {"username": "janedoe"}]


@router.get("/users/{username}", tags=["users"])
async def get_user(username: str):
    log.debug(f"Received GET request for {username}")
    return {"username": username}
