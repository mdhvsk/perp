from backend.services.base_service import BaseService, ServiceConfig
from backend.services.embedding_service import EmbeddingService
from typing import List, Optional, Dict, Any

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from fastapi import HTTPException

import logging

logger = logging.getLogger(__name__)
class LLMService(BaseService):
    """Service for handling LLM operations."""
    
    def __init__(self, embedding_service: EmbeddingService = None, config: Optional[ServiceConfig] = None):
        """
        Initialize LLM service.
        
        Args:
            embedding_service: Optional EmbeddingService instance to share vector store
            config: Optional configuration
        """
        self.config = config or self._load_default_config()
        self.client = OpenAI(api_key=self.config.openai_api_key)
        
        # Use existing vector store from embedding service or create new one
        if embedding_service:
            self.vector_store = embedding_service.vector_store
        else:
            self.vector_store = self._create_vector_store()
            
        self.query_engine = self._setup_retrieval()

    def _setup_retrieval(self) -> RetrieverQueryEngine:
        """Set up the retrieval pipeline."""
        index = VectorStoreIndex.from_vector_store(self.vector_store)
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=self.config.top_k
        )
        return RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[
                SimilarityPostprocessor(similarity_cutoff=self.config.similarity_cutoff)
            ]
        )

    def query(self, question: str) -> Dict[str, Any]:
        """Basic query without research context."""
        try:
            messages = [
                ChatMessage(role="system", content="You are a personal trainer and nutritionist"),
                ChatMessage(role="user", content=question)
            ]
            response = self.client.chat(messages=messages)
            
            return {
                'question': question,
                'answer': str(response),
                'sources': None,
                'error': None
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def query_with_research(self, question: str) -> Dict[str, Any]:
        """Query with research context from vector store."""
        try:
            # Get research context
            research_response = self.query_engine.query(question)
            sources = self._extract_sources(research_response)

            # Format messages with research context
            messages = [
                ChatMessage(role="system", content="You are a personal trainer and nutritionist"),
                ChatMessage(
                    role="user", 
                    content=f"Using this research context: {str(research_response)}\n\nPlease answer: {question}"
                )
            ]
            
            response = self.client.chat(messages=messages)

            return {
                'question': question,
                'answer': str(response),
                'sources': sources,
                'error': None
            }
        except Exception as e:
            return {
                'question': question,
                'answer': None,
                'sources': None,
                'error': str(e)
            }

    def _extract_sources(self, response) -> List[Dict[str, Any]]:
        """Extract source information from response."""
        sources = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                source = {
                    'text': node.node.text[:200] + "..." if len(node.node.text) > 200 else node.node.text,
                    'score': node.score if hasattr(node, 'score') else None,
                    'metadata': {
                        'title': node.metadata.get('title', 'Unknown'),
                        'authors': node.metadata.get('authors', []),
                        'published_date': node.metadata.get('published_date', 'Unknown'),
                        'arxiv_id': node.metadata.get('arxiv_id', 'Unknown')
                    } if hasattr(node, 'metadata') else {}
                }
                sources.append(source)
        return sources
    
    def generate_short_title(self, text: str) -> str:
        """
        Generate a short title (up to 3 words) for a given text.
        
        Args:
            text: Text content to generate title for
            
        Returns:
            A string containing up to 3 words as a title
        """
        try:
            messages = [
                ChatMessage(
                    role="system", 
                    content="You are a concise title generator. Always respond with only 1-3 words."
                ),
                ChatMessage(
                    role="user", 
                    content=f"Generate a 1-3 word title that captures the main topic of this text: {text}"
                )
            ]
            
            response = self.client.chat(messages=messages)
            title = str(response).strip()
            
            # Ensure we only return up to 3 words
            words = title.split()
            if len(words) > 3:
                title = ' '.join(words[:3])
                
            return title
            
        except Exception as e:
            logger.error(f"Error generating title: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate title: {str(e)}"
            )