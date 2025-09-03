from fastapi import APIRouter, Query, HTTPException
import app.core.managers.session_manager as redis

router = APIRouter()

@router.get("/sessions")
async def get_redis_sessions():
    sessions = await redis.get_sessions()
    
    if not sessions:
        raise HTTPException(status_code=404, detail="Sessions not found!")
        
    return {"sessions": sessions}
    
@router.get("/session")
async def get_session_info(session_id: str):
    session = await redis.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found!")
        
    return {"session": session}
    
@router.post("/create-session")
async def create_redis_session():
    session = await redis.create_session()
    
    if not session:
        raise HTTPException(status_code=500, detail="An error occurred while creating session!")
    
    return {"message": "Session created!", "session_id": session.id}