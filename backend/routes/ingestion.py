# app/api/routes/notes.py
from fastapi import APIRouter, FastAPI, HTTPException, Query, File, UploadFile, Body
from typing import List, Optional
from pydantic import BaseModel
from backend.services.document_service import DocumentService
from backend.services.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["ingestion"])
embedding_service = EmbeddingService()
document_service = DocumentService(embedding_service)

@router.post("/documents/upload")
async def upload_health_document(
    file: UploadFile,
    category: str = Query(..., enum=["nutrition", "medical", "fitness", "mental-health", "research"]),
    source: str = Query(..., description="Source of the document (e.g., WHO, NIH, peer-reviewed journal)"),
    year: Optional[int] = Query(None, description="Publication year")
):
    """Upload and index health-related documents with metadata."""
    pass

@router.get("/documents/categories")
async def get_document_categories():
    """Get all available document categories and their statistics."""
    pass


@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    
    
    pass

@router.post("/documents/topic")
async def queryArchive(
    keyword: str,
    file_number: int = 0
):
    logging.info("Querying /document/topic for keyword: {keyword}")
    document_service.process_and_embed_papers(keyword)
    
    

