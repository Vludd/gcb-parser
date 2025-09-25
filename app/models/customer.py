from pydantic import BaseModel, Field
from typing import Optional
from .loan import MLoan

class MCustomer(BaseModel):
    iin: Optional[str] = None                           # иин клиента
    phone: Optional[str] = None                         # номер клиента
    codes: list[str] = []                               # коды, полученные по смс
    active_loans: list[MLoan] = [MLoan()]       # список активных кредитов
    score: Optional[str] = None                         # предварительный пре-скоринг
