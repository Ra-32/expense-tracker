"""
Abstract base class for LLM providers.
Enables easy switching between different AI models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class LLMResponse:
    """Standardized response format for all LLM providers"""
    content: str
    provider: str
    model: str
    raw_response: Optional[Any] = None
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        return self.error is None and self.content is not None

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 2048):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._client = None
    
    @abstractmethod
    def initialize_client(self) -> Any:
        """Initialize the provider's client"""
        pass
    
    @abstractmethod
    def generate_content(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generate content from the LLM"""
        pass
    
    @abstractmethod
    def generate_structured_output(self, prompt: str, output_schema: Dict) -> LLMResponse:
        """Generate structured output (JSON) from the LLM"""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in the text"""
        pass
    
    def get_provider_name(self) -> str:
        """Get the provider name"""
        return self.__class__.__name__.replace("Provider", "").lower()