# app/api/routes/notes.py
from pathlib import Path
from fastapi import APIRouter, FastAPI, HTTPException, Query, File, UploadFile, Body
from typing import List, Optional
from pydantic import BaseModel
from backend.services.document_service import DocumentService
from backend.services.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["ingestion"])
embedding_service = EmbeddingService()
document_service = DocumentService(embedding_service, 3)

class FetchPapersResponse(BaseModel):
    """Response model for fetched papers"""
    papers_fetched: int
    papers: List[dict]
    query: str

class ProcessingResponse(BaseModel):
    """Response model for document processing"""
    status: str
    message: str
    documents_processed: Optional[int] = None

@router.post("/papers/fetch")
async def fetch_papers(
    keyword: str = Query(..., description="Search keyword for arXiv papers"),
    max_results: Optional[int] = Query(10, description="Maximum number of papers to fetch")
):
    """
    Fetch papers from arXiv without processing them.
    """
    try:
        # Override max_results temporarily
        original_max = document_service.max_results
        document_service.max_results = max_results
        
        papers = document_service.fetch_papers(keyword)
        
        # Restore original max_results
        document_service.max_results = original_max
        
        return FetchPapersResponse(
            papers_fetched=len(papers),
            papers=papers,
            query=keyword
        )
    except Exception as e:
        logger.error(f"Error fetching papers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/process")
async def process_documents():
    """
    Process all PDF documents in the backend/papers directory.
    """
    try:
        # Get all PDFs in the papers directory
        papers_dir = Path("backend/papers")
        if not papers_dir.exists():
            raise HTTPException(status_code=404, detail="Papers directory not found")
        
        # Create paper info list from existing PDFs
        papers = []
        for pdf_file in papers_dir.glob("*.pdf"):
            arxiv_id = pdf_file.stem  # Assuming filename is arxiv_id.pdf
            papers.append({
                'local_path': str(pdf_file),
                'arxiv_id': arxiv_id
            })
        
        if not papers:
            return ProcessingResponse(
                status="error",
                message="No PDF documents found in papers directory"
            )
        
        # Process the documents
        cleaned_docs = document_service.load_and_clean_documents(papers)
        
        if not cleaned_docs:
            return ProcessingResponse(
                status="error",
                message="No documents were successfully processed"
            )
            
        return ProcessingResponse(
            status="success",
            message="Documents processed successfully",
            documents_processed=len(cleaned_docs)
        )
        
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embeddings/create")
async def create_embeddings():
    """
    Run the embedding pipeline on processed documents in memory.
    Note: Documents must be processed first using /documents/process
    """
    try:
        # Get the processed documents
        papers_dir = Path("backend/papers")
        if not papers_dir.exists():
            raise HTTPException(status_code=404, detail="Papers directory not found")
            
        # Get paper info list
        papers = []
        for pdf_file in papers_dir.glob("*.pdf"):
            arxiv_id = pdf_file.stem
            papers.append({
                'local_path': str(pdf_file),
                'arxiv_id': arxiv_id
            })
            
        if not papers:
            return ProcessingResponse(
                status="error",
                message="No documents found to create embeddings"
            )
            
        # Load and process documents
        cleaned_docs = document_service.load_and_clean_documents(papers)
        logging.info("Cleaned_docs list: " + str(len(cleaned_docs)))
        logging.info(cleaned_docs)
        if not cleaned_docs:
            return ProcessingResponse(
                status="error",
                message="No documents were successfully processed for embedding"
            )
            
        # Create embeddings
        document_service.embedding_service.run_pipeline(cleaned_docs)
        
        return ProcessingResponse(
            status="success",
            message="Embeddings created successfully",
            documents_processed=len(cleaned_docs)
        )
        
    except Exception as e:
        logger.error(f"Error creating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/topic")
async def query_archive(
    keyword: str = Query(..., description="Search keyword for arXiv papers")
):
    """
    Complete pipeline: fetch papers, process them, and create embeddings.
    """
    logging.info(f"Querying /document/topic for keyword: {keyword}")
    result = document_service.process_and_embed_papers(keyword)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

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
async def query_archive(
    keyword: str,
):
    logging.info(f"Querying /document/topic for keyword: {keyword}")
    document_service.process_and_embed_papers(keyword)
    
    

