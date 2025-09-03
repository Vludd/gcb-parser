from app.models.sessions import MRedisSession
from app.core.utils.logger import logger

sessions = []

async def create_session() -> MRedisSession:
    tg_client_id = "client_1"
    created_session = MRedisSession(tg_client_id=tg_client_id)
    logger.debug(f" Created session data for TG Client[{tg_client_id}]: \n{created_session.model_dump()}")
    sessions.append(created_session)
    return created_session

async def get_sessions() -> list[MRedisSession]:
    logger.debug(f" Total sessions: {len(sessions)}")
    return sessions

async def get_session(session_id: str) -> MRedisSession | None:
    if not sessions:
        return None
    
    finded_session = None;
    for session in sessions:
        if str(session.id) == session_id:
            finded_session = session
    
    if not finded_session:
        return None
    
    return finded_session
