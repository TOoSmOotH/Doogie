from abc import ABC, abstractmethod
from typing import Dict, List, Any, AsyncGenerator, Optional


class BaseLLMConnector(ABC):
    """Base class for LLM connectors."""
    
    @abstractmethod
    async def generate(
        self,
        system_message: Dict[str, str],
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a response from the LLM.
        
        Args:
            system_message: The system message
            messages: The conversation history
            temperature: The temperature for generation
            max_tokens: The maximum number of tokens to generate
            
        Returns:
            A dictionary containing the response content and metadata
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        system_message: Dict[str, str],
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream a response from the LLM.
        
        Args:
            system_message: The system message
            messages: The conversation history
            temperature: The temperature for generation
            max_tokens: The maximum number of tokens to generate
            
        Yields:
            Dictionaries containing response chunks and metadata
        """
        pass
    
    @abstractmethod
    async def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            The number of tokens
        """
        pass
    
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """
        Get an embedding for a text.
        
        Args:
            text: The text to get an embedding for
            
        Returns:
            The embedding as a list of floats
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of available models.
        
        Returns:
            A list of dictionaries containing model information
        """
        pass