import os
import json
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import AIAgent
from rag import RAGSystem
import uvicorn

app = FastAPI(title="AI Agent RAG System", version="1.0.0")

# Initialize agent and RAG system
rag_system = RAGSystem()
agent = AIAgent(rag_system=rag_system)

# Session storage (in-memory for demo)
sessions = {}

class Query(BaseModel):
    query: str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[str]
    session_id: str

@app.post("/ask", response_model=QueryResponse)
async def ask(query: Query):
    """
    Process a user query using the AI Agent with RAG
    """
    try:
        session_id = query.session_id or str(len(sessions) + 1)
        
        # Get or create session
        if session_id not in sessions:
            sessions[session_id] = {"history": []}
        
        # Process query
        result = await agent.process_query(
            query=query.query,
            session_id=session_id,
            history=sessions[session_id]["history"]
        )
        
        # Update history
        sessions[session_id]["history"].append({
            "query": query.query,
            "answer": result["answer"]
        })
        
        return QueryResponse(
            answer=result["answer"],
            source_documents=result.get("sources", []),
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "AI Agent RAG System API", "docs_url": "/docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
