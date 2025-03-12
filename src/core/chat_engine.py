from typing import List, Dict, Any, Optional, AsyncGenerator, Tuple, Union
from sqlalchemy.orm import Session
import re
import time
import asyncio

from src.database import User, Chat, ChatMessage, MessageRole, SystemSetting
from src.llm_connector.factory import get_llm_connector
from src.rag.retriever import retrieve_context


async def process_message(
    message: str,
    chat_id: str,
    user_id: str,
    db: Session,
    stream: bool = False,
) -> Union[AsyncGenerator[Dict[str, Any], None], Tuple[str, Optional[str], int]]:
    """
    Process a user message and generate a response.
    
    Args:
        message: The user's message
        chat_id: The ID of the chat
        user_id: The ID of the user
        db: Database session
        stream: Whether to stream the response
        
    Returns:
        If stream=True: An async generator yielding response chunks
        If stream=False: A tuple of (response_content, thinking_content, tokens)
    """
    # Get chat history
    history = db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).order_by(ChatMessage.created_at).all()
    
    # Get user settings
    user = db.query(User).filter(User.id == user_id).first()
    
    # Get system prompt
    system_prompt = db.query(SystemSetting).filter(SystemSetting.key == "default_system_prompt").first()
    system_prompt_content = system_prompt.value if system_prompt else "You are a helpful assistant."
    
    # Retrieve relevant context using RAG
    context_docs = await retrieve_context(message, db)
    
    # Format context for the prompt
    context_text = ""
    if context_docs:
        context_text = "### Relevant Information:\n"
        for i, doc in enumerate(context_docs):
            context_text += f"[{i+1}] {doc['content']}\n"
        context_text += "\n"
    
    # Get LLM connector based on user settings
    llm = get_llm_connector(user, db)
    
    # Format conversation history
    formatted_history = []
    for msg in history[-10:]:  # Limit to last 10 messages
        formatted_history.append({
            "role": msg.role.value,
            "content": msg.content
        })
    
    # Add system message with context
    system_message = {
        "role": "system",
        "content": f"{system_prompt_content}\n\n{context_text if context_text else ''}"
    }
    
    # Add user message
    formatted_history.append({
        "role": "user",
        "content": message
    })
    
    # Generate response
    if stream:
        return _stream_response(llm, system_message, formatted_history, context_docs)
    else:
        return await _generate_response(llm, system_message, formatted_history, context_docs)


async def _generate_response(
    llm,
    system_message: Dict[str, str],
    history: List[Dict[str, str]],
    context_docs: List[Dict[str, Any]],
) -> Tuple[str, Optional[str], int]:
    """Generate a complete response."""
    start_time = time.time()
    
    # Call LLM
    response = await llm.generate(system_message, history)
    
    # Extract thinking content if present
    thinking_content = None
    content = response["content"]
    
    # Check for thinking tags
    thinking_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
    if thinking_match:
        thinking_content = thinking_match.group(1).strip()
        # Remove thinking tags from content
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
    
    # Calculate tokens
    tokens = response.get("tokens", 0)
    
    # For development, simulate processing time
    if not tokens:
        await asyncio.sleep(1)
        tokens = len(content.split()) * 1.3  # Rough estimate
    
    return content, thinking_content, int(tokens)


async def _stream_response(
    llm,
    system_message: Dict[str, str],
    history: List[Dict[str, str]],
    context_docs: List[Dict[str, Any]],
) -> AsyncGenerator[Dict[str, Any], None]:
    """Stream the response in chunks."""
    start_time = time.time()
    thinking_buffer = ""
    content_buffer = ""
    in_thinking = False
    tokens = 0
    
    # Call LLM with streaming
    async for chunk in llm.generate_stream(system_message, history):
        tokens += chunk.get("tokens", 0)
        text = chunk.get("content", "")
        
        # Check for thinking tags
        if "<think>" in text:
            in_thinking = True
            text = text.replace("<think>", "")
        
        if "</think>" in text:
            in_thinking = False
            text = text.replace("</think>", "")
            # Send thinking update
            yield {
                "type": "thinking",
                "thinking": thinking_buffer,
            }
        
        # Add text to appropriate buffer
        if in_thinking:
            thinking_buffer += text
            yield {
                "type": "thinking",
                "thinking": thinking_buffer,
            }
        else:
            content_buffer += text
            yield {
                "type": "chunk",
                "content": text,
            }
    
    # For development, simulate processing time if no tokens
    if not tokens:
        await asyncio.sleep(0.5)
        tokens = len(content_buffer.split()) * 1.3  # Rough estimate
    
    # Send final complete message
    yield {
        "type": "complete",
        "content": content_buffer,
        "thinking": thinking_buffer if thinking_buffer else None,
        "tokens": int(tokens),
        "citations": [{"id": doc["id"], "title": doc["title"]} for doc in context_docs] if context_docs else None,
    }