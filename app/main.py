import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import api_router
from app.core.managers.redis_manager import RedisManager
from app.core.utils.logger import logger
import app.config as cfg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.ALLOW_ORIGINS,
    allow_credentials=cfg.ALLOW_CREDENTIALS,
    allow_methods=cfg.ALLOW_METHODS,
    allow_headers=cfg.ALLOW_HEADERS,
)

app.include_router(api_router, prefix="/api")

async def initialize():
    redis_manager = RedisManager()
    import app.core.managers.workers_manager
    await redis_manager.connect()
    
    logger.debug("Server is starting with Middlwares..." )
    logger.debug(f"ALLOW_ORIGINS: {cfg.ALLOW_ORIGINS}")
    logger.debug(f"ALLOW_CREDENTIALS: {cfg.ALLOW_CREDENTIALS}")
    logger.debug(f"ALLOW_METHODS: {cfg.ALLOW_METHODS}")
    logger.debug(f"ALLOW_HEADERS: {cfg.ALLOW_HEADERS}")

async def main():
    await initialize()
    uvicorn.run(cfg.API_MAIN_MODULE, host=cfg.API_HOST, port=cfg.API_PORT, reload=cfg.LOGGER_LEVEL == 'DEBUG')
