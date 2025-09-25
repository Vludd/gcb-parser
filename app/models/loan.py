from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MLoan(BaseModel):
    subject_role: Optional[str] = None              # роль субъекта
    rest_of_debts: int = 0                          # остаток задолженности
    loan_received_date: datetime | None = None      # дата получения кредита
    loan_ending_date: datetime | None = None        # дата окончания кредита
    payment: int = 0                                # ежемесячный платеж
    debts_days: int = 0                             # дни просрочки
    debts_amount: int = 0                           # сумма просрочки
    have_pledge: bool = False                       # наличие залога
