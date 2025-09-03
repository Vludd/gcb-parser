from fastapi import APIRouter
from .gkb_router import router as gkb_router
from .redis_router import router as redis_router

api_router = APIRouter(prefix="/v1")

@api_router.get("/ping")
async def ping():
    return {"message": "pong"}

api_router.include_router(gkb_router, prefix="/gkb", tags=["GKB"])

api_router.include_router(redis_router, prefix="/dev/redis", tags=["[DEV] Redis"])
