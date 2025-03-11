import { get, post, put, del } from './client';
import axios from 'axios';

// Types
export interface Document {
  id: string;
  title: string;
  description?: string;
  doc_type: string;
  source: string;
  status: string;
  file_path?: string;
  url?: string;
  created_by?: string;
  created_at: string;
  updated_at: string;
  metadata?: Record<string, any>;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  content: string;
  chunk_index: number;
  metadata?: Record<string, any>;
  embedding_file?: string;
  created_at: string;
}

export interface DocumentCreateRequest {
  title: string;
  description?: string;
  doc_type: string;
  source: string;
  url?: string;
  metadata?: Record<string, any>;
}

export interface DocumentUpdateRequest {
  title?: string;
  description?: string;
  metadata?: Record<string, any>;
}

export interface DocumentUploadResponse {
  id: string;
  title: string;
  file_name: string;
  doc_type: string;
  status: string;
}

export interface DocumentProcessResponse {
  id: string;
  status: string;
  message: string;
}

export interface SearchQuery {
  query: string;
  limit?: number;
  use_hybrid?: boolean;
  use_graph?: boolean;
  use_reranker?: boolean;
}

export interface SearchResult {
  id: string;
  content: string;
  document_id: string;
  document_title: string;
  relevance: number;
  source: string;
  metadata?: Record<string, any>;
}

// Document API services
export const documentService = {
  // Get all documents
  getDocuments: async (
    skip: number = 0,
    limit: number = 100,
    status?: string
  ): Promise<Document[]> => {
    const params: Record<string, any> = { skip, limit };
    if (status) {
      params.status = status;
    }
    return get<Document[]>('/documents', { params });
  },

  // Get a specific document
  getDocument: async (documentId: string): Promise<Document> => {
    return get<Document>(`/documents/${documentId}`);
  },

  // Create a new document (for manual entry or URL)
  createDocument: async (data: DocumentCreateRequest): Promise<Document> => {
    return post<Document>('/documents', data);
  },

  // Update a document
  updateDocument: async (
    documentId: string,
    data: DocumentUpdateRequest
  ): Promise<Document> => {
    return put<Document>(`/documents/${documentId}`, data);
  },

  // Delete a document
  deleteDocument: async (documentId: string): Promise<void> => {
    return del<void>(`/documents/${documentId}`);
  },

  // Upload a document file
  uploadDocument: async (
    file: File,
    title: string,
    description?: string
  ): Promise<DocumentUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    
    if (description) {
      formData.append('description', description);
    }

    const response = await axios.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });

    return response.data;
  },

  // Process or reprocess a document
  processDocument: async (documentId: string): Promise<DocumentProcessResponse> => {
    return post<DocumentProcessResponse>(`/documents/${documentId}/process`);
  },

  // Reset the entire RAG system
  resetRAG: async (): Promise<{ message: string }> => {
    return post<{ message: string }>('/documents/reset');
  },

  // Search documents
  search: async (searchQuery: SearchQuery): Promise<SearchResult[]> => {
    return post<SearchResult[]>('/rag/search', searchQuery);
  },

  // Get RAG status
  getRAGStatus: async (): Promise<any> => {
    return get<any>('/rag/status');
  },
};

export default documentService;