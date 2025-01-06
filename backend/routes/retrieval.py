# app/api/routes/notes.py
from fastapi import APIRouter, FastAPI, HTTPException, Query, File, UploadFile, Body
from typing import Dict, List, Optional
from pydantic import BaseModel

from backend.services.llm_service import LLMService


class QueryGeneral(BaseModel):
    query: str

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
    input: QueryGeneral,
):
    
    response =  llm_service.query(input.query)
    return response
  

@router.post("/nutrition")
async def search_nutrition_data(
    query: str,
    dietary_restrictions: List[str] = Query(None),
    allergies: List[str] = Query(None)
) -> dict:
    pass

@router.post("/medical")
async def search_medical_information(
    query: str,
    include_research: bool = False,
    credentials: Optional[dict] = None
) -> dict:
    pass



# Initialize LLM service

@router.post("/ask")
async def ask_health_question(input: QueryGeneral,
):
    return llm_service.query_with_research(input.query)
