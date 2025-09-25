import app.config as cfg
import app.core.utils.data_formatter as freader
# import app.core.utils.data_formatter as re
import re

class LoanModel:
    def __init__(
        self,
        subject_role: str = '',
        remaining_amount: int = 0,
        currency: str = "KZT",
        loan_term: str = "",
        monthly_payment: int = 0,
        current_debt_days: int = 0,
        debt_amount: int = 0,
        have_pledge: bool = False
    ):
        self.subject_role = subject_role
        self.remaining_amount = remaining_amount
        self.currency = currency
        self.loan_term = loan_term
        self.monthly_payment = monthly_payment
        self.current_debt_days = current_debt_days
        self.debt_amount = debt_amount
        self.have_pledge = have_pledge

class InfoModel:
    def __init__(
        self,
        contracts: int = 0,
        loans: list[LoanModel] = [],
        score: int = 0
    ):
        self.contracts = contracts
        self.loans = loans if loans is not None else []
        self.score = score

def parse_loans_data(bot_messages: list[str]) -> InfoModel | None:
    if not bot_messages:
        return None
    
    contracts = 0
    loans = []

    # Парсим количество договоров
    for msg in bot_messages:
        match_contracts = re.search(r"Активные договоры\s*-\s*(\d+)", msg)
        if match_contracts:
            contracts = int(match_contracts.group(1))

        # Парсим кредиты
        if "Кредитор" in msg:
            # Роль субъекта
            role_match = re.search(r"Роль субъекта:\s*([^\n]+)", msg)
            subject_role = role_match.group(1).strip() if role_match else ""
            
            # Остаток задолженности
            amount_match = re.search(r"Остаток задолженности:\s*([\d\s]+)\s*(KZT)", msg)
            remaining_amount = int(amount_match.group(1).replace(" ", "")) if amount_match else 0
            currency = amount_match.group(2) if amount_match else "KZT"

            # Срок кредита
            term_match = re.search(r"Срок кредита:\s*([\d\.]+)-([\d\.]+)", msg)
            loan_term = f"{term_match.group(1)}-{term_match.group(2)}" if term_match else ""

            # Платеж
            payment_match = re.search(r"Платеж:\s*([\d\s]+)\s*(KZT)", msg)
            monthly_payment = int(payment_match.group(1).replace(" ", "")) if payment_match else 0

            # Текущая просрочка
            debt_days_match = re.search(r"Текущая просрочка:\s*(\d+)\s*дней", msg)
            current_debt_days = int(debt_days_match.group(1)) if debt_days_match else 0

            # Сумма просрочки
            debt_amount_match = re.search(r"Сумма просрочки:\s*([\d\s]+)\s*(KZT)", msg)
            debt_amount = int(debt_amount_match.group(1).replace(" ", "")) if debt_amount_match else 0

            # Наличие залога
            pledge_match = re.search(r"Наличие залога:\s*(отсутствует|есть)", msg)
            have_pledge = pledge_match.group(1) == "есть" if pledge_match else False

            loans.append(
                LoanModel(
                    subject_role=subject_role,
                    remaining_amount=remaining_amount,
                    currency=currency,
                    loan_term=loan_term,
                    monthly_payment=monthly_payment,
                    current_debt_days=current_debt_days,
                    debt_amount=debt_amount,
                    have_pledge=have_pledge
                )
            )

    return InfoModel(contracts=contracts, loans=loans)

def parse_score(bot_messages: list[str]) -> int:
    for msg in bot_messages:
        match = re.search(r"скорбалл\s*=\s*(\d+)", msg, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0