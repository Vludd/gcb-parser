import asyncio
import redis.asyncio as aioredis

import app.config as cfg
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

