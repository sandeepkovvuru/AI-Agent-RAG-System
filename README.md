# AI Agent with RAG (Retrieval-Augmented Generation) System

## Overview

This project implements an intelligent AI agent that combines Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers to user queries about company documents. The system uses Azure OpenAI for language understanding and can retrieve relevant information from document collections.

## Features

- **AI Agent with Tool Calling**: Intelligent agent that decides whether to use LLM directly or retrieve documents
- **RAG (Retrieval-Augmented Generation)**: Retrieves relevant documents and uses them as context for better answers
- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **Multi-Session Support**: Maintains conversation history across multiple sessions
- **Azure Integration**: Uses Azure OpenAI for state-of-the-art language models
- **Document Management**: Load and manage company documents for retrieval
- **Prompt Engineering**: Carefully crafted system prompts for consistent behavior
- **RESTful API**: Easy-to-use endpoints for querying and document management

## Tech Stack

- **Backend**: FastAPI (Python)
- **LLM**: Azure OpenAI GPT-4
- **Document Retrieval**: Keyword-based retrieval (FAISS/Azure AI Search ready)
- **Embeddings**: Azure OpenAI Embeddings
- **Web Server**: Uvicorn
- **Async**: Native async/await support

## Architecture

```
User Query
    |
    v
  FastAPI Endpoint (/ask)
    |
    v
  AI Agent
    |
    +---> RAG System (Document Retrieval)
    |
    +---> Azure OpenAI (LLM)
    |
    v
Structured Response (answer + sources)
```

## Project Structure

```
AI-Agent-RAG-System/
├── app.py              # FastAPI application and main endpoints
├── agent.py            # AI Agent implementation with LLM integration
├── rag.py              # RAG system with document retrieval
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── Dockerfile          # Docker containerization
├── docker-compose.yml  # Docker Compose configuration
├── documents/          # Sample documents directory
└── README.md           # This file
```

## API Endpoints

### 1. Ask Query
**POST** `/ask`

Process a user query with RAG context.

**Request Body**:
```json
{
  "query": "What is the annual leave policy?",
  "session_id": "session-123"  // Optional
}
```

**Response**:
```json
{
  "answer": "Employees are entitled to 20 days of annual leave...",
  "source_documents": ["company_policy_leave.txt"],
  "session_id": "session-123"
}
```

### 2. Health Check
**GET** `/health`

Check API health status.

### 3. API Documentation
**GET** `/docs`

Access Swagger UI documentation.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Azure OpenAI API key and endpoint
- pip package manager

### Local Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/AI-Agent-RAG-System.git
cd AI-Agent-RAG-System
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your Azure credentials
export AZURE_OPENAI_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4"
```

5. **Run the application**:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build Docker image**:
```bash
docker build -t ai-agent-rag .
```

2. **Run Docker container**:
```bash
docker run -p 8000:8000 --env-file .env ai-agent-rag
```

### Azure Deployment

#### Using Azure App Service

1. **Create App Service**:
```bash
az appservice plan create -g myResourceGroup -n myAppPlan
az webapp create -g myResourceGroup -p myAppPlan -n myAIAgent
```

2. **Deploy code**:
```bash
az webapp up -n myAIAgent -g myResourceGroup
```

3. **Configure environment variables**:
```bash
az webapp config appsettings set -g myResourceGroup -n myAIAgent \
  --settings AZURE_OPENAI_KEY="your-key" \
             AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
```

#### Using Azure Functions

1. **Initialize function app**:
```bash
func init AIAgentFunction --python
```

2. **Deploy**:
```bash
func azure functionapp publish myFunctionApp
```

## Design Decisions

1. **Keyword-based Retrieval**: Started with simple keyword matching (Jaccard similarity) for quick implementation. Can be upgraded to embedding-based retrieval using FAISS or Azure AI Search.

2. **In-Memory Session Storage**: Session history is stored in memory for demo purposes. For production, use Redis or database.

3. **Async/Await Pattern**: Full async implementation for better scalability and performance.

4. **System Prompts**: Carefully engineered system prompts to guide LLM behavior for document-based Q&A.

5. **Tool Calling Foundation**: Architecture supports Azure OpenAI's tool calling API for future expansion.

## Limitations and Future Improvements

### Current Limitations
- Document retrieval is keyword-based (no semantic embeddings yet)
- Session storage is in-memory (not persistent)
- No authentication/authorization implemented
- Limited error handling for LLM failures
- No rate limiting

### Future Improvements
- [ ] Integrate FAISS or Azure AI Search for semantic retrieval
- [ ] Add persistent session storage (Redis/Database)
- [ ] Implement JWT-based authentication
- [ ] Add request logging and monitoring (Application Insights)
- [ ] Support for PDF/image documents (with OCR)
- [ ] Batch processing for bulk queries
- [ ] Custom knowledge base management API
- [ ] Fine-tuning support for domain-specific tasks
- [ ] WebSocket support for real-time streaming responses
- [ ] Multi-language support

## Testing

Example test queries:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the annual leave policy?",
    "session_id": "session-1"
  }'
```

## Troubleshooting

### Azure OpenAI Connection Error
- Verify `AZURE_OPENAI_KEY` and `AZURE_OPENAI_ENDPOINT` are correct
- Check network connectivity to Azure
- Ensure API version in code matches your deployment

### No Documents Found
- Check `documents/` directory exists
- Ensure document files have `.txt` extension
- Verify file permissions

### Slow Response Times
- Check document retrieval performance
- Monitor Azure OpenAI API latency
- Consider caching frequently asked questions

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - See LICENSE file for details

## Contact

For questions or support, please contact: sandeepkovvuru@example.com

## Acknowledgments

- Built as an AI Engineer assignment project
- Uses Azure OpenAI for LLM capabilities
- Inspired by best practices in RAG systems
