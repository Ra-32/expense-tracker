"""
Groq API implementation
"""

from groq import Groq
from src.ai.base_llm import BaseLLMProvider, LLMResponse
import json

class GroqProvider(BaseLLMProvider):
    """Groq API provider implementation"""
    
    def initialize_client(self):
        """Initialize Groq client"""
        return Groq(api_key=self.api_key)
    
    def _get_client(self):
        if self._client is None:
            self._client = self.initialize_client()
        return self._client
    
    def generate_content(self, prompt: str, system_prompt: str = None) -> LLMResponse:
        try:
            client = self._get_client()
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                provider="groq",
                model=self.model,
                raw_response=response
            )
        except Exception as e:
            return LLMResponse(
                content="",
                provider="groq",
                model=self.model,
                error=str(e)
            )
    
    def generate_structured_output(self, prompt: str, output_schema: dict) -> LLMResponse:
        # Add structured output logic for Groq
        pass
    
    def count_tokens(self, text: str) -> int:
        # Rough estimate
        return len(text.split()) * 1.3