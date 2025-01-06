from dataclasses import dataclass
from pinecone.grpc import PineconeGRPC
from llama_index.vector_stores.pinecone import PineconeVectorStore


from dotenv import load_dotenv
import os

@dataclass
class ServiceConfig:
    openai_api_key: str
    pinecone_api_key: str
    index_name: str
    buffer_size: int = 1
    breakpoint_percentile: float = 95
    similarity_cutoff: float = 0.7
    top_k: int = 5

class BaseService:
    
    @staticmethod
    def _load_default_config() -> ServiceConfig:
        load_dotenv()
        return ServiceConfig(
            openai_api_key=os.getenv('OPENAI_API_KEY', ''),
            pinecone_api_key=os.getenv('PINECONE_API_KEY', ''),
            index_name="perplexity"
        )

    def _create_vector_store(self) -> PineconeVectorStore:
        pc = PineconeGRPC(api_key=self.config.pinecone_api_key)
        pinecone_index = pc.Index(self.config.index_name)
        return PineconeVectorStore(pinecone_index=pinecone_index)