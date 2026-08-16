"""
Data processing utilities for expense analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from src.core.constants import WASTEFUL_CATEGORIES

class DataProcessor:
    """Handle all data processing and analysis"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self._validate_data()
    
    def _validate_data(self):
        """Validate and clean the DataFrame"""
        # Ensure required columns exist
        required_cols = ['Amount']
        for col in required_cols:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Convert Date column if exists
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Ensure Amount is numeric
        self.df['Amount'] = pd.to_numeric(self.df['Amount'], errors='coerce')
        
        # Drop rows with invalid amounts
        self.df = self.df.dropna(subset=['Amount'])
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive statistics"""
        total_spent = self.df['Amount'].sum()
        
        # Category analysis
        category_spending = self.df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        category_counts = self.df.groupby('Category').size()
        
        # Daily analysis
        if 'Date' in self.df.columns:
            daily_spending = self.df.groupby('Date')['Amount'].sum()
            avg_daily = daily_spending.mean()
            worst_day = daily_spending.idxmax()
            worst_day_amount = daily_spending.max()
            start_date = self.df['Date'].min()
            end_date = self.df['Date'].max()
        else:
            avg_daily = total_spent / len(self.df)
            worst_day = None
            worst_day_amount = 0
            start_date = None
            end_date = None
        
        # Wasteful spending
        wasteful_spending = self.df[self.df['Category'].isin(WASTEFUL_CATEGORIES)]['Amount'].sum()
        waste_percentage = (wasteful_spending / total_spent * 100) if total_spent > 0 else 0
        
        # Category breakdown string
        category_breakdown = ""
        for cat, amount in category_spending.items():
            percentage = (amount / total_spent * 100) if total_spent > 0 else 0
            category_breakdown += f"- {cat}: ₹{amount:,.2f} ({percentage:.1f}%)\n"
        
        return {
            'total_spent': total_spent,
            'avg_daily': avg_daily,
            'transaction_count': len(self.df),
            'category_spending': category_spending,
            'category_counts': category_counts,
            'daily_spending': daily_spending if 'Date' in self.df.columns else None,
            'worst_day': worst_day,
            'worst_day_amount': worst_day_amount,
            'start_date': start_date,
            'end_date': end_date,
            'wasteful_spending': wasteful_spending,
            'waste_percentage': waste_percentage,
            'category_breakdown': category_breakdown
        }
    
    def get_category_data(self) -> pd.DataFrame:
        """Get category-wise aggregation"""
        if 'Category' not in self.df.columns:
            self.df['Category'] = 'Other'
        
        return self.df.groupby('Category').agg({
            'Amount': ['sum', 'mean', 'count', 'max']
        }).round(2)
    
    def get_daily_trend(self) -> pd.DataFrame:
        """Get daily spending trend"""
        if 'Date' in self.df.columns:
            return self.df.groupby('Date')['Amount'].sum().reset_index()
        return pd.DataFrame()
    
    def get_top_expenses(self, n: int = 10) -> pd.DataFrame:
        """Get top N expenses"""
        return self.df.nlargest(n, 'Amount')
    
    def filter_by_category(self, categories: List[str]) -> 'DataProcessor':
        """Filter data by categories"""
        filtered_df = self.df[self.df['Category'].isin(categories)]
        return DataProcessor(filtered_df)
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> 'DataProcessor':
        """Filter data by date range"""
        if 'Date' in self.df.columns:
            mask = (self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)
            filtered_df = self.df[mask]
            return DataProcessor(filtered_df)
        return self