"""
Factory pattern for creating LLM providers.
Enables easy switching between models with a single configuration change.
"""

from typing import Dict, Type
from src.ai.base_llm import BaseLLMProvider
from src.ai.gemini_provider import GeminiProvider
from src.core.config import Config

class LLMFactory:
    """Factory for creating LLM provider instances"""
    
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "gemini": GeminiProvider,
        # "groq": GroqProvider,  # Uncomment when implemented
        # "openai": OpenAIProvider,  # Uncomment when implemented
    }
    
    @classmethod
    def create_provider(cls, provider_name: str = None) -> BaseLLMProvider:
        """
        Create an LLM provider instance
        
        Args:
            provider_name: Name of the provider (gemini, groq, openai)
                          If None, uses the configured default
        
        Returns:
            BaseLLMProvider instance
        """
        provider_name = provider_name or Config.LLM_PROVIDER
        
        if provider_name not in cls._providers:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        provider_class = cls._providers[provider_name]
        api_key = Config.get_api_key(provider_name)
        model = Config.get_model(provider_name)
        
        return provider_class(
            api_key=api_key,
            model=model,
            temperature=Config.API_TEMPERATURE,
            max_tokens=Config.API_MAX_TOKENS
        )

# Singleton instance for easy access
def get_llm_provider() -> BaseLLMProvider:
    """Get the configured LLM provider instance"""
    return LLMFactory.create_provider()