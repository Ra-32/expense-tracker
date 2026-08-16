"""
Custom exceptions for the Expense Roaster application
"""

class ExpenseRoasterError(Exception):
    """Base exception for Expense Roaster"""
    pass

class DataValidationError(ExpenseRoasterError):
    """Raised when data validation fails"""
    pass

class LLMProviderError(ExpenseRoasterError):
    """Raised when LLM provider fails"""
    pass

class ConfigurationError(ExpenseRoasterError):
    """Raised when configuration is invalid"""
    pass

class DataProcessingError(ExpenseRoasterError):
    """Raised when data processing fails"""
    pass

class APIKeyMissingError(ExpenseRoasterError):
    """Raised when API key is missing"""
    pass