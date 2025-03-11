from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from src.database import User, UserSetting, SystemSetting
from src.llm_connector.base import BaseLLMConnector
from src.llm_connector.mock import MockLLMConnector
from src.utils.encryption import decrypt_value

# Import actual connectors when implemented
# from src.llm_connector.openai import OpenAIConnector
# from src.llm_connector.anthropic import AnthropicConnector
# from src.llm_connector.ollama import OllamaConnector
# from src.llm_connector.openrouter import OpenRouterConnector


def get_llm_connector(user: User, db: Session) -> BaseLLMConnector:
    """
    Get an LLM connector based on user settings.
    
    Args:
        user: The user
        db: Database session
        
    Returns:
        An LLM connector instance
    """
    # Get user settings
    user_settings = db.query(UserSetting).filter(UserSetting.user_id == user.id).first()
    
    # Default to mock connector for development
    provider = "mock"
    
    # If user has a preferred provider, use that
    if user_settings and user_settings.default_llm_provider:
        provider = user_settings.default_llm_provider
    
    # Get API keys and configuration from system settings
    api_keys = {}
    config = {}
    
    system_settings = db.query(SystemSetting).all()
    for setting in system_settings:
        if setting.key.startswith("api_key_"):
            # Decrypt API keys
            key_name = setting.key.replace("api_key_", "")
            api_keys[key_name] = decrypt_value(setting.value) if setting.is_encrypted else setting.value
        elif setting.key.startswith("llm_config_"):
            # Get configuration
            config_name = setting.key.replace("llm_config_", "")
            config[config_name] = setting.value
    
    # Create and return the appropriate connector
    if provider == "openai":
        # Return OpenAI connector when implemented
        # return OpenAIConnector(api_key=api_keys.get("openai"))
        return MockLLMConnector(provider="openai")
    
    elif provider == "anthropic":
        # Return Anthropic connector when implemented
        # return AnthropicConnector(api_key=api_keys.get("anthropic"))
        return MockLLMConnector(provider="anthropic")
    
    elif provider == "ollama":
        # Get Ollama model from user settings
        ollama_model = user_settings.default_ollama_model if user_settings else None
        ollama_model = ollama_model or "llama2"
        
        # Get Ollama server URL from config
        ollama_url = config.get("ollama_url", "http://localhost:11434")
        
        # Return Ollama connector when implemented
        # return OllamaConnector(base_url=ollama_url, model=ollama_model)
        return MockLLMConnector(provider="ollama", model=ollama_model)
    
    elif provider == "openrouter":
        # Return OpenRouter connector when implemented
        # return OpenRouterConnector(api_key=api_keys.get("openrouter"))
        return MockLLMConnector(provider="openrouter")
    
    else:
        # Default to mock connector
        return MockLLMConnector()


def get_embedding_model(db: Session) -> BaseLLMConnector:
    """
    Get an embedding model.
    
    Args:
        db: Database session
        
    Returns:
        An LLM connector instance for embeddings
    """
    # Get embedding model configuration from system settings
    embedding_provider = "mock"
    api_key = None
    
    embedding_provider_setting = db.query(SystemSetting).filter(SystemSetting.key == "embedding_provider").first()
    if embedding_provider_setting:
        embedding_provider = embedding_provider_setting.value
    
    api_key_setting = db.query(SystemSetting).filter(SystemSetting.key == f"api_key_{embedding_provider}").first()
    if api_key_setting:
        api_key = decrypt_value(api_key_setting.value) if api_key_setting.is_encrypted else api_key_setting.value
    
    # Create and return the appropriate connector
    if embedding_provider == "openai":
        # Return OpenAI connector when implemented
        # return OpenAIConnector(api_key=api_key)
        return MockLLMConnector(provider="openai")
    
    else:
        # Default to mock connector
        return MockLLMConnector()