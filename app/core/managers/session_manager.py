from app.models.sessions import MRedisSession
from datetime import datetime, timezone
import app.config as cfg
import redis.asyncio as aioredis
import json

import logging
logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client

    # async def create_session(self, tg_client_id: str) -> MRedisSession:
    #     """Создать новую сессию и связать с Telegram-клиентом"""
    #     session = MRedisSession(tg_client_id=tg_client_id)
        
    #     # РАЗОБРАТЬСЯ С ЭТИМ КОДОМ

    #     # сохраняем в Redis
    #     key = f"session:{session.id}"
    #     await self.redis.setex(
    #         key,
    #         cfg.REDIS_SESSION_TTL,
    #         session.model_dump_json()
    #     )

    #     # помечаем клиента занятым
    #     await self.redis.set(f"client:{tg_client_id}:session", str(session.id))

    #     logger.debug(f"✅ Created session for TG Client[{tg_client_id}] -> {session.id}")
    #     return session

    async def get_session(self, tl_client_id: str) -> MRedisSession | None:
        """Достать сессию по ID"""
        data = await self.redis.get(f"session:{tl_client_id}")
        if not data:
            return None
        
        data = json.loads(data)
        return MRedisSession.model_validate(data)

    async def get_sessions(self) -> list[MRedisSession]:
        """Получить все активные сессии"""
        keys = await self.redis.keys("session:*")
        
        if not keys:
            return []
        
        sessions = []
        for key in keys:
            raw = await self.redis.hgetall(key) # type: ignore
            if raw:
                data = { 
                    (k.decode() if isinstance(k, bytes) else k): 
                    (v.decode() if isinstance(v, bytes) else v)
                    for k, v in raw.items()
                }
                sessions.append(MRedisSession.model_validate(data))
        logger.debug(f"📊 Total sessions in Redis: {len(sessions)}")
        return sessions

    # async def update_session_step(self, session_id: str, step: str) -> MRedisSession | None:
    #     """Обновить шаг в сессии"""
    #     session = await self.get_session(session_id)
    #     if not session:
    #         return None
    #     session.step = step
    #     session.updated_at = datetime.now(timezone.utc)

    #     await self.redis.setex(
    #         f"session:{session.id}",
    #         cfg.REDIS_SESSION_TTL,
    #         session.model_dump_json()
    #     )
    #     return session

    async def free_session(self, tl_client_id: str):
        """Достать сессию по ID"""
        await self.redis.delete(f"session:{tl_client_id}")
        logger.debug(f"🗑️ Cleared {tl_client_id} session from Redis")
            
    async def clear_all_sessions(self):
        if self.redis:
            keys = await self.redis.keys("session:*")
            
            if keys:
                await self.redis.delete(*keys)
                logger.debug(f"🗑️ Cleared {len(keys)} sessions from Redis")
            else:
                logger.debug("⚠️ No sessions found in Redis")
