"""
Configuration management for the Expense Roaster application.
Supports environment variables, secrets, and easy model switching.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """Application configuration manager"""
    
    # LLM Provider Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # gemini, groq, openai
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    
    # Model Names
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # API Settings
    API_TEMPERATURE = float(os.getenv("API_TEMPERATURE", 0.7))
    API_MAX_TOKENS = int(os.getenv("API_MAX_TOKENS", 2048))
    
    # App Settings
    APP_NAME = os.getenv("APP_NAME", "Expense Roaster")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    @classmethod
    def get_api_key(cls, provider: Optional[str] = None) -> str:
        """Get API key for specified provider"""
        provider = provider or cls.LLM_PROVIDER
        
        if provider == "gemini":
            if not cls.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not configured")
            return cls.GEMINI_API_KEY
        elif provider == "groq":
            if not cls.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not configured")
            return cls.GROQ_API_KEY
        elif provider == "openai":
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")
            return cls.OPENAI_API_KEY
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @classmethod
    def get_model(cls, provider: Optional[str] = None) -> str:
        """Get model name for specified provider"""
        provider = provider or cls.LLM_PROVIDER
        
        models = {
            "gemini": cls.GEMINI_MODEL,
            "groq": cls.GROQ_MODEL,
            "openai": cls.OPENAI_MODEL
        }
        return models.get(provider, cls.GEMINI_MODEL)

def setup_environment():
    """Setup environment variables and validate configuration"""
    # Validate API keys based on provider
    provider = Config.LLM_PROVIDER
    
    if provider == "gemini" and not Config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is required when using Gemini provider")
    elif provider == "groq" and not Config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is required when using Groq provider")
    elif provider == "openai" and not Config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
    
    return Config