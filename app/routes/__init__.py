from fastapi import APIRouter
from app.routes.gcb_router import router as gcb_router
from app.routes.redis_router import router as redis_router

api_router = APIRouter(prefix="/v1")

@api_router.get("/ping")
async def ping():
    return {"message": "pong"}

api_router.include_router(gcb_router, prefix="/gcb", tags=["GCB Process"])
api_router.include_router(redis_router, prefix="/dev/redis", tags=["[DEV] Redis"])
