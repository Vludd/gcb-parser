from app.core.managers.redis_manager import RedisManager
from app.core.managers.session_manager import SessionManager
from app.core.managers.client_manager import ClientsManager

import app.config as cfg

API_KEYS = cfg.API_KEYS

REDIS_MANAGER = RedisManager()
SESSION_MANAGER = None
WORKERS_MANAGER = None
REDIS_CLIENT = None

async def init():
    global SESSION_MANAGER, WORKERS_MANAGER, REDIS_CLIENT
    
    if REDIS_MANAGER:
        REDIS_CLIENT = await REDIS_MANAGER.connect()
    
    WORKERS_MANAGER = ClientsManager(API_KEYS)
    
    if WORKERS_MANAGER:
        await WORKERS_MANAGER.run()
    
    if REDIS_CLIENT:
        SESSION_MANAGER = SessionManager(REDIS_CLIENT)
