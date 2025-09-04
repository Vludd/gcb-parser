import asyncio
from telethon import TelegramClient, events, Button
import app.config as cfg

import logging
logger = logging.getLogger(__name__)

from app.models.app_data import MAppData

class WorkersManager:
    def __init__(self, api_keys: list[MAppData]):
        self.api_keys: list[MAppData] = api_keys
        self.clients: list[TelegramClient] = []
        self.task_queue = asyncio.Queue()
        self.workers = []

    async def init_clients(self):
        """Создаём клиентов Telethon"""
        logger.info(f"🔑 Initializing Telethon clients...")
        created_count = 0
        for key in self.api_keys:
            session_name = f"sessions/tl_client_{key.api_id}"
            
            client = TelegramClient(
                session_name,
                api_id=key.api_id,
                api_hash=key.api_hash
            )
            
            self.clients.append(client)
            created_count += 1
            logger.debug(f"👾 Created Telethon client: {client.api_id} ({created_count}/{len(self.api_keys)})")

        logger.info("✅ Initialization complete!")

    async def worker(self, client: TelegramClient):
        logger.debug(f"🔄 Preparing client {client.api_id}...")
        try:
            await client.connect()

            if not await client.is_user_authorized():
                logger.debug(f"🔐 Client {client.api_id} not authorized, starting verification...")
                try:
                    client.start()
                    logger.debug(f"✅ Client {client.api_id} authorized successfully")
                except Exception as e:
                    logger.error(f"❌ Failed verification for {client.api_id}: {e}")
                    return
            else:
                logger.debug(f"✅ Client {client.api_id} already authorized")

            async with client:
                logger.debug(f"🌐 Client {client.api_id} connected to Telegram servers")

                while True:
                    task = await self.task_queue.get()
                    if task is None:
                        break
                    try:
                        user_id = task["user_id"]
                        result = await client.get_entity(user_id)
                        logger.info(f"{client.session.filename} -> {result}") # type: ignore
                    except Exception as e:
                        logger.error(f"Error in {client.session.filename}: {e}") # type: ignore
                    self.task_queue.task_done()

        except Exception as e:
            logger.error(f"❌ Worker crashed for {client.session.filename}: {e}") # type: ignore

    async def start_workers(self):
        """Запуск воркеров последовательно"""
        workers_count = 0
        for client in self.clients:
            logger.debug(f"🚀 Starting worker for {client.session.filename}") # type: ignore
            task = asyncio.create_task(self.worker(client))
            self.workers.append(task)
            workers_count += 1
            logger.debug(f"👾 Worker started for client - {client.api_id} ({workers_count}/{len(self.clients)})")
            await asyncio.sleep(1)
        
        logger.info(f"👾 Initialization completed! Runned workers: {workers_count}")

    async def stop_workers(self):
        """Остановка всех воркеров"""
        for _ in self.clients:
            await self.task_queue.put(None)
        await asyncio.gather(*self.workers)
        logger.debug("🛑 Workers stopped")

    async def run(self):
        """Запуск менеджера"""
        await self.init_clients()
        await self.start_workers()

    async def shutdown(self):
        """Чистое завершение"""
        await self.stop_workers()

