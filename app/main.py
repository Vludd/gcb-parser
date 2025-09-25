import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import api_router
import app.config as cfg
import app.dependencies as dep

import logging
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await dep.init()
    
    if not dep.SESSION_MANAGER:
        logger.error("❌ SESSION_MANAGER not initialized!")
        
    if not dep.WORKERS_MANAGER:
        logger.error("❌ WORKERS_MANAGER not initialized!")
        
    if not dep.REDIS_CLIENT:
        logger.error("❌ REDIS_CLIENT not initialized!")
    
    yield
    await dep.WORKERS_MANAGER.shutdown()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.ALLOW_ORIGINS,
    allow_credentials=cfg.ALLOW_CREDENTIALS,
    allow_methods=cfg.ALLOW_METHODS,
    allow_headers=cfg.ALLOW_HEADERS,
)

app.include_router(api_router, prefix="/api")
    
async def main():
    uvicorn.run(cfg.API_MAIN_MODULE, host=cfg.API_HOST, port=cfg.API_PORT, reload=cfg.LOGGER_LEVEL == 'DEBUG')
