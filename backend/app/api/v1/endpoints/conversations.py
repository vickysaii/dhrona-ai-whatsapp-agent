from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.db_repo import DatabaseRepository
from app.middleware.auth_middleware import get_current_admin
from typing import List, Dict, Any

router = APIRouter()

@router.get("")
async def list_conversations(admin: dict = Depends(get_current_admin)):
    """
    Lists all active chat sessions (customers).
    """
    return DatabaseRepository.get_chat_sessions()

@router.get("/{session_id}/messages")
async def get_messages(session_id: str, admin: dict = Depends(get_current_admin)):
    """
    Retrieves message history for a specific customer session.
    """
    return DatabaseRepository.get_session_messages(session_id)

@router.post("/{session_id}/takeover")
async def toggle_human_takeover(
    session_id: str, 
    human_takeover: bool, 
    admin: dict = Depends(get_current_admin)
):
    """
    Toggles the human takeover mode flag.
    If true, the automated RAG reply loop is paused for this customer.
    """
    success = DatabaseRepository.update_session_takeover(session_id, human_takeover)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update human takeover status"
        )
    return {"success": True, "human_takeover": human_takeover}

@router.get("/system/logs")
async def get_system_logs(admin: dict = Depends(get_current_admin)):
    """
    Retrieves detailed logs of individual user prompts, RAG documents matched, and generation speeds.
    """
    return DatabaseRepository.get_conversation_logs()
