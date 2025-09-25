from app.services.mtproto.actions import send_message, read_last_messages, click_last_button
import app.config as cfg
import asyncio
from app.core.utils.data_formatter import format_phone
from app.services.mtproto.utils.response_parser import parse_loans_data, parse_score
from app.core.utils.logger import logger
import re
import time

async def start(tl_client, user_phone: str, iin: str):
    formatted_phone = format_phone(user_phone)
    
    if not tl_client:
        logger.error("Telegram Client is None")
        return None
    
    logger.debug("Sending \"/stop\" command...")
    
    await send_message(tl_client, cfg.GKB_TL_BOT, "/stop")
    await asyncio.sleep(.5)
    logger.debug("Sending \"/start\" command...")
    await send_message(tl_client, cfg.GKB_TL_BOT, "/start")
    await asyncio.sleep(2)
    logger.debug("Sending \"Русский\" button text...")
    await click_last_button(tl_client, cfg.GKB_TL_BOT, button_text="Русский")
    await asyncio.sleep(1)
    logger.debug("Sending \"[iin]\" data...")
    await send_message(tl_client, cfg.GKB_TL_BOT, iin)
    await asyncio.sleep(0.5)
    logger.debug("Sending \"[phone]\" data...")
    await send_message(tl_client, cfg.GKB_TL_BOT, formatted_phone)
    await asyncio.sleep(2)
    
    logger.debug("Parsing data...")
    bot_response = await read_last_messages(tl_client, cfg.GKB_TL_BOT, 2)
    
    if not bot_response:
        logger.error("Messages not found!")
        return None
    
    return bot_response[0].text if bot_response[0] and bot_response[0].text else None

async def try_verify_phone(tl_client, code: str):
    await send_message(tl_client, cfg.GKB_TL_BOT, code)
    await asyncio.sleep(1)
    
    bot_response = await read_last_messages(tl_client, cfg.GKB_TL_BOT, 2)
    
    if not bot_response:
        logger.error("Messages not found!")
        return False
    
    bot_answer = bot_response[0].text if bot_response[0] and bot_response[0].text else None
    
    if bot_answer and re.search(r"код неправильный, попробуйте снова", bot_answer, re.IGNORECASE):
        logger.info("Incorrect code")
        return False
    
    return True

async def try_confirm_collection(tl_client, code: str):
    await send_message(tl_client, cfg.GKB_TL_BOT, code)
    await asyncio.sleep(3)
    
    bot_response = await read_last_messages(tl_client, cfg.GKB_TL_BOT, 2)
    
    if not bot_response:
        logger.error("Messages not found!")
        return None
    
    bot_answer = bot_response[0].text if bot_response[0] and bot_response[0].text else None
    
    if bot_answer and re.search(r"код неправильный, попробуйте снова", bot_answer, re.IGNORECASE):
        logger.info("Incorrect code")
        return None
    
    bot_response = await read_last_messages(tl_client, cfg.GKB_TL_BOT, 5)
    
    if not bot_response:
        logger.error("Messages not found!")
        return None
    
    bot_answers = [response.text for response in bot_response]
    bot_answers = delete_list_items(bot_answers, 2, True)
    
    customer_info = parse_loans_data(bot_answers)
    
    if not customer_info:
        logger.error("Data is unknown!")
        return None
        
    await send_message(tl_client, cfg.GKB_TL_BOT, "/menu")
    await asyncio.sleep(1)
    await send_message(tl_client, cfg.GKB_TL_BOT, "Кредитование")
    await asyncio.sleep(1)
    await send_message(tl_client, cfg.GKB_TL_BOT, "Скорбалл")
    await asyncio.sleep(2)
    
    bot_response = await read_last_messages(tl_client, cfg.GKB_TL_BOT, 5)
    
    if not bot_response:
        logger.error("Messages not found!")
        return customer_info
    
    bot_answers = [response.text for response in bot_response]
    bot_answers = delete_list_items(bot_answers, 3, True)
    
    score = parse_score(bot_answers)
    
    customer_info.score = score
    return customer_info

def delete_list_items(items: list, count: int = 1, reverse_first: bool = False):
    if not items:
        return []
    
    if reverse_first:
        items.reverse()
    
    for i in range(count):
        items.pop()
        
    return items

async def wait_for_message(client, chat_id, pattern, timeout=15, check_limit=5):
    start = time.time()
    while time.time() - start < timeout:
        messages = await read_last_messages(client, chat_id, check_limit)
        
        if not messages:
            return None
        
        for msg in messages:
            if msg and re.search(pattern, msg, re.IGNORECASE):
                return msg
        await asyncio.sleep(0.5)
    return None