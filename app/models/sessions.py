from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta

from app.models.customer import MCustomer
import app.config as cfg

class MRedisSession(BaseModel):
    tl_client_id: int
    phone: str                                                                 # текущий шаг клиента
    iin: str                                                                 # текущий шаг клиента
