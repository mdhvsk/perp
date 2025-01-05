from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from backend.services.search_message_service import SearchMessageService
from backend.services.search_session_service import SearchSessionService
from ..utils.supabase_client import get_supabase

class SessionCreate(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

class MessageCreate(BaseModel):
    session_id: UUID
    role: str
    message: str

class MessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    message: str
    created_at: datetime

# Create the router
router = APIRouter(prefix="/api/db", tags=["database"])

# Dependency to get our services
async def get_search_session_service():
    return SearchSessionService(get_supabase())

async def get_search_message_service():
    return SearchMessageService(get_supabase())

# Session routes
@router.get("/sessions", response_model=List[SessionResponse])
async def get_all_sessions(
    service: SearchSessionService = Depends(get_search_session_service)
) -> List[Dict[str, Any]]:
    try:
        return await service.get_all_sessions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session_by_id(
    session_id: UUID,
    service: SearchSessionService = Depends(get_search_session_service)
) -> Dict[str, Any]:
    try:
        session = await service.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    session: SessionCreate,
    service: SearchSessionService = Depends(get_search_session_service)
) -> Dict[str, Any]:
    try:
        return await service.create_session(session.title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Message routes
@router.get("/messages/{session_id}", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: UUID,
    service: SearchMessageService = Depends(get_search_message_service)
) -> List[Dict[str, Any]]:
    try:
        return await service.get_messages_by_session_id(session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/messages", response_model=MessageResponse)
async def create_message(
    message: MessageCreate,
    service: SearchMessageService = Depends(get_search_message_service)
) -> Dict[str, Any]:
    try:
        return await service.create_message(
            session_id=message.session_id,
            role=message.role,
            message=message.message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))