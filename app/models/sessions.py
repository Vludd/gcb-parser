from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta

from app.models.user import MUser
import app.config as cfg

class MRedisSession(BaseModel):
    id: UUID = Field(default_factory=uuid4)                                             # ID сессии
    tg_client_id: Optional[str]                                                         # ID клиента Telegram
    step: str = "start"                                                                 # текущий шаг клиента
    user_data: MUser = MUser()                                                          # данные клиента
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))    # дата создания сессии
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))    # дата обновления сессии
    expires_at: datetime = Field(default_factory=lambda: 
        datetime.now(timezone.utc) + timedelta(seconds=cfg.REDIS_SESSION_TTL)           # дата авто-удаления сессии
    )
    