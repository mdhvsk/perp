from dataclasses import dataclass
from typing import List, Optional
from xml.dom.minidom import Document

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.ingestion import IngestionPipeline
from pinecone.grpc import PineconeGRPC
from llama_index.vector_stores.pinecone import PineconeVectorStore
import arxiv
from llama_index.readers.file import PDFReader


from backend.services.base_service import BaseService, ServiceConfig

class EmbeddingService(BaseService):
    """Service for managing embeddings and vector storage."""
    
    def __init__(self, config: Optional[ServiceConfig] = None):
        self.config = config or self._load_default_config()
        self._initialize_components()
    
    def _initialize_components(self) -> None:
        """Initialize all service components."""
        self.embedding_model = OpenAIEmbedding(api_key=self.config.openai_api_key)
        self.vector_store = self._create_vector_store()
        self.pipeline = self._create_ingestion_pipeline()
    
    def _create_ingestion_pipeline(self) -> IngestionPipeline:
        """Create and configure the ingestion pipeline."""
        return IngestionPipeline(
            transformations=[
                SemanticSplitterNodeParser(
                    buffer_size=self.config.buffer_size,
                    breakpoint_percentile_threshold=self.config.breakpoint_percentile,
                    embed_model=self.embedding_model,
                ),
                self.embedding_model,
            ],
            vector_store=self.vector_store
        )
    
    def run_pipeline(self, docs: List[Document] | None):
        """Run the ingestion pipeline on documents."""
        print("Running pipeline")
        self.pipeline.run(documents=docs)