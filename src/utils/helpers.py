"""
Helper utility functions for the Expense Roaster
"""

import re
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime"""
    try:
        return pd.to_datetime(date_str)
    except:
        return None

def generate_id() -> str:
    """Generate a unique ID"""
    import uuid
    return str(uuid.uuid4())[:8]

def safe_json_loads(text: str) -> Optional[Dict]:
    """Safely parse JSON from text"""
    try:
        return json.loads(text)
    except:
        return None

def extract_numbers(text: str) -> List[float]:
    """Extract all numbers from text"""
    return [float(x) for x in re.findall(r'[\d,]+\.?\d*', text.replace(',', ''))]

def calculate_savings(current: float, suggested: float) -> Dict[str, Any]:
    """Calculate savings between current and suggested amounts"""
    savings = current - suggested
    percentage = (savings / current * 100) if current > 0 else 0
    return {
        'savings': savings,
        'percentage': percentage,
        'new_total': suggested,
        'current_total': current
    }

def get_date_range(days: int = 30) -> tuple:
    """Get date range for last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def is_valid_csv(content: bytes) -> bool:
    """Check if content is valid CSV"""
    try:
        pd.read_csv(pd.io.common.StringIO(content.decode('utf-8')))
        return True
    except:
        return False

def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """Safe division to avoid division by zero"""
    if denominator == 0:
        return default
    return numerator / denominator

def get_category_emoji(category: str) -> str:
    """Get emoji for category"""
    emoji_map = {
        'Food': '🍔',
        'Entertainment': '🎬',
        'Transport': '🚗',
        'Shopping': '🛍️',
        'Bills': '📄',
        'Healthcare': '🏥',
        'Education': '📚',
        'Rent': '🏠',
        'Insurance': '🛡️',
        'Other': '📌'
    }
    return emoji_map.get(category, '📌')

@st.cache_data(ttl=300)
def load_sample_data() -> pd.DataFrame:
    """Load sample data with caching"""
    from src.data.mock_data import generate_mock_data
    return generate_mock_data()