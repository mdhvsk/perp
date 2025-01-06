from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import db_router
from .routes import ingestion
from .routes import retrieval
import logging
import uvicorn
import os

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a logger for your application
logger = logging.getLogger(__name__)


app = FastAPI()


origins = ["http://localhost:3000","https://perp-henna.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(ingestion.router)
app.include_router(retrieval.router)
app.include_router(db_router.router)



@app.get("/")
async def health_check():
    try:
        settings = get_settings()
        assert settings.OPENAI_API_KEY, "OpenAI API key not set"
        print(settings.PINECONE_API_KEY)
        print(settings.OPENAI_API_KEY)

        assert settings.PINECONE_API_KEY, "Pinecone API key not set"
        
        # Test services
        # ... test OpenAI connection
        # ... test Pinecone connection
        
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )