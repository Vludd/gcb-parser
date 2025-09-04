from fastapi import APIRouter
from app.routes.gkb_router import router as gkb_router
from app.routes.redis_router import router as redis_router
from app.routes.telethon_router import router as telethon_router

api_router = APIRouter(prefix="/v1")

@api_router.get("/ping")
async def ping():
    return {"message": "pong"}

api_router.include_router(gkb_router, prefix="/gkb", tags=["GKB"])
api_router.include_router(telethon_router, prefix="/telethon", tags=["Telethon"])

api_router.include_router(redis_router, prefix="/dev/redis", tags=["[DEV] Redis"])
