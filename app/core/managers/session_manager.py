from app.models.sessions import MRedisSession
from datetime import datetime, timezone
import app.config as cfg
import json

import logging
logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def create_session(self, tg_client_id: str) -> MRedisSession:
        """Создать новую сессию и связать с Telegram-клиентом"""
        session = MRedisSession(tg_client_id=tg_client_id)

        # сохраняем в Redis
        key = f"session:{session.id}"
        await self.redis.setex(
            key,
            cfg.REDIS_SESSION_TTL,
            session.model_dump_json()
        )

        # помечаем клиента занятым
        await self.redis.set(f"client:{tg_client_id}:session", str(session.id))

        logger.debug(f"✅ Created session for TG Client[{tg_client_id}] -> {session.id}")
        return session

    async def get_session(self, session_id: str) -> MRedisSession | None:
        """Достать сессию по ID"""
        data = await self.redis.get(f"session:{session_id}")
        if not data:
            return None
        
        data = json.loads(data)
        return MRedisSession.model_validate(data)

    async def get_sessions(self) -> list[MRedisSession]:
        """Получить все активные сессии"""
        keys = await self.redis.keys("session:*")
        sessions = []
        for key in keys:
            raw = await self.redis.get(key)
            if raw:
                data = json.loads(raw)
                sessions.append(MRedisSession.model_validate(data))
        logger.debug(f"📊 Total sessions in Redis: {len(sessions)}")
        return sessions

    async def update_session_step(self, session_id: str, step: str) -> MRedisSession | None:
        """Обновить шаг в сессии"""
        session = await self.get_session(session_id)
        if not session:
            return None
        session.step = step
        session.updated_at = datetime.now(timezone.utc)

        await self.redis.setex(
            f"session:{session.id}",
            cfg.REDIS_SESSION_TTL,
            session.model_dump_json()
        )
        return session

    async def free_client(self, tg_client_id: str):
        """Освободить клиента"""
        await self.redis.delete(f"client:{tg_client_id}:session")
        logger.debug(f"🟢 Client {tg_client_id} is now free")
