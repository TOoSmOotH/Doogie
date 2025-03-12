from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class DocumentBase(BaseModel):
    """Base document schema."""
    title: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(None, alias="meta_data")
    
    class Config:
        populate_by_name = True


class DocumentCreate(DocumentBase):
    """Schema for document creation."""
    doc_type: str
    source: str
    url: Optional[str] = None


class DocumentUpdate(BaseModel):
    """Schema for document update."""
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(None, alias="meta_data")


class DocumentResponse(DocumentBase):
    """Schema for document response."""
    id: str
    doc_type: str
    source: str
    status: str
    file_path: Optional[str] = None
    url: Optional[str] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    id: str
    title: str
    file_name: str
    doc_type: str
    status: str


class DocumentProcessResponse(BaseModel):
    """Schema for document processing response."""
    id: str
    status: str
    message: str


class DocumentChunkBase(BaseModel):
    """Base document chunk schema."""
    content: str
    chunk_index: int
    metadata: Optional[Dict[str, Any]] = Field(None, alias="meta_data")
    
    class Config:
        populate_by_name = True


class DocumentChunkResponse(DocumentChunkBase):
    """Schema for document chunk response."""
    id: str
    document_id: str
    embedding_file: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class GraphNodeBase(BaseModel):
    """Base graph node schema."""
    node_type: str
    name: str
    metadata: Optional[Dict[str, Any]] = Field(None, alias="meta_data")
    
    class Config:
        populate_by_name = True


class GraphNodeResponse(GraphNodeBase):
    """Schema for graph node response."""
    id: str
    chunk_id: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class GraphEdgeBase(BaseModel):
    """Base graph edge schema."""
    source_id: str
    target_id: str
    relation_type: str
    weight: float = 1.0
    metadata: Optional[Dict[str, Any]] = Field(None, alias="meta_data")
    
    class Config:
        populate_by_name = True


class GraphEdgeResponse(GraphEdgeBase):
    """Schema for graph edge response."""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class SearchQuery(BaseModel):
    """Schema for search query."""
    query: str
    limit: int = 5
    use_hybrid: bool = True
    use_graph: bool = True
    use_reranker: bool = True


class SearchResult(BaseModel):
    """Schema for search result."""
    id: str
    content: str
    document_id: str
    document_title: str
    relevance: float
    source: str
    metadata: Optional[Dict[str, Any]] = Field(None, alias="meta_data")
    
    class Config:
        populate_by_name = True