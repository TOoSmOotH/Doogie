from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatBase(BaseModel):
    """Base chat schema."""
    title: Optional[str] = "New Chat"


class ChatCreate(ChatBase):
    """Schema for chat creation."""
    pass


class ChatResponse(ChatBase):
    """Schema for chat response."""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageBase(BaseModel):
    """Base chat message schema."""
    content: str
    role: str = "user"


class ChatMessageCreate(ChatMessageBase):
    """Schema for chat message creation."""
    pass


class ChatMessageResponse(ChatMessageBase):
    """Schema for chat message response."""
    id: str
    chat_id: str
    thinking: Optional[str] = None
    tokens: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageFeedbackBase(BaseModel):
    """Base message feedback schema."""
    feedback_type: str
    comment: Optional[str] = None


class MessageFeedbackCreate(MessageFeedbackBase):
    """Schema for message feedback creation."""
    pass


class MessageFeedbackResponse(MessageFeedbackBase):
    """Schema for message feedback response."""
    id: str
    message_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCitationBase(BaseModel):
    """Base message citation schema."""
    chunk_id: str
    relevance_score: Optional[float] = None


class MessageCitationResponse(MessageCitationBase):
    """Schema for message citation response."""
    id: str
    message_id: str
    created_at: datetime
    
    # Include document information
    document_title: Optional[str] = None
    document_source: Optional[str] = None
    chunk_content: Optional[str] = None

    class Config:
        from_attributes = True


class StreamingResponse(BaseModel):
    """Schema for streaming response."""
    type: str  # "chunk", "thinking", "complete"
    content: Optional[str] = None
    thinking: Optional[str] = None
    message_id: Optional[str] = None
    tokens: Optional[int] = None
    citations: Optional[List[Dict[str, Any]]] = None