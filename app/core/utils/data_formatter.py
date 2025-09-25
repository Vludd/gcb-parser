import re
from enum import Enum

class PhoneFormat(Enum):
    PLAIN = 1,
    PLUS = 2

import re

def format_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("8"):
        digits = "7" + digits[1:]
    elif digits.startswith("7"):
        pass
    elif digits.startswith("007"):
        digits = "7" + digits[3:]
    elif digits.startswith("77"):
        pass
    return digits[-11:]


def get_only_number(text: str) -> int:
    match = re.search(r'\d+', text)
    if match:
        number = int(match.group())
        return number

    return 0

def parse_kzt_amount(text: str):
    """Парсит сумму вида '1 492 984 KZT' или '0 KZT' в (int, str)"""
    match = re.search(r"([\d\s]+)\s*(KZT)", text)
    if match:
        amount = int(match.group(1).replace(" ", ""))
        currency = match.group(2)
        return amount, currency
    return 0, "KZT"

def parse_days(text: str):
    """Парсит строку '0 дней' и возвращает int"""
    match = re.search(r"(\d+)\s*дн", text)
    return int(match.group(1)) if match else 0