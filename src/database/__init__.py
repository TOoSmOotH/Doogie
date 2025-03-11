from .base import Base, engine, get_db, SessionLocal
from .models import (
    User, UserRole, UserStatus, UserSetting,
    SystemSetting,
    Document, DocumentStatus, DocumentType, DocumentSource, DocumentChunk,
    GraphNode, GraphEdge,
    Chat, ChatMessage, MessageRole,
    MessageFeedback, FeedbackType,
    MessageCitation
)

# Create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)