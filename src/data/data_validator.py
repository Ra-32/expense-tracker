"""
Data validation utilities for expense data
"""

import pandas as pd
from typing import Tuple, List, Optional

class DataValidator:
    """Validate and clean expense data"""
    
    REQUIRED_COLUMNS = ['Amount']
    OPTIONAL_COLUMNS = ['Date', 'Category', 'Description']
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.errors = []
    
    def validate_expense_data(self) -> Tuple[bool, List[str]]:
        """
        Validate the expense DataFrame
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        self.errors = []
        
        # Check for empty DataFrame
        if self.df.empty:
            self.errors.append("DataFrame is empty")
            return False, self.errors
        
        # Check required columns
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        if missing_cols:
            self.errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        
        # Check amount column
        if 'Amount' in self.df.columns:
            # Check for non-numeric values
            non_numeric = self.df[~pd.to_numeric(self.df['Amount'], errors='coerce').notna()]
            if not non_numeric.empty:
                self.errors.append(f"Found {len(non_numeric)} non-numeric values in 'Amount' column")
            
            # Check for negative amounts
            negative = self.df[self.df['Amount'] < 0]
            if not negative.empty:
                self.errors.append(f"Found {len(negative)} negative amounts")
        
        # Check category column
        if 'Category' in self.df.columns:
            # Check for missing categories
            missing_cats = self.df['Category'].isna().sum()
            if missing_cats > 0:
                self.errors.append(f"Found {missing_cats} rows with missing categories")
        
        return len(self.errors) == 0, self.errors
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and prepare the DataFrame"""
        df = self.df.copy()
        
        # Ensure Amount is numeric
        if 'Amount' in df.columns:
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            df = df.dropna(subset=['Amount'])
            df['Amount'] = df['Amount'].abs()  # Convert negative to positive
        
        # Fill missing categories
        if 'Category' in df.columns:
            df['Category'] = df['Category'].fillna('Other')
        
        # Convert Date to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Sort by date
        if 'Date' in df.columns:
            df = df.sort_values('Date')
        
        return df.reset_index(drop=True)
    
    def get_data_quality_report(self) -> dict:
        """Generate a data quality report"""
        report = {
            'total_rows': len(self.df),
            'missing_values': self.df.isna().sum().to_dict(),
            'numeric_columns': self.df.select_dtypes(include=['float64', 'int64']).columns.tolist(),
            'categorical_columns': self.df.select_dtypes(include=['object']).columns.tolist(),
            'date_columns': self.df.select_dtypes(include=['datetime64']).columns.tolist(),
            'unique_categories': len(self.df['Category'].unique()) if 'Category' in self.df.columns else 0,
            'total_amount': self.df['Amount'].sum() if 'Amount' in self.df.columns else 0
        }
        return report