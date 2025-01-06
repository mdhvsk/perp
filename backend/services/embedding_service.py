import time
from typing import List, Optional
from llama_index.core import Document

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.ingestion import IngestionPipeline



from backend.services.base_service import BaseService, ServiceConfig
import logging

logger = logging.getLogger(__name__)

class EmbeddingService(BaseService):
    
    def __init__(self, config: Optional[ServiceConfig] = None):
        self.config = config or self._load_default_config()
        self._initialize_components()
        self.batch_size = 50  # Smaller batch size for safety

    
    def _initialize_components(self) -> None:
        self.embedding_model = OpenAIEmbedding(api_key=self.config.openai_api_key)
        self.vector_store = self._create_vector_store()
        self.pipeline = self._create_ingestion_pipeline()
    
    def _create_ingestion_pipeline(self) -> IngestionPipeline:
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
    
    def run_pipeline(self, documents: List[Document] | None):
        if not documents:
            logger.warning("No documents provided to process")
            return
        
        try:
            total_docs = len(documents)
            logger.info(f"Processing {total_docs} documents through pipeline")
            
            # Process in batches
            for i in range(0, total_docs, self.batch_size):
                batch = documents[i:i + self.batch_size]
                logger.info(f"Processing batch {i//self.batch_size + 1}, size: {len(batch)}")
                
                try:
                    self.pipeline.run(documents=batch)
                    # Add a small delay between batches if needed
                    time.sleep(1)  
                except Exception as e:
                    logger.error(f"Error processing batch {i//self.batch_size + 1}: {str(e)}")
                    # Continue with next batch instead of failing completely
                    continue
                    
            logger.info("Successfully processed all documents through pipeline")
        except Exception as e:
            logger.error(f"Failed to run pipeline: {str(e)}")
            raise