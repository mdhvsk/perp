from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    PINECONE_API_KEY: str    
    OPENAI_API_KEY: str
    class Config:
        env_file = ".env"



def get_settings():
    return Settings()

