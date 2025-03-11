# Doogie - Advanced RAG Chatbot System

Doogie is a hybrid RAG (Retrieval-Augmented Generation) chatbot system that combines multiple retrieval approaches (BM25, FAISS vector search, and GraphRAG) with neural reranking to provide highly relevant and accurate responses.

## Features

- **Hybrid RAG**: Combines BM25 and FAISS vector search for improved retrieval
- **GraphRAG**: Utilizes graph-based relationships for complex queries
- **Neural Reranking**: Improves result relevance with cross-encoder models
- **Multiple LLM Support**: Connect to Ollama server or API-based LLMs (OpenAI, Claude, OpenRouter)
- **Document Management**: Support for multiple document types (PDF, DOCX, MD, RST, TXT)
- **Web Interface**: Modern, responsive UI with dark/light mode
- **User Management**: Email-based authentication with admin approval
- **Chat History**: Persistent chat history with feedback mechanism
- **Performance Metrics**: Display tokens/s and other statistics

## Technology Stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy, SQLite3
- **Frontend**: React.js, Tailwind CSS
- **Containerization**: Docker, Docker Compose
- **RAG Components**: FAISS, Pyserini/BM25, NetworkX
- **LLM Integration**: OpenAI, Claude, Ollama, OpenRouter

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/doogie.git
   cd doogie
   ```

2. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

3. Access the web interface at http://localhost:8000

### Initial Setup

1. Register an admin user
2. Configure API keys in the settings panel
3. Upload documents to the RAG system
4. Start chatting!

## Development

### Project Structure

```
doogie/
├── src/
│   ├── api/              # FastAPI routes and schemas
│   ├── core/             # Core application logic
│   ├── database/         # Database models and connection
│   ├── document_processor/ # Document processing pipeline
│   ├── frontend/         # React.js frontend
│   ├── llm_connector/    # LLM integration
│   ├── rag/              # RAG implementation
│   └── utils/            # Utility functions
├── tests/                # Test suite
├── migrations/           # Database migrations
├── docker-compose.yml    # Docker Compose configuration
└── Dockerfile            # Docker configuration
```

### Running Tests

```bash
docker-compose run test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [React](https://reactjs.org/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Ollama](https://ollama.ai/)