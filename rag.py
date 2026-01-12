import os
import json
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self, documents_path: str = "documents"):
        self.documents_path = Path(documents_path)
        self.documents = []
        self.embeddings = {}
        self.index = None
        self._load_documents()
    
    def _load_documents(self):
        """Load all documents from the documents directory"""
        try:
            # Create sample documents if none exist
            if not self.documents_path.exists():
                self.documents_path.mkdir(parents=True, exist_ok=True)
                self._create_sample_documents()
            
            # Load documents from files
            for file_path in self.documents_path.glob("*.txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents.append({
                        "source": file_path.name,
                        "content": content
                    })
            
            logger.info(f"Loaded {len(self.documents)} documents")
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
    
    def _create_sample_documents(self):
        """Create sample company policy documents"""
        sample_docs = {
            "company_policy_leave.txt": """COMPANY LEAVE POLICY
            
Enjoyable Leave:
- Employees are entitled to 20 days of annual leave
- Leave should be requested 2 weeks in advance
- Public holidays are additional to annual leave
- Work-from-home is allowed up to 2 days per week
            """,
            "company_policy_code_conduct.txt": """CODE OF CONDUCT
            
Employees must:
1. Maintain professional conduct at all times
2. Report conflicts of interest
3. Protect company information
4. Treat all colleagues with respect
5. Follow safety procedures
            """,
            "company_product_features.txt": """PRODUCT FEATURES
            
Our AI Agent RAG System provides:
- Document retrieval and indexing
- Natural language processing
- Multi-session support
- Azure OpenAI integration
- FastAPI backend
- Real-time question answering
            """
        }
        
        for filename, content in sample_docs.items():
            with open(self.documents_path / filename, "w") as f:
                f.write(content)
    
    async def retrieve_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant documents for the query"""
        try:
            if not self.documents:
                return []
            
            # Simple keyword-based retrieval
            query_words = set(query.lower().split())
            scores = []
            
            for doc in self.documents:
                doc_words = set(doc["content"].lower().split())
                # Calculate Jaccard similarity
                intersection = query_words & doc_words
                union = query_words | doc_words
                score = len(intersection) / len(union) if union else 0
                scores.append(score)
            
            # Get top-k documents
            top_indices = np.argsort(scores)[-top_k:][::-1]
            retrieved_docs = [self.documents[i] for i in top_indices if scores[i] > 0]
            
            return retrieved_docs
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def add_document(self, title: str, content: str):
        """Add a new document to the system"""
        try:
            self.documents.append({
                "source": title,
                "content": content
            })
            logger.info(f"Added document: {title}")
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
    
    def get_document_stats(self) -> Dict:
        """Get statistics about loaded documents"""
        total_chars = sum(len(doc["content"]) for doc in self.documents)
        return {
            "total_documents": len(self.documents),
            "total_characters": total_chars,
            "documents": [doc["source"] for doc in self.documents]
        }
