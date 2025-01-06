# RAG-Powered Health/Nutrition Answer Engine

A full-stack application that provides AI-powered answers to research queries using RAG (Retrieval Augmented Generation) technology. The system retrieves relevant research papers from arXiv, generates accurate responses using OpenAI's LLM, and maintains context through vector similarity search.

## 🚀 Features

- **Real-time Research Paper Analysis**: Fetches and analyzes papers from arXiv API in real-time
- **Intelligent Answer Generation**: Uses OpenAI's GPT models for generating accurate, context-aware responses
- **Vector Similarity Search**: Implements efficient document retrieval using Pinecone
- **Persistent Chat History**: Stores all conversations and context in Supabase
- **Modern Web Interface**: Built with Next.js (App Router) for a responsive user experience

## 🛠️ Technology Stack

### Frontend
- Next.js
- React
- TailwindCSS
- TypeScript

### Backend
- FastAPI
- Python 3.9+
- OpenAI API
- Pinecone
- Supabase
- LlamaIndex

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- OpenAI API key
- Pinecone API key
- Supabase account and credentials
- arXiv API access
- LlamaIndex API key


## Architecture Diagram 
<img width="911" alt="Screenshot 2025-01-05 at 8 43 45 PM" src="https://github.com/user-attachments/assets/2ad44848-9b53-4d32-baf0-90bb649764da" />

## ⚙️ Environment Variables

```bash
# Backend (.env)
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=your_backend_url
```

## 🚀 Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/mdhvsk/perp.git
cd perp
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start the development servers:

Backend:
```bash
uvicorn backend.main:app --reload
```

Frontend:
```bash
npm run dev
```

## 🎯 Usage

1. Visit `http://localhost:3000` in your browser
2. Enter your research query in the chat interface
3. The system will:
   - Retrieve relevant papers from arXiv
   - Generate embeddings using OpenAI
   - Store and search vectors in Pinecone
   - Generate a comprehensive answer using OpenAI's LLM
   - Store the conversation in Supabase

## 🔄 RAG Pipeline
The RAG pipeline is implemented using LlamaIndex's powerful data framework, which handles:

Document Retrieval: Fetches relevant research papers from arXiv based on user query using LlamaIndex's Document Loaders
Embedding Generation: Creates embeddings for documents using OpenAI's embedding model through LlamaIndex's embedding interface
Vector Storage: Stores embeddings in Pinecone using LlamaIndex's VectorStoreIndex and PineconeVectorStore
Context Retrieval: Retrieves relevant context based on query similarity using LlamaIndex's query engine
Answer Generation: Generates comprehensive answers using OpenAI's LLM through LlamaIndex's LLMPredictor

## 📚 Dependencies & APIs

LlamaIndex: Core framework used for:

RAG pipeline orchestration
Document loading and processing
Vector store integration
LLM/Embedding interface management


arXiv API: Primary source for research papers
OpenAI API: Used for:

Text embeddings (text-embedding-ada-002)
LLM generation (gpt-4-turbo)


Pinecone: Vector database for similarity search
Supabase: PostgreSQL database for chat storage




