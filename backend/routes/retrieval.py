# app/api/routes/notes.py
from fastapi import APIRouter, FastAPI, HTTPException, Query, File, UploadFile, Body
from typing import List, Optional
from pydantic import BaseModel

from backend.services.llm_service import LLMService


class SearchResponse(BaseModel):
    query: str
    results: List[dict]
    sources: List[dict]
    related_topics: List[str]
    medical_disclaimer: str


router = APIRouter(prefix="/api/query", tags=["retrieval"])

llm_service = LLMService()  # Add your vector_store if available


@router.post("/general")
async def search_health_information(
    query: str,
    filters: dict = Body(default={}),
    max_results: int = 5
) -> str:
    llm = LLMService()
    
    return llm.query(query)
  

@router.post("/nutrition")
async def search_nutrition_data(
    query: str,
    dietary_restrictions: List[str] = Query(None),
    allergies: List[str] = Query(None)
) -> dict:
    """Specialized nutrition search with dietary considerations."""
    pass

@router.post("/medical")
async def search_medical_information(
    query: str,
    include_research: bool = False,
    credentials: Optional[dict] = None
) -> dict:
    """Medical information search with optional research paper inclusion."""
    pass



# Initialize LLM service

@router.post("/ask")
async def ask_health_question(request: str):
    return llm_service.query_with_research(request)
