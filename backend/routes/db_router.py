from backend.services import llm_service
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from backend.services.search_message_service import SearchMessageService
from backend.services.search_session_service import SearchSessionService
from ..utils.supabase_client import get_supabase
import logging

logger = logging.getLogger(__name__)
class SessionCreate(BaseModel):
    title: str

class SessionResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

class MessageCreate(BaseModel):
    session_id: str
    question: str
    answer: str
    sources: List[Dict[str, Any]] = None

class MessageResponse(BaseModel):
    id: str
    session_id: str
    question: str
    answer: str
    sources: List[Dict[str, Any]]
    created_at: str

class TitleRequest(BaseModel):
    text: str
    session_id: Optional[str] = None

class TitleResponse(BaseModel):
    title: str
    session_id: Optional[str] = None
    updated: bool = False

router = APIRouter(prefix="/api/db", tags=["database"])

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
            question=message.question,
            answer=message.answer,
            sources=message.sources
        )
    except Exception as e:
        logging.warning("Not processable")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-title", response_model=TitleResponse)
async def generate_title(
    request: TitleRequest,
    search_session_service: SearchSessionService = Depends(get_search_session_service)
):

    try:
        # Generate title
        llm = llm_service.LLMService()
        result = llm.generate_short_title(request.text)
        title = result["title"]
        
        # Update session if session_id provided
        if request.session_id:
            try:
                # Get current session
                session = await search_session_service.get_session_by_id(request.session_id)
                
                if session:
                    # Update the session with new title
                    current_time = datetime.utcnow().isoformat()
                    updated_data = {
                        'title': title,
                        'updated_at': current_time
                    }
                    
                    response = search_session_service.supabase.table('search_sessions')\
                        .update(updated_data)\
                        .eq('id', str(request.session_id))\
                        .execute()
                        
                    result["updated"] = True
                else:
                    logger.warning(f"Session {request.session_id} not found")
                    
            except Exception as e:
                logger.error(f"Error updating session title: {str(e)}")
                # Don't fail the entire request if session update fails
                result["updated"] = False
        
        return TitleResponse(
            title=result["title"],
            session_id=result["session_id"],
            updated=result["updated"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate title: {str(e)}"
        )