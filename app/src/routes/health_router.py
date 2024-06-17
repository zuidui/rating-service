from fastapi import APIRouter

health_router = APIRouter()


@health_router.get(
    "/health", tags=["Sanity check"], responses={200: {"description": "Health check"}}
)
async def health_check():
    return {"status": "ok"}
