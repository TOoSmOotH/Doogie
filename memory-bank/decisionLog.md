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

---

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