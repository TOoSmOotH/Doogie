# Decision Log

This document tracks key architectural and implementation decisions for the Doogie project.

## Format
Each decision record follows this format:
- **ID**: Unique identifier (YYYYMMDD-NN)
- **Date**: When the decision was made
- **Title**: Brief description of the decision
- **Context**: Background and why this decision was needed
- **Options**: Alternatives that were considered
- **Decision**: The chosen approach
- **Rationale**: Why this option was selected
- **Consequences**: Expected impacts of this decision
- **Status**: Current status (Proposed, Accepted, Superseded, Deprecated)

---

## Decision Records

### DEC-20250311-01
- **Date**: 2025-03-11
- **Title**: Project Initialization and Memory Bank Setup
- **Context**: Beginning the Doogie project required establishing a documentation and planning structure to guide development.
- **Options**:
  1. Ad-hoc documentation approach
  2. Structured memory bank with standardized documents
  3. Wiki-based documentation
- **Decision**: Implement structured memory bank with standardized documentation files.
- **Rationale**: A structured approach provides better organization, improves traceability, and ensures consistent documentation across the project lifecycle.
- **Consequences**: Requires initial setup time but will provide long-term benefits for project management and knowledge retention.
- **Status**: Accepted

### DEC-20250311-02
- **Date**: 2025-03-11
- **Title**: Database Technology Selection
- **Context**: The project requires a database for storing user data, documents, and RAG components.
- **Options**:
  1. SQLite - Lightweight, file-based, no separate server
  2. PostgreSQL - Full-featured, robust, separate server
  3. MongoDB - Document-oriented, flexible schema
- **Decision**: Use SQLite for development and initial deployment.
- **Rationale**: SQLite meets the requirements while being simple to set up and deploy. It doesn't require a separate server, which simplifies the Docker setup. The project's data model is well-defined and relational, making a SQL database appropriate.
- **Consequences**: May need to migrate to PostgreSQL if scaling becomes necessary, but SQLite is sufficient for the initial implementation and can be easily replaced later if needed.
- **Status**: Accepted

### DEC-20250311-03
- **Date**: 2025-03-11
- **Title**: API Framework Selection
- **Context**: The project needs a web API framework for the backend.
- **Options**:
  1. FastAPI - Modern, high-performance, easy to use
  2. Flask - Lightweight, flexible, widely used
  3. Django - Full-featured, batteries-included
- **Decision**: Use FastAPI for the backend API.
- **Rationale**: FastAPI offers excellent performance, built-in OpenAPI documentation, data validation with Pydantic, and native async support. It's also well-suited for Python 3.12+ and has good integration with SQLAlchemy.
- **Consequences**: Faster development with automatic validation and documentation, but team members may need to learn FastAPI if they're more familiar with Flask or Django.
- **Status**: Accepted

### DEC-20250311-04
- **Date**: 2025-03-11
- **Title**: Authentication Mechanism
- **Context**: The system requires user authentication with admin approval.
- **Options**:
  1. JWT-based authentication
  2. Session-based authentication
  3. OAuth2 with external providers
- **Decision**: Implement JWT-based authentication with custom user approval workflow.
- **Rationale**: JWT provides a stateless authentication mechanism that works well with modern web applications and APIs. It's easy to implement, secure when properly configured, and doesn't require server-side session storage.
- **Consequences**: Requires careful implementation of token expiration and refresh mechanisms. Admin approval workflow will need to be custom-built.
- **Status**: Accepted

### DEC-20250311-05
- **Date**: 2025-03-11
- **Title**: RAG Implementation Approach
- **Context**: The project requires a hybrid RAG system combining BM25, vector search, and graph-based retrieval.
- **Options**:
  1. Use existing libraries (Langchain, LlamaIndex)
  2. Custom implementation with direct integration of components
  3. Hybrid approach with custom integration of specialized libraries
- **Decision**: Custom implementation with direct integration of specialized libraries.
- **Rationale**: This approach provides maximum flexibility and control over the RAG pipeline while leveraging well-established libraries for specific components (Pyserini for BM25, FAISS for vector search, NetworkX for graph). It avoids the overhead and constraints of higher-level frameworks.
- **Consequences**: Requires more implementation effort but results in a more tailored and efficient solution. May need more maintenance than using a higher-level framework.
- **Status**: Accepted

### DEC-20250311-06
- **Date**: 2025-03-11
- **Title**: External Embedding Models with FAISS Vector Storage
- **Context**: The Docker build was downloading large PyTorch packages due to sentence-transformers dependency, even though embedding models are intended to be hosted externally.
- **Options**:
  1. Keep sentence-transformers and FAISS for fully local embedding generation and search
  2. Use external models (Ollama/OpenAI) for embeddings but keep FAISS for vector storage/search
  3. Use external services for both embedding generation and vector search
