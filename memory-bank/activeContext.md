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
- Fixed SQLite database access issues in Docker by using bind mounts
- Fixed frontend-build permission issues by setting user to 1000 in Docker Compose
- Fixed TypeScript error in useAuth.tsx by adding React import
- Created missing frontend pages (Register, Chat, Documents, Settings, Admin)
- Removed obsolete 'version' attribute from docker-compose.yml
- Fixed frontend static file serving by using absolute path in main.py
- Fixed React AuthProvider error by wrapping App in AuthProvider in main.tsx

## Immediate Next Steps
- Implement actual user authentication system
- Complete document processing pipeline with real text extraction
- Implement BM25 indexing using Pyserini
- Implement FAISS vector search with external embeddings (Ollama or OpenAI)
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
- Integration strategy for external embedding models (Ollama/OpenAI)