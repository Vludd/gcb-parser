from fastapi import APIRouter, Query, HTTPException
import app.core.managers.session_manager as redis

router = APIRouter()

@router.post("/start-gkb")
async def start_gkb(user_phone:str = Query(..., title="User Phone")):
    
    session = await redis.create_session()
    # session = None
    
    if not session:
        raise HTTPException(status_code=500, detail="An error occurred while creating session!")
    
    # запуск клиента телеграм
    # ассинхронное выполнение прескоринга
    
    return {"detail": f"Session created for {user_phone}", "session_id": session.id}