import asyncio
import redis.asyncio as aioredis

import app.config as cfg
from app.models.sessions import MRedisSession
import logging
logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self, host=cfg.REDIS_HOST, port=int(cfg.REDIS_PORT), db=0, password=cfg.REDIS_PASSWORD):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None

    async def connect(self):
        """Try connect to Redis"""
        if self.client is None:
            self.client = aioredis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
            
            try:
                pong = await self.client.ping()
                if pong:
                    logger.info("✅ Redis connected successfully!")
                    return self.client
            except Exception as e:
                logger.error(f"❌ Redis connection error: {e}")
                self.client = None
                
        return None
    
    async def create_session(self, session: MRedisSession):
        """
        Сохраняет сессию в Redis.
        Ключ: session:{session_id}
        Значение: сериализованный словарь сессии
        """
        if not self.client:
            self.client = await self.connect()
            
        key = f"session:{session.tl_client_id}"
        value = session.model_dump() if hasattr(session, "model_dump") else session.__dict__
        
        try:
            await self.client.hmset(key, value) # type: ignore
            
            logger.info(f"📝 Сессия {session.tl_client_id} сохранена в Redis")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка при сохранении сессии: {e}")
            return False
        
    async def get_session(self, session_id: str):
        """
        Получает данные сессии из Redis по session_id.
        Возвращает экземпляр MRedisSession или None, если не найдено.
        """
        if not self.client:
            self.client = await self.connect()
        key = f"session:{session_id}"
        
        try:
            data = await self.client.hgetall(key) # type: ignore
            
            if data:
                return MRedisSession(**data)
            else:
                logger.info(f"ℹ️ Сессия {session_id} не найдена в Redis")
                return None
        except Exception as e:
            logger.error(f"❌ Ошибка при получении сессии: {e}")
            return None

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            await self.client.connection_pool.disconnect()
            self.client = None
            logger.info("🛑 Redis disconnected")

    async def restart(self):
        """Restart Redis connection"""
        logger.info("🔄 Restarting Redis connection...")
        await self.disconnect()
        await self.connect()
