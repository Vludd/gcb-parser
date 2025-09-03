from pydantic import BaseModel
from uuid import UUID, uuid4

class MTelegramClient(BaseModel):
    id: UUID = uuid4()                          # ID клиента Telegram
    api_key: str                                # API ключ клиента Telegram
    api_hash: str                               # API хэш клиента Telegram
    app_title: str                              # название приложения
    app_short: str                              # короткое название приложения
    isAvailable: bool = True                    # статус доступности клиента
    isBusy: bool = False                        # статус занятости клиента
    