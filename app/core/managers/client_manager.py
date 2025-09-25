import asyncio
from telethon import TelegramClient
import app.config as cfg

import logging
logger = logging.getLogger(__name__)

from app.models.tl_app_data import MTelegramAppData
import app.dependencies as dep

class ClientsManager:
    def __init__(self, api_keys: list[MTelegramAppData]):
        self.api_keys: list[MTelegramAppData] = api_keys
        self.telegram_clients: list[TelegramClient] = []
        self.task_queue = asyncio.Queue()
        self.workers = []
        self.client_busy: dict[TelegramClient, bool] = {}

    async def init_clients(self):
        """Создаём клиентов Telethon"""
        logger.info(f"🔑 Initializing Telethon clients...")
        # api_keys = self.api_keys
        api_keys = await self.use_my_sessions() # фильтрация от других сессий
        
        created_count = 0
        for key in api_keys:
            session_name = f"sessions/tl_client_{key.api_id}"
            
            client = TelegramClient(
                session_name,
                api_id=key.api_id,
                api_hash=key.api_hash
            )
            
            self.telegram_clients.append(client)
            
            created_count += 1
            logger.debug(f"👾 Created Telethon client: {client.api_id} ({created_count}/{len(self.api_keys)})")

        logger.info("✅ Initialization complete!")
        
    async def exclude_my_sessions(self):
        api_list = self.api_keys
        total_keys = len(api_list)
        logger.debug(f"👾 Total APIs: {total_keys}")

        removed = api_list[:2]
        kept = api_list[2:]

        for i, deleted in enumerate(removed):
            logger.debug(f"🗑️ Deleted API Credential [{i}]: {deleted.api_id} (removed {i+1}/2)...")
            
        return kept
    
    async def use_my_sessions(self):
        api_list = self.api_keys
        total_keys = len(api_list)
        logger.debug(f"👾 Total APIs: {total_keys}")
        
        api_list = api_list[:2]
        
        removed_count = total_keys - len(api_list)
        logger.debug(f"🗑️ Deleted {removed_count} API credentials, kept first 2")
            
        return api_list

    async def prepare_client(self, client: TelegramClient):
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
    
                        pass
                    except Exception as e:
                        logger.error(f"Error in {client.session.filename}: {e}") # type: ignore
                    finally:
                        # self.client_busy[client] = False
                        self.task_queue.task_done()

        except Exception as e:
            logger.error(f"❌ Worker crashed for {client.session.filename}: {e}") # type: ignore

    async def start_clients(self):
        """Запуск воркеров последовательно"""
        workers_count = 0
        for client in self.telegram_clients:
            logger.debug(f"🚀 Starting worker for {client.session.filename}") # type: ignore
            task = asyncio.create_task(self.prepare_client(client))
            self.workers.append(task)
            workers_count += 1
            logger.debug(f"👾 Worker started for client - {client.api_id} ({workers_count}/{len(self.telegram_clients)})")
            await asyncio.sleep(1)
        
        logger.info(f"👾 Initialization completed! Runned workers: {workers_count}")
        
    async def get_available_client(self) -> TelegramClient | None:
        """Возвращает свободного клиента или None, если все заняты"""
        redis_manager = dep.REDIS_MANAGER
        
        if not redis_manager:
            return None
        
        for client in self.telegram_clients:
            if not await redis_manager.get_session(str(client.api_id)):
                return client
        
        return None
    
    async def get_client(self, phone: str):
        redis_manager = dep.REDIS_MANAGER
        
        if not redis_manager:
            return None
        
        for client in self.telegram_clients:
            redis_session = await redis_manager.get_session(str(client.api_id))
                
            if redis_session:
                if hasattr(redis_session, "phone") and redis_session.phone == phone:
                    return client
        
        return None

    async def stop_clients(self):
        """Остановка всех воркеров"""
        for _ in self.telegram_clients:
            await self.task_queue.put(None)
        await asyncio.gather(*self.workers)
        logger.debug("🛑 Workers stopped")

    async def run(self):
        """Запуск менеджера"""
        await self.init_clients()
        await self.start_clients()

    async def shutdown(self):
        """Чистое завершение"""
        await self.stop_clients()

