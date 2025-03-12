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

### DEC-20250311-11
- **Date**: 2025-03-11
- **Title**: RAG System Implementation Strategy
- **Context**: For Phase 2, we needed to implement the core RAG components including document processing, BM25 indexing, vector search, graph-based retrieval, and neural reranking.
- **Options**:
  1. Use existing libraries like LangChain or LlamaIndex for all RAG components
  2. Implement custom solutions for all components from scratch
  3. Use specialized libraries for each component with custom integration
- **Decision**: Use specialized libraries for each component with custom integration (Pyserini for BM25, FAISS for vector search, NetworkX for graph-based retrieval, and cross-encoder models for reranking).
- **Rationale**: This approach provides more control and flexibility than using high-level frameworks while leveraging well-established libraries for specific components. It allows for better optimization and customization for our specific needs.
- **Consequences**: The implementation is more tailored to our requirements and avoids dependencies on high-level frameworks that might change. However, it requires more integration work and maintenance.
- **Status**: Accepted

### DEC-20250311-12
- **Date**: 2025-03-11
- **Title**: Document Chunking Strategy
- **Context**: Different document types require different chunking strategies for optimal retrieval.
- **Options**:
  1. Use a single chunking strategy for all document types
  2. Implement document type-specific chunking strategies
  3. Use semantic chunking based on content analysis
- **Decision**: Implement document type-specific chunking strategies (e.g., heading-based for Markdown/RST, page-based for PDFs, paragraph-based for general text).
- **Rationale**: Different document types have different structural elements that can be leveraged for more meaningful chunking. This approach preserves the logical structure of documents while ensuring chunks are of appropriate size for retrieval.
- **Consequences**: More complex chunking logic but better retrieval quality. The system can now handle various document types more effectively, preserving their semantic structure.
- **Status**: Accepted

### DEC-20250311-13
- **Date**: 2025-03-11
- **Title**: Authentication Security Enhancements
- **Context**: The initial authentication system used hardcoded secrets and lacked password reset functionality.
- **Options**:
  1. Keep the simple authentication system for development
  2. Implement environment variable-based secrets and add password reset
  3. Use a third-party authentication service
- **Decision**: Implement environment variable-based secrets and add password reset functionality.
- **Rationale**: This approach improves security while maintaining control over the authentication system. Using environment variables for secrets follows security best practices, and password reset is an essential feature for user experience.
- **Consequences**: More secure authentication system with better user experience. The implementation is more complex but provides necessary security features for a production system.
- **Status**: Accepted

### DEC-20250311-14
- **Date**: 2025-03-11
- **Title**: Pure Python BM25 Implementation
- **Context**: The application was failing to start due to Pyserini being unable to find the Java JDK, which is required for its BM25 indexing functionality.
- **Options**:
  1. Install OpenJDK in the Docker container
  2. Use a different BM25 implementation that doesn't require Java
  3. Remove BM25 indexing functionality
- **Decision**: Replace Pyserini with the pure Python rank_bm25 library for BM25 indexing.
- **Rationale**: This approach eliminates the Java dependency while maintaining BM25 functionality. The rank_bm25 library is a lightweight, pure Python implementation that provides similar functionality without requiring external dependencies like the JDK.
- **Consequences**: Potentially different performance characteristics compared to Pyserini, but avoids adding a large dependency (JDK) to the Docker image. The implementation is simpler and more consistent with the rest of the Python codebase.
- **Status**: Accepted

### DEC-20250311-15
- **Date**: 2025-03-11
- **Title**: bcrypt Version Compatibility Fix
- **Context**: The application was encountering an error during user registration due to a compatibility issue between passlib and bcrypt libraries.
- **Options**:
  1. Pin bcrypt to a specific version known to work with passlib
  2. Update passlib to a version compatible with the latest bcrypt
  3. Replace the authentication system with a different implementation
- **Decision**: Pin bcrypt to version 4.0.1 in requirements.txt.
- **Rationale**: This is the simplest and most direct solution to the compatibility issue. Version 4.0.1 of bcrypt is known to work well with passlib and doesn't require changes to the existing authentication code.
- **Consequences**: Ensures proper functionality of the user registration and authentication system. May require monitoring for future updates to either library to maintain compatibility.
- **Status**: Accepted

### DEC-20250311-16
- **Date**: 2025-03-11
- **Title**: Authentication System Enhancements
- **Context**: The application was encountering 400 Bad Request errors during user registration and login due to incorrect request formatting and schema inconsistencies.
- **Options**:
  1. Update frontend authentication requests to match backend expectations
  2. Modify backend to accept different request formats
  3. Implement a middleware to handle format conversion
  4. Enhance schema validation and error logging
- **Decision**: Implement a comprehensive fix including frontend request formatting, schema improvements, enhanced error logging, and improved error handling.
- **Rationale**: A multi-faceted approach addresses several potential issues simultaneously. The frontend now correctly formats requests, the backend schemas are more consistent and explicit, detailed logging helps identify issues, and specific error messages are properly displayed to users.
- **Consequences**: Improved reliability and user experience of the authentication system. The login now uses form data with the correct Content-Type header for the OAuth2 token endpoint, registration uses JSON with the appropriate Content-Type header, schemas properly validate required fields, and users receive clear feedback about registration issues (such as when an email is already registered).
- **Status**: Accepted

### DEC-20250312-01
- **Date**: 2025-03-12
- **Title**: Frontend Development Workflow Enhancement
- **Context**: The current Docker setup doesn't automatically reflect UI changes because the frontend-build container runs once at startup, builds the frontend, and exits. This requires manual rebuilds to see UI changes.
- **Options**:
  1. Add a dedicated frontend development container with hot reloading
  2. Implement a manual rebuild process with documented commands
  3. Modify the build container to use watch mode and stay running
- **Decision**: Add a dedicated frontend development container with hot reloading (Option 1).
- **Rationale**: This approach provides the best developer experience by enabling immediate feedback on UI changes. It separates development and production builds, allowing for a more efficient workflow while maintaining the existing production build process.
- **Consequences**: Developers will need to run an additional container during development, but will benefit from immediate UI updates without manual rebuilds. The development and production environments remain clearly separated, which helps prevent development-only code from affecting production.
- **Status**: Accepted

### DEC-20250312-02
- **Date**: 2025-03-12
- **Title**: UI Theme Implementation and Modernization
- **Context**: The UI theme implementation was inconsistent, with issues in multiple places: the Settings page had components hardcoded with light theme styles, and the index.html file had hardcoded dark theme classes in the body tag. Additionally, the overall UI design lacked a modern, professional appearance.
- **Options**:
  1. Create a separate theme file with all theme variables
  2. Update individual components to properly respect the theme context
  3. Implement a global CSS approach with theme classes
  4. Completely redesign the UI with a new framework
- **Decision**: Update individual components to properly respect the theme context, remove hardcoded theme classes, and modernize the UI design with a Claude-inspired interface (Option 2 with UI modernization).
- **Rationale**: This approach provides an immediate fix without requiring a major refactoring of the theme system or switching frameworks. It ensures that all UI components properly check the current theme value and apply appropriate styles, while removing any hardcoded theme classes that would override the theme system. The modernized UI design provides a more professional and contemporary look that enhances user experience.
- **Consequences**: Improved UI consistency with proper dark/light theme support and a more professional appearance. The Settings page now correctly displays in dark mode when selected, and the application properly respects the user's theme preference without being overridden by hardcoded classes. The updated color scheme, spacing, and component styling create a more modern interface similar to popular AI applications. This approach may require similar updates to other components as they are developed.
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