# Product Context

## Vision
Create an advanced, flexible RAG chatbot system that combines multiple retrieval approaches to provide highly relevant and accurate responses, with a modern user interface and robust admin controls.

## Target Users
- **Administrators**: Technical users who manage the system, documents, and user access
- **End Users**: Individuals who interact with the chatbot to retrieve information

## Key Differentiators
- Hybrid RAG combining multiple retrieval approaches (BM25, FAISS, GraphRAG)
- Neural reranking for improved response relevance
- Flexible LLM integration (Ollama, OpenAI, Claude, OpenRouter)
- Multiple document ingestion methods (direct upload, GitHub, web crawling)
- Comprehensive admin controls and analytics

## Constraints
- Python 3.12+ ecosystem
- SQLite3 database
- Docker containerization
- Browser-based interface

## Success Metrics
- Response accuracy and relevance
- Retrieval speed and efficiency
- User satisfaction and feedback scores
- System reliability and uptime
- Document processing capabilities

## Integration Points
- External Ollama server
- API-based LLM services (OpenAI, Claude, OpenRouter)
- GitHub repositories
- Web content via crawling
- Document management systems

## Deployment Considerations
- Docker and Docker Compose for containerization
- Persistent storage for database and documents
- API key management and security
- User authentication and authorization
