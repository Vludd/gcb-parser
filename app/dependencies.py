from app.core.managers.redis_manager import RedisManager
from app.core.managers.session_manager import SessionManager
from app.core.managers.workers_manager import WorkersManager
import app.config as cfg

API_KEYS = cfg.API_KEYS

REDIS_MANAGER = RedisManager()
SESSION_MANAGER = None
WORKERS_MANAGER = None
REDIS_CLIENT = None

async def init():
    global SESSION_MANAGER, WORKERS_MANAGER, REDIS_CLIENT
    
    REDIS_CLIENT = await REDIS_MANAGER.connect()

    WORKERS_MANAGER = WorkersManager(API_KEYS)
    await WORKERS_MANAGER.run()

    SESSION_MANAGER = SessionManager(REDIS_CLIENT)
