# Doogie - Advanced RAG Chatbot System

## Project Overview
Doogie is an advanced chatbot system utilizing hybrid RAG (Retrieval-Augmented Generation) techniques to provide intelligent, context-aware responses. The system combines BM25 and FAISS vector search with graph-based RAG approaches, enhanced by neural reranking for improved result relevance.

## Core Requirements

### RAG Engine
- Hybrid RAG implementation combining BM25 and FAISS vector search
- GraphRAG for complex relationship mapping
- Neural reranking for improved result relevance
- Support for multiple document types (PDF, DOCX, MD, RST, TXT)
- Document management interface
- Direct content input via forms
- RAG reset and reprocessing capabilities
- Integration with GitHub repositories and website crawling

### LLM Integration
- External Ollama server connection
- API-based LLM integration (OpenRouter, OpenAI, Claude)
- Dynamic model selection for different tasks
- System-wide prompt configuration
- Support for reasoning models with `<think></think>` tags

### User Interface
- Modern, dynamic web interface
- Dark mode by default with light mode option
- Real-time streaming of responses
- Chat history visualization
- Performance statistics display (tokens/s, etc.)
- Response feedback mechanism

### Backend
- Python 3.12+ implementation
- SQLite3 database for data persistence
- Docker and Docker Compose for containerization
- Comprehensive testing within container

### User Management
- Email-based user authentication
- Admin approval for user registration
- Admin-only settings interface
- API key storage and management
- Chat history persistence and resumption

## Project Goals
1. Create a production-ready RAG chatbot system
2. Implement state-of-the-art retrieval techniques
3. Provide flexibility in LLM selection and configuration
4. Ensure a seamless, responsive user experience
5. Maintain robust security and admin controls