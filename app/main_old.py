import asyncio
from telethon import TelegramClient, events, Button
import app.config as cfg

api_id = cfg.APP_API_ID
api_hash = cfg.APP_API_HASH
bot_username = cfg.GKB_TL_BOT

client = TelegramClient('mtproto_session', api_id, api_hash)

last_event_with_buttons = None

def show_event(event, label="💬"):
    global last_event_with_buttons
    print(f'\n{label}: {event.raw_text}')

    if event.buttons:
        print("┌─[Buttons]:")
        flat_buttons = []
        for row in event.buttons:
            for button in row:
                flat_buttons.append(button)
                print(f"[{len(flat_buttons)-1}] {button.text}")
        last_event_with_buttons = event
    else:
        last_event_with_buttons = None

    print("> ", end='', flush=True)

async def message_listener():
    async for event in client.iter_messages(bot_username, reverse=True, limit=1):
        show_event(event)

    @client.on(events.NewMessage(from_users=bot_username))
    async def handler(event):
        show_event(event, "[MKB-Bot]")

    # @client.on(events.MessageEdited(from_users=bot_username))
    # async def edited(event):
    #     show_event(event, "[MKB-Bot-Edited]")

async def repl():
    print("MKB-Parser Started! Enter the message or /start. Reply button on '/btn <number>'")

    while True:
        msg = await asyncio.to_thread(input, "> ")
        if msg.strip().lower() == "/exit":
            break
        elif msg.startswith("/btn"):
            try:
                _, index = msg.split(maxsplit=1)
                index = int(index)
                if last_event_with_buttons:
                    flat_buttons = sum(last_event_with_buttons.buttons, [])
                    if 0 <= index < len(flat_buttons):
                        await last_event_with_buttons.click(text=flat_buttons[index].text)
                    else:
                        print("Unknown a button number.")
                else:
                    print("Active buttons not found.")
            except Exception as e:
                print(f"Button error: {e}")
        else:
            await client.send_message(bot_username, msg)
    
async def main():
    await client.start()
    asyncio.create_task(message_listener())
    await repl()
    await client.disconnect()
    print("Session stoped")

if __name__ == "__main__":
    asyncio.run(main())