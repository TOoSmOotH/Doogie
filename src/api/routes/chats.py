from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from src.database import get_db, User, Chat, ChatMessage, MessageRole, MessageFeedback, FeedbackType
from src.api.schemas.chats import (
    ChatCreate, ChatResponse, ChatMessageCreate, ChatMessageResponse,
    MessageFeedbackCreate, MessageFeedbackResponse
)
from src.api.routes.auth import get_current_active_user
from src.core.chat_engine import process_message

# Router
router = APIRouter()


@router.get("/", response_model=List[ChatResponse])
async def get_user_chats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all chats for the current user."""
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).all()
    return chats


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new chat."""
    new_chat = Chat(
        user_id=current_user.id,
        title=chat_data.title or "New Chat",
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific chat."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    return chat


@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: str,
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a chat."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    chat.title = chat_data.title
    db.commit()
    db.refresh(chat)
    return chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a chat."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    db.delete(chat)
    db.commit()
    return None


@router.get("/{chat_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    chat_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all messages for a chat."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    messages = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at).all()
    return messages


@router.post("/{chat_id}/messages", response_model=ChatMessageResponse)
async def create_message(
    chat_id: str,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new message in a chat (non-streaming)."""
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    # Create user message
    user_message = ChatMessage(
        chat_id=chat_id,
        role=MessageRole.USER,
        content=message_data.content,
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    # Process message and get response
    response_content, thinking, tokens = await process_message(
        message_data.content,
        chat_id,
        current_user.id,
        db,
    )
    
    # Create assistant message
    assistant_message = ChatMessage(
        chat_id=chat_id,
        role=MessageRole.ASSISTANT,
        content=response_content,
        thinking=thinking,
        tokens=tokens,
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    
    return assistant_message


@router.post("/{chat_id}/messages/{message_id}/feedback", response_model=MessageFeedbackResponse)
async def create_message_feedback(
    chat_id: str,
    message_id: str,
    feedback_data: MessageFeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create or update feedback for a message."""
    # Verify chat belongs to user
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    # Verify message belongs to chat
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id, ChatMessage.chat_id == chat_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    
    # Check if feedback already exists
    feedback = db.query(MessageFeedback).filter(MessageFeedback.message_id == message_id).first()
    
    if feedback:
        # Update existing feedback
        feedback.feedback_type = FeedbackType(feedback_data.feedback_type)
        feedback.comment = feedback_data.comment
    else:
        # Create new feedback
        feedback = MessageFeedback(
            message_id=message_id,
            feedback_type=FeedbackType(feedback_data.feedback_type),
            comment=feedback_data.comment,
        )
        db.add(feedback)
    
    db.commit()
    db.refresh(feedback)
    return feedback


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: str,
    db: Session = Depends(get_db),
):
    """WebSocket endpoint for streaming chat messages."""
    await websocket.accept()
    
    try:
        # Authenticate user (simplified for now)
        # In production, use proper WebSocket authentication
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Create user message
            user_message = ChatMessage(
                chat_id=chat_id,
                role=MessageRole.USER,
                content=message_data.get("content", ""),
            )
            db.add(user_message)
            db.commit()
            
            # Process message and stream response
            async for chunk in process_message(
                message_data.get("content", ""),
                chat_id,
                message_data.get("user_id"),
                db,
                stream=True,
            ):
                await websocket.send_text(json.dumps(chunk))
            
            # Final message with complete response
            final_response = {
                "type": "complete",
                "message_id": "temp_id",  # Replace with actual ID in implementation
                "content": "Response placeholder",  # Replace with actual content
                "thinking": "Thinking placeholder",  # Replace with actual thinking
                "tokens": 0,  # Replace with actual token count
            }
            await websocket.send_text(json.dumps(final_response))
            
    except WebSocketDisconnect:
        # Handle disconnect
        pass