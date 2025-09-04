from fastapi import APIRouter, Query, HTTPException
import app.core.managers.session_manager as redis

router = APIRouter()

@router.post("/register-client")
async def register_client(
    api_id: int = Query(..., title="App API ID"),
    api_hash: str = Query(..., title="App API Hash")
    ):
    return {"detail": f"Client [{api_id}] registered, but need verification..."}

@router.post("/verify-client")
async def verify_client(api_id: int = Query(..., title="App API ID"), code: int = Query(..., title="Code verification")):
    return {"detail": f"Client [{api_id}] registered successfully!"}