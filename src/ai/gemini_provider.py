"""
Google Gemini API implementation
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
from src.ai.base_llm import BaseLLMProvider, LLMResponse
import json

class GeminiProvider(BaseLLMProvider):
    """Gemini API provider implementation"""
    
    def initialize_client(self) -> Any:
        """Initialize Gemini client"""
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(self.model)
    
    def _get_client(self):
        """Lazy initialization of client"""
        if self._client is None:
            self._client = self.initialize_client()
        return self._client
    
    def generate_content(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generate content using Gemini"""
        try:
            client = self._get_client()
            
            # Prepare the full prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate response
            response = client.generate_content(
                full_prompt,
                generation_config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_tokens,
                }
            )
            
            return LLMResponse(
                content=response.text,
                provider="gemini",
                model=self.model,
                raw_response=response
            )
            
        except Exception as e:
            return LLMResponse(
                content="",
                provider="gemini",
                model=self.model,
                error=str(e)
            )
    
    def generate_structured_output(self, prompt: str, output_schema: Dict) -> LLMResponse:
        """Generate structured JSON output"""
        try:
            client = self._get_client()
            
            # Create a prompt that requests JSON output
            json_prompt = f"""
            You must respond with valid JSON only. Follow this exact schema:
            {json.dumps(output_schema, indent=2)}
            
            {prompt}
            """
            
            response = client.generate_content(
                json_prompt,
                generation_config={
                    "temperature": 0.1,  # Lower temperature for structured output
                    "max_output_tokens": self.max_tokens,
                    "response_mime_type": "application/json"
                }
            )
            
            return LLMResponse(
                content=response.text,
                provider="gemini",
                model=self.model,
                raw_response=response
            )
            
        except Exception as e:
            return LLMResponse(
                content="",
                provider="gemini",
                model=self.model,
                error=str(e)
            )
    
    def count_tokens(self, text: str) -> int:
        """Count tokens using Gemini's tokenizer"""
        try:
            client = self._get_client()
            result = client.count_tokens(text)
            return result.total_tokens
        except:
            # Fallback: rough estimate
            return len(text.split()) * 1.3