import asyncio
from telethon import TelegramClient, events, Button
import app.config as cfg
from app.core.utils.logger import logger

API_KEYS = cfg.API_KEYS

clients = [
    TelegramClient(f'sessions/tl_client_{API_KEYS[i].api_id}', api_id=API_KEYS[i].api_id, api_hash=API_KEYS[i].api_hash)
    for i in range(len(API_KEYS))
]

logger.debug(f" Created Telegram sessions: {[c.session.filename for c in clients]}")

# task_queue = asyncio.Queue()
