# Active Context

## Current Focus
- Completed Phase 1: Foundation and Core Structure
- Preparing for Phase 2: Core Backend Development

## Recent Activities
- Created project structure with appropriate directories
- Set up Docker and Docker Compose configuration
- Implemented database schema with SQLAlchemy
- Created database models for users, documents, chunks, graph nodes/edges, chats
- Implemented core API structure with FastAPI
- Created authentication routes and JWT implementation
- Implemented document processing skeleton
- Created mock LLM connector for development
- Implemented mock RAG retriever for development

## Immediate Next Steps
- Implement actual user authentication system
- Complete document processing pipeline with real text extraction
- Implement BM25 indexing using Pyserini
- Implement FAISS vector search
- Develop GraphRAG using NetworkX
- Integrate neural reranking
- Begin frontend development with React

## Open Questions
- Best approach for storing and retrieving vector embeddings efficiently
- Optimal chunking strategy for different document types
- Most effective way to implement GraphRAG relationships
- Performance considerations for hybrid search
- Security best practices for API key storage
- Frontend framework selection (React vs Vue vs other options)