- **Decision**: Use external models (Ollama/OpenAI) for embeddings but keep FAISS for vector storage/search.
- **Rationale**: This hybrid approach allows us to leverage external models for generating embeddings while maintaining control over vector storage and search with FAISS. This reduces some dependencies while preserving the ability to perform efficient vector search locally.
- **Consequences**: Reduced Docker image size by removing sentence-transformers, but still requires FAISS. Implementation will need to handle API communication with external services for embeddings while using FAISS for storage and retrieval.
- **Status**: Accepted
### DEC-20250311-07
- **Date**: 2025-03-11
- **Title**: SQLite Database Storage with Bind Mounts
- **Context**: The application was encountering SQLite database access errors in Docker containers due to file path and permission issues.
- **Options**:
  1. Use Docker volumes for database persistence
  2. Use bind mounts to map a local directory for database storage
  3. Store database in-memory (non-persistent)
- **Decision**: Use bind mounts to map a local directory for database storage.
- **Rationale**: Bind mounts provide a simple and transparent way to persist the SQLite database files while ensuring proper file access permissions. This approach makes it easy to access and back up the database files directly from the host system.
- **Consequences**: Database files will be stored in a local 'data' directory in the project root, which will be created automatically. This provides persistence between container restarts and makes database files directly accessible on the host system.
- **Status**: Accepted

### DEC-20250311-08
- **Date**: 2025-03-11
- **Title**: Frontend Build Container User Permissions
- **Context**: The frontend-build container was encountering permission errors when trying to create the node_modules directory during npm install.
- **Options**:
  1. Run the container as root user
  2. Run the container as user 1000 (typical first non-root user ID)
  3. Create a volume for node_modules
  4. Change permissions on the host directory
- **Decision**: Run the frontend-build container as user 1000.
- **Rationale**: Running as user 1000 typically matches the host system's user ID, providing sufficient permissions to access mounted volumes while being more secure than running as root. This approach avoids permission issues without compromising security.
- **Consequences**: The container will have appropriate access to the mounted volumes for development purposes. This approach balances security and functionality better than using root, while still being simpler than managing separate volumes for node_modules.
- **Status**: Accepted

### DEC-20250311-09
- **Date**: 2025-03-11
- **Title**: Frontend React Component Implementation
- **Context**: After fixing the Docker permission issues, we encountered TypeScript errors in the frontend build process and discovered missing React components referenced in App.tsx.
- **Options**:
  1. Remove references to missing components
  2. Create minimal placeholder components
  3. Implement fully functional components
- **Decision**: Implement fully functional React components for all missing pages.
- **Rationale**: Creating complete components provides a better foundation for the frontend development and ensures the application can be properly tested. This approach allows for a more realistic representation of the final product and facilitates further development.
- **Consequences**: The frontend now has a complete set of pages with proper TypeScript typing and React components. This provides a solid foundation for further frontend development and integration with the backend API.
- **Status**: Accepted

### DEC-20250311-10
- **Date**: 2025-03-11
- **Title**: Frontend Static File Serving Configuration
- **Context**: After fixing the Docker permission issues and implementing the missing React components, we encountered issues with serving the frontend static files from the FastAPI backend.
- **Options**:
  1. Use a separate web server for the frontend
  2. Fix the static file serving in the FastAPI application
  3. Implement a proxy server to handle both frontend and backend
- **Decision**: Fix the static file serving in the FastAPI application by using absolute paths and wrapping the React application with the AuthProvider.
- **Rationale**: This approach maintains the simplicity of the current architecture where the API server also serves the frontend static files. Using absolute paths ensures reliable file location in the Docker container, and wrapping the application with AuthProvider fixes React context errors.
- **Consequences**: The frontend is now properly served by the FastAPI backend, and the React application can access the authentication context. This approach simplifies deployment and development while ensuring proper functionality.
- **Status**: Accepted

---

### DEC-Template
### DEC-Template
- **Date**: YYYY-MM-DD
- **Title**: [Decision Title]
- **Context**: [Background and reason for decision]
- **Options**:
  1. [Option 1]
  2. [Option 2]
  3. [Option 3]
- **Decision**: [Chosen approach]
- **Rationale**: [Justification for the decision]
- **Consequences**: [Expected outcomes and impacts]
- **Status**: [Proposed/Accepted/Superseded/Deprecated]