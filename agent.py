import os
import json
from typing import Optional, List, Dict
from openai import AzureOpenAI
import logging

logger = logging.getLogger(__name__)

class AIAgent:
    def __init__(self, rag_system=None):
        self.rag_system = rag_system
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        return """You are an intelligent AI assistant that helps answer questions about company documents.
        
Your responsibilities:
1. Answer user questions accurately based on provided context from company documents
2. If you need more information from documents, indicate that you're retrieving relevant documents
3. Always cite the source documents when providing answers
4. Be honest if information is not available in the documents
5. Maintain context from the conversation history

When answering, structure your response clearly and provide relevant document references."""
    
    async def process_query(self, query: str, session_id: str, history: List[Dict]) -> Dict:
        """Process user query using tool calling with RAG"""
        try:
            # Retrieve relevant documents
            relevant_docs = []
            sources = []
            
            if self.rag_system:
                relevant_docs = await self.rag_system.retrieve_documents(query)
                sources = [doc.get("source", "Unknown") for doc in relevant_docs]
            
            # Build context from retrieved documents
            context = self._build_context(relevant_docs)
            
            # Build messages with conversation history
            messages = self._build_messages(query, history, context)
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": sources,
                "session_id": session_id
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    def _build_context(self, documents: List[Dict]) -> str:
        """Build context string from retrieved documents"""
        if not documents:
            return "No relevant documents found."
        
        context_parts = ["Relevant documents:"]
        for i, doc in enumerate(documents[:3], 1):  # Limit to top 3
            source = doc.get("source", "Unknown")
            content = doc.get("content", "")[:500]  # Limit content length
            context_parts.append(f"\n[Document {i}] Source: {source}\n{content}...")
        
        return "\n".join(context_parts)
    
    def _build_messages(self, query: str, history: List[Dict], context: str) -> List[Dict]:
        """Build message list for LLM"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Context: {context}"}
        ]
        
        # Add conversation history
        for item in history[-5:]:  # Keep last 5 exchanges
            messages.append({"role": "user", "content": item.get("query")})
            messages.append({"role": "assistant", "content": item.get("answer")})
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        return messages
