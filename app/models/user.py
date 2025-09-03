from pydantic import BaseModel, Field
from typing import Optional
from .loan import LoanModel

class MUser(BaseModel):
    iin: Optional[str] = None                           # иин клиента
    phone: Optional[str] = None                         # номер клиента
    codes: list[str] = []                               # коды, полученные по смс
    active_loans: list[LoanModel] = [LoanModel()]       # список активных кредитов
    score: Optional[str] = None                         # предварительный пре-скоринг
    