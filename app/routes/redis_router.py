from fastapi import APIRouter, Query, HTTPException
import app.dependencies as dep

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/sessions")
async def get_redis_sessions():
    if not dep.SESSION_MANAGER:
        logger.error("SESSION_MANAGER not initialized!")
        
    sessions = await dep.SESSION_MANAGER.get_sessions()
    
    if not sessions:
        raise HTTPException(status_code=404, detail="Sessions not found!")
        
    return {"sessions": sessions}
    
@router.get("/session")
async def get_session_info(session_id: str):
    session = await dep.SESSION_MANAGER.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found!")
        
    return {"session": session}
    
@router.post("/create-session")
async def create_redis_session(tg_client_id: str = Query(..., title="Telegram Client ID")):
    session = await dep.SESSION_MANAGER.create_session(tg_client_id)
    
    if not session:
        raise HTTPException(status_code=500, detail="An error occurred while creating session!")
    
    return {"message": "Session created!", "session_id": session.id}