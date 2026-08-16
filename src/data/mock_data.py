"""
Mock data generator for the Expense Roaster
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from src.core.constants import EXPENSE_CATEGORIES

def generate_mock_data(days: int = 30, transactions_per_day: int = 3) -> pd.DataFrame:
    """
    Generate realistic mock expense data
    
    Args:
        days: Number of days to generate
        transactions_per_day: Average transactions per day
    
    Returns:
        DataFrame with mock expense data
    """
    data = []
    start_date = datetime(2026, 1, 1)
    
    # Category-specific spending patterns
    category_patterns = {
        "Food": {"min": 100, "max": 600, "frequency": 0.35},
        "Entertainment": {"min": 200, "max": 1200, "frequency": 0.10},
        "Transport": {"min": 50, "max": 400, "frequency": 0.20},
        "Shopping": {"min": 300, "max": 1500, "frequency": 0.08},
        "Bills": {"min": 800, "max": 2500, "frequency": 0.05},
        "Healthcare": {"min": 100, "max": 800, "frequency": 0.05},
        "Education": {"min": 200, "max": 1000, "frequency": 0.07},
        "Rent": {"min": 5000, "max": 8000, "frequency": 0.03},
        "Insurance": {"min": 1000, "max": 3000, "frequency": 0.02},
        "Other": {"min": 50, "max": 500, "frequency": 0.05}
    }
    
    descriptions = {
        "Food": ["Lunch", "Dinner", "Groceries", "Coffee", "Snacks", "Restaurant", "Takeout"],
        "Entertainment": ["Movie", "Concert", "Gaming", "Netflix", "Spotify", "Event", "Party"],
        "Transport": ["Fuel", "Uber", "Bus", "Train", "Metro", "Parking", "Toll"],
        "Shopping": ["Clothes", "Accessories", "Electronics", "Books", "Home", "Gifts"],
        "Bills": ["Electricity", "Water", "Gas", "Internet", "Phone", "Maintenance"],
        "Healthcare": ["Medicine", "Doctor", "Pharmacy", "Insurance", "Checkup", "Dental"],
        "Education": ["Course", "Books", "Training", "Workshop", "Subscription", "Degree"],
        "Rent": ["Rent Payment"],
        "Insurance": ["Premium", "Renewal"],
        "Other": ["Miscellaneous", "Service", "Repair", "Fees"]
    }
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        
        # Weekend effect - more spending on weekends
        is_weekend = current_date.weekday() >= 5
        transactions = transactions_per_day + random.randint(-1, 1)
        if is_weekend:
            transactions += random.randint(1, 2)
        
        for _ in range(max(1, transactions)):
            # Select category based on frequency
            categories = list(category_patterns.keys())
            weights = [category_patterns[cat]["frequency"] for cat in categories]
            category = random.choices(categories, weights=weights)[0]
            
            # Generate amount
            pattern = category_patterns[category]
            amount = random.randint(pattern["min"], pattern["max"])
            
            # Weekend effect on amounts
            if is_weekend and category in ["Entertainment", "Food", "Shopping"]:
                amount *= random.uniform(1.2, 1.8)
            
            # Random descriptions
            desc = random.choice(descriptions.get(category, ["Expense"]))
            
            data.append({
                "Date": current_date,
                "Category": category,
                "Description": f"{desc} - {random.randint(100, 999)}",
                "Amount": round(amount, 2)
            })
    
    df = pd.DataFrame(data)
    
    # Add some large random expenses
    for _ in range(3):
        idx = random.randint(0, len(df) - 1)
        df.loc[idx, "Amount"] = random.randint(2000, 5000)
        df.loc[idx, "Category"] = random.choice(["Shopping", "Entertainment", "Food"])
    
    return df

def generate_advanced_mock_data() -> pd.DataFrame:
    """Generate more complex mock data with patterns"""
    df = generate_mock_data(days=45, transactions_per_day=3)
    
    # Add some recurring expenses
    for day in range(1, 31, 7):  # Weekly subscription
        date = datetime(2026, 1, 1) + timedelta(days=day)
        df = pd.concat([df, pd.DataFrame([{
            "Date": date,
            "Category": "Entertainment",
            "Description": "Weekly Subscription",
            "Amount": random.randint(200, 400)
        }])], ignore_index=True)
    
    # Monthly rent
    df = pd.concat([df, pd.DataFrame([{
        "Date": datetime(2026, 1, 5),
        "Category": "Rent",
        "Description": "Monthly Rent",
        "Amount": random.randint(6000, 8000)
    }])], ignore_index=True)
    
    return df.sort_values('Date').reset_index(drop=True)