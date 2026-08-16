"""
Application constants and configuration
"""

from typing import Dict, List

# App Configuration
APP_CONFIG: Dict = {
    "title": "💰 The Expense Roaster 🔥",
    "icon": "💰",
    "layout": "wide",
    "sidebar_state": "expanded",
    "version": "2.0.0"
}

# Expense Categories
EXPENSE_CATEGORIES: List[str] = [
    "Food", 
    "Entertainment", 
    "Transport", 
    "Shopping", 
    "Bills", 
    "Healthcare", 
    "Education",
    "Rent",
    "Insurance",
    "Other"
]

# Category Colors for Visualization
CATEGORY_COLORS: Dict[str, str] = {
    "Food": "#FF6B6B",
    "Entertainment": "#FFA94D",
    "Transport": "#FFD93D",
    "Shopping": "#6BCB77",
    "Bills": "#4D96FF",
    "Healthcare": "#9B59B6",
    "Education": "#FF6B9D",
    "Rent": "#00D2D3",
    "Insurance": "#54A0FF",
    "Other": "#8395A7"
}

# Wasteful Categories (for roasting)
WASTEFUL_CATEGORIES: List[str] = ["Entertainment", "Shopping", "Food"]

# Date Range
DEFAULT_START_DATE = "2026-01-01"
DEFAULT_END_DATE = "2026-01-30"

# UI Messages
MESSAGES: Dict[str, str] = {
    "welcome_title": "👋 Welcome to The Expense Roaster!",
    "welcome_subtitle": "Upload your expenses and get brutally roasted by AI, then recover like a pro.",
    "no_data": "Upload your expense CSV or generate sample data from the sidebar.",
    "loading": "🧠 Analyzing your spending habits...",
    "error_upload": "⚠️ Please upload a valid CSV file with 'Amount' column.",
    "success_upload": "✅ Successfully loaded {count} transactions.",
    "data_stays_local": "🔒 Your data stays in your browser session and is never stored."
}

# Financial Thresholds
FINANCIAL_THRESHOLDS: Dict[str, float] = {
    "high_risk_daily_spend": 5000,
    "medium_risk_daily_spend": 3000,
    "warning_waste_percent": 30
}