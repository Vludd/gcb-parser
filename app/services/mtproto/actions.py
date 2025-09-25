from telethon import TelegramClient
import app.config as cfg
bot_username = cfg.GKB_TL_BOT
from app.core.utils.logger import logger

async def send_message(
    client: TelegramClient,
    chat_id,
    message: str = "Test Message"
):
    """Отправить сообщение в указанный чат через переданный клиент"""
    if not chat_id:
        logger.warning("Chat ID not found")
        return None
    logger.debug(f"Sending message: {message}")
    return await client.send_message(chat_id, message)

async def read_last_messages(
    client: TelegramClient,
    chat_id,
    search_limit: int = 1
):
    """Прочитать последние сообщения с лимитом в search_limit"""
    if not chat_id:
        logger.warning("Chat ID not found")
        return None
    
    logger.debug(f"Searching messages count: {search_limit}")
    messages = []
    async for msg in client.iter_messages(chat_id, limit=search_limit):
        messages.append(msg)
        
    if messages:
        texts = " | ".join([str(m.text) for m in messages if m.text])
        logger.debug(f"Founded messages: {texts}")
    else:
        logger.debug("Founded messages: None")
        
    return messages

async def click_last_button(
    client: TelegramClient, 
    chat_id,
    button_text: str = "",
    button_index: int = 0,
    search_limit: int = 10
):
    """
    Найти последнее сообщение с кнопками и нажать на кнопку по тексту или индексу.
    """
    if not chat_id:
        logger.warning("Chat ID not found")
        return None
    
    messages = await read_last_messages(client, chat_id, search_limit)
    
    if not messages:
        logger.warning("Messages not found")
        return None
    
    for msg in messages:
        if not msg.buttons:
            continue
        
        flat_buttons = sum(msg.buttons, [])
        
        if button_text is not None:
            for btn in flat_buttons:
                if btn.text == button_text:
                    return await msg.click(text=btn.text)
        elif button_index is not None and 0 <= button_index < len(flat_buttons):
            return await msg.click(text=flat_buttons[button_index].text)
        
        break
    return None
