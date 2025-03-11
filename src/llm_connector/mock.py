import asyncio
import random
from typing import Dict, List, Any, AsyncGenerator, Optional
import time

from src.llm_connector.base import BaseLLMConnector


class MockLLMConnector(BaseLLMConnector):
    """Mock LLM connector for development and testing."""
    
    def __init__(self, provider: str = "mock", model: str = "mock-model"):
        """
        Initialize the mock LLM connector.
        
        Args:
            provider: The provider name
            model: The model name
        """
        self.provider = provider
        self.model = model
        self.responses = {
            "greeting": "Hello! How can I assist you today?",
            "rag": "Based on the information provided, I can tell you that [RELEVANT FACT]. This is because [EXPLANATION].",
            "thinking": "Let me think about this...\n\n<think>I need to consider several factors here:\n1. The user's question is about [TOPIC]\n2. The relevant information mentions [DETAILS]\n3. The best approach is to [APPROACH]</think>\n\nAfter careful consideration, I believe that [ANSWER].",
            "code": "Here's a code example that might help:\n\n```python\ndef example_function(param1, param2):\n    \"\"\"Example function with docstring.\"\"\"\n    result = param1 + param2\n    return result\n```\n\nYou can use this function by calling `example_function(1, 2)` which would return `3`.",
            "error": "I apologize, but I encountered an error while processing your request. Please try again or rephrase your question.",
        }
    
    async def generate(
        self,
        system_message: Dict[str, str],
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Generate a mock response."""
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""
        
        # Select a response based on the message content
        response_text = self._select_response(last_message, system_message.get("content", ""))
        
        # Simulate token count
        tokens = len(response_text.split()) * 1.3
        
        return {
            "content": response_text,
            "tokens": int(tokens),
            "model": self.model,
            "provider": self.provider,
            "finish_reason": "stop",
        }
    
    async def generate_stream(
        self,
        system_message: Dict[str, str],
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream a mock response."""
        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""
        
        # Select a response based on the message content
        response_text = self._select_response(last_message, system_message.get("content", ""))
        
        # Split the response into words for streaming
        words = response_text.split()
        
        # Stream the response word by word
        buffer = ""
        for i, word in enumerate(words):
            # Add the word to the buffer
            if i > 0:
                buffer += " "
            buffer += word
            
            # Yield the word
            yield {
                "content": word + " " if i < len(words) - 1 else word,
                "tokens": 1,
                "model": self.model,
                "provider": self.provider,
                "finish_reason": None,
            }
            
            # Simulate typing delay
            await asyncio.sleep(0.05)
        
        # Yield the final chunk
        yield {
            "content": "",
            "tokens": 0,
            "model": self.model,
            "provider": self.provider,
            "finish_reason": "stop",
        }
    
    async def count_tokens(self, text: str) -> int:
        """Count tokens in a text (mock implementation)."""
        # Simple approximation: 1 token ≈ 0.75 words
        return int(len(text.split()) * 1.3)
    
    async def get_embedding(self, text: str) -> List[float]:
        """Get a mock embedding for a text."""
        # Generate a deterministic but seemingly random embedding based on the text
        random.seed(text)
        return [random.uniform(-1, 1) for _ in range(384)]
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get a list of available mock models."""
        return [
            {"id": "mock-gpt", "name": "Mock GPT", "provider": self.provider},
            {"id": "mock-llama", "name": "Mock Llama", "provider": self.provider},
            {"id": "mock-claude", "name": "Mock Claude", "provider": self.provider},
        ]
    
    def _select_response(self, user_message: str, system_message: str) -> str:
        """Select an appropriate mock response based on the user message."""
        user_message = user_message.lower()
        
        # Check for RAG context in system message
        has_context = "relevant information" in system_message.lower()
        
        if "hello" in user_message or "hi" in user_message:
            return self.responses["greeting"]
        elif "code" in user_message or "function" in user_message or "example" in user_message:
            return self.responses["code"]
        elif "think" in user_message or "reasoning" in user_message:
            return self.responses["thinking"]
        elif has_context or "document" in user_message:
            return self.responses["rag"]
        elif random.random() < 0.05:  # Occasionally return an error
            return self.responses["error"]
        else:
            # Default response with some randomization
            responses = list(self.responses.values())
            return random.choice(responses)