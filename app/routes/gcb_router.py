from fastapi import APIRouter, Query, HTTPException
import app.dependencies as dep
from app.core.utils.logger import logger
from app.services.mtproto.actions import send_message, read_last_messages, click_last_button
import app.config as cfg
import asyncio
from app.core.utils.data_formatter import format_phone
from app.services.mtproto.utils.response_parser import parse_loans_data
import app.services.gcb_parser.main as gcb
from app.models.sessions import MRedisSession

router = APIRouter()

@router.post("/initiate")
async def initiate_gcb(
    user_phone:str = Query(..., title="User Phone"),
    iin:str = Query(..., title="User IIN")
):
    tl_client = await dep.WORKERS_MANAGER.get_client(user_phone)
    
    if not tl_client:
        tl_client = await dep.WORKERS_MANAGER.get_available_client()
    
    if not tl_client:
        raise HTTPException(status_code=429, detail="All clients are busy! Retry later")
    
    tl_client_id = tl_client.api_id
    redis_manager = dep.REDIS_MANAGER
    
    new_session = MRedisSession(
        tl_client_id=tl_client_id,
        phone=user_phone,
        iin=iin
    )
    
    session_created = await redis_manager.create_session(new_session)
    
    if not session_created:
        raise HTTPException(status_code=500, detail="Session is not created!")
        
    bot_answer = await gcb.start(tl_client, user_phone, iin)

    return {
        "detail": "Started!",
        "data": {
            "tl_client": tl_client_id,
            "phone": user_phone,
            "bot_answer": bot_answer,
            "session_data": new_session
        }
    }

@router.post("/verify-phone")
async def verify_first_code(
    user_phone:str = Query(..., title="User Phone"),
    code: str = Query(..., title="Verification Code")
):
    tl_client = await dep.WORKERS_MANAGER.get_client(user_phone)
    
    if not tl_client:
        raise HTTPException(status_code=429, detail="All clients are busy! Retry later")
    
    tl_client_id = tl_client.api_id
    if await gcb.try_verify_phone(tl_client, code):    
        return {
            "detail": "Number has been verified! Confirmation code for the collection and processing of personal information was sent to the phone number",
            "data": {
                "tl_client": tl_client_id,
                "phone": user_phone
            }
        }
    
    return {
        "detail": "Incorrect verification code. Retry again!",
        "data": {
            "tl_client": tl_client_id,
            "phone": user_phone
        }
    }

@router.post("/credit-report")
async def gcb_report(
    user_phone:str = Query(..., title="User Phone"),
    code: str = Query(..., title="Second Verification Code")
):
    tl_client = await dep.WORKERS_MANAGER.get_client(user_phone)
    
    if not tl_client:
        raise HTTPException(status_code=429, detail="All clients are busy! Retry later")
    
    tl_client_id = tl_client.api_id
    
    parsed_data = await gcb.try_confirm_collection(tl_client, code)
    
    if not parsed_data:
        raise HTTPException(status_code=429, detail="Incorrect Confirmation code or GCB Server Error")
    
    await dep.SESSION_MANAGER.free_session(str(tl_client_id))
    
    return {
        "detail": f"The collecting information is agreed for {user_phone}",
        "data": {
            "tl_client": tl_client_id,
            "phone": user_phone,
            "credit_history": parsed_data,
            "score": parsed_data.score
        }
    }
    
    # return {
    #     "detail": f"The collecting information is agreed for {user_phone}",
    #     "customer_data": {
    #         "credit_history": [
    #             {
    #                 "role": "Заёмщик",
    #                 "amount": 1485975,
    #                 "received_at": "26.09.2023",
    #                 "expiring_at": "26.06.2029",
    #                 "currency": "KZT",
    #                 "payment": 81583,
    #                 "debt_days": 0,
    #                 "debt_amount": 0,
    #                 "have_pledge": False
    #             }
    #         ],
    #         "score": ""
    #     }
    # }
    
# @router.post("/start-gcb")
# async def start_bot(phone: str):
#     tl_client = await dep.WORKERS_MANAGER.get_available_worker()
    
#     await dep.WORKERS_MANAGER.task_queue.put({"user_id": 12345})
    
#     if not tl_client:
#         raise HTTPException(status_code=429, detail="All clients are busy! Retry later")
    
#     tl_client_id = tl_client.api_id
#     sent = await send_message(tl_client, cfg.GKB_TL_BOT, "/start")
#     await asyncio.sleep(2)
#     bot_response = await read_last_messages(tl_client, cfg.GKB_TL_BOT, 2)
    
#     if not bot_response:
#         raise HTTPException(status_code=404, detail="Messages not found!")
    
#     bot_answer = bot_response[0].text if bot_response[0] and bot_response[0].text else None
    
#     return {
#         "message": "Started!",
#         "detail": {
#             "tl_client": tl_client_id,
#             "bot_message": bot_answer
#         }
#     }
    
# print(f"Contracts: {info.contracts}")
# for idx, loan in enumerate(info.loans, start=1):
#     print(f"\nLoan {idx}:")
#     print(f"- Amount: {loan.remaining_amount} {loan.currency}")
#     print(f"- Loan term: {loan.loan_term}")
#     print(f"- Monthly payment: {loan.monthly_payment} {loan.currency}")
#     print(f"- Current debt days: {loan.current_debt_days}")
#     print(f"- Debt amount: {loan.debt_amount}")
#     print(f"- Have pledge: {'Yes' if loan.have_pledge else 'No'}")

# Бот: ✅ Активные договоры - 2
# Бот: 🔹Кредитор 1 по состоянию на 27.07.2025:
# ▫️ Роль субъекта: Заёмщик
# ▫️ Остаток задолженности: 1 492 984 KZT
# ▫️ Срок кредита: 26.09.2023-26.06.2029
# ▫️ Платеж: 81 097 KZT
# ▫️ Текущая просрочка: 0 дней
# ▫️ Сумма просрочки: 0 KZT
# ▫️ Наличие залога: отсутствует
# Бот: 🔹Кредитор 2 по состоянию на 25.07.2025:
# ▫️ Роль субъекта: Заёмщик
# ▫️ Остаток задолженности: 76 781 KZT
# ▫️ Срок кредита: 14.12.2024-14.12.2026
# ▫️ Платеж: 36 849 KZT
# ▫️ Текущая просрочка: 0 дней
# ▫️ Сумма просрочки: 0 KZT
# ▫️ Наличие залога: отсутствует
