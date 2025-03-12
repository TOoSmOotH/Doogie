from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from .base import Base


def generate_uuid():
    """Generate a UUID string."""
    return str(uuid.uuid4())


class UserRole(enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"


class UserStatus(enum.Enum):
    """User status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    chats = relationship("Chat", back_populates="user")
    settings = relationship("UserSetting", back_populates="user", uselist=False)


class UserSetting(Base):
    """User-specific settings."""
    __tablename__ = "user_settings"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    theme = Column(String, default="dark")
    default_llm_provider = Column(String)
    default_ollama_model = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="settings")


class SystemSetting(Base):
    """System-wide settings."""
    __tablename__ = "system_settings"

    id = Column(String, primary_key=True, default=generate_uuid)
    key = Column(String, unique=True, index=True, nullable=False)
    value = Column(Text)
    is_encrypted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DocumentStatus(enum.Enum):
    """Document processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(enum.Enum):
    """Document type enumeration."""
    PDF = "pdf"
    DOCX = "docx"
    MARKDOWN = "md"
    RST = "rst"
    TEXT = "txt"
    HTML = "html"
    FORM = "form"


class DocumentSource(enum.Enum):
    """Document source enumeration."""
    UPLOAD = "upload"
    GITHUB = "github"
    WEBSITE = "website"
    MANUAL = "manual"


class Document(Base):
    """Document model for RAG system."""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_path = Column(String)
    url = Column(String)
    source = Column(Enum(DocumentSource), nullable=False)
    doc_type = Column(Enum(DocumentType), nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING)
    meta_data = Column(JSON)  # Renamed from metadata (reserved name in SQLAlchemy)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(String, ForeignKey("users.id"))

    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    """Document chunk model for RAG system."""
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, default=generate_uuid)
    document_id = Column(String, ForeignKey("documents.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    meta_data = Column(JSON)  # Renamed from metadata (reserved name in SQLAlchemy)
    embedding_file = Column(String)  # Path to embedding file
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    document = relationship("Document", back_populates="chunks")
    graph_nodes = relationship("GraphNode", back_populates="chunk", cascade="all, delete-orphan")


class GraphNode(Base):
    """Graph node model for GraphRAG."""
    __tablename__ = "graph_nodes"

    id = Column(String, primary_key=True, default=generate_uuid)
    chunk_id = Column(String, ForeignKey("document_chunks.id", ondelete="CASCADE"))
    node_type = Column(String, nullable=False)  # e.g., "entity", "concept", "document"
    name = Column(String, nullable=False)
    meta_data = Column(JSON)  # Renamed from metadata (reserved name in SQLAlchemy)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    chunk = relationship("DocumentChunk", back_populates="graph_nodes")
    source_edges = relationship("GraphEdge", foreign_keys="GraphEdge.source_id", back_populates="source")
    target_edges = relationship("GraphEdge", foreign_keys="GraphEdge.target_id", back_populates="target")


class GraphEdge(Base):
    """Graph edge model for GraphRAG."""
    __tablename__ = "graph_edges"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_id = Column(String, ForeignKey("graph_nodes.id", ondelete="CASCADE"))
    target_id = Column(String, ForeignKey("graph_nodes.id", ondelete="CASCADE"))
    relation_type = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    meta_data = Column(JSON)  # Renamed from metadata (reserved name in SQLAlchemy)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    source = relationship("GraphNode", foreign_keys=[source_id], back_populates="source_edges")
    target = relationship("GraphNode", foreign_keys=[target_id], back_populates="target_edges")


class Chat(Base):
    """Chat model for conversation history."""
    __tablename__ = "chats"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="chats")
    messages = relationship("ChatMessage", back_populates="chat", cascade="all, delete-orphan")


class MessageRole(enum.Enum):
    """Message role enumeration."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(Base):
    """Chat message model for conversation history."""
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    chat_id = Column(String, ForeignKey("chats.id", ondelete="CASCADE"))
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    thinking = Column(Text)  # For <think></think> content
    tokens = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    chat = relationship("Chat", back_populates="messages")
    feedback = relationship("MessageFeedback", back_populates="message", uselist=False)
    citations = relationship("MessageCitation", back_populates="message")


class FeedbackType(enum.Enum):
    """Feedback type enumeration."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class MessageFeedback(Base):
    """Message feedback model."""
    __tablename__ = "message_feedback"

    id = Column(String, primary_key=True, default=generate_uuid)
    message_id = Column(String, ForeignKey("chat_messages.id", ondelete="CASCADE"), unique=True)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    message = relationship("ChatMessage", back_populates="feedback")


class MessageCitation(Base):
    """Message citation model for tracking sources."""
    __tablename__ = "message_citations"

    id = Column(String, primary_key=True, default=generate_uuid)
    message_id = Column(String, ForeignKey("chat_messages.id", ondelete="CASCADE"))
    chunk_id = Column(String, ForeignKey("document_chunks.id"))
    relevance_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    message = relationship("ChatMessage", back_populates="citations")