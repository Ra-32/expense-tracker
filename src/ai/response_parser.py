"""
Response parsing utilities for AI-generated content.
Extracts structured data from LLM responses.
"""

import re
import pandas as pd
from typing import Optional, Dict, Any, List
import json

class ResponseParser:
    """Parse and extract structured data from AI responses"""
    
    @staticmethod
    def extract_recovery_table(text: str) -> Optional[pd.DataFrame]:
        """
        Extract recovery plan table from AI response
        
        Args:
            text: Full AI response text
        
        Returns:
            DataFrame with recovery plan or None
        """
        try:
            # Look for markdown table
            lines = text.split('\n')
            table_started = False
            table_rows = []
            headers = []
            
            for line in lines:
                line = line.strip()
                
                # Find table header
                if '| Category |' in line or '|Category|' in line:
                    # Extract headers
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 4:
                        headers = parts[:4]  # Category, Current, Suggested, Action
                    table_started = True
                    continue
                
                # Skip separator line
                if '|---' in line or '----------' in line:
                    continue
                
                # Extract data rows
                if table_started and line.startswith('|'):
                    parts = [p.strip() for p in line.split('|')[1:-1]]
                    if len(parts) >= 4:
                        # Clean the parts
                        cleaned = []
                        for part in parts[:4]:
                            # Remove ₹ and commas
                            cleaned_part = re.sub(r'[₹,]', '', part).strip()
                            cleaned.append(cleaned_part)
                        table_rows.append(cleaned)
                elif table_started and not line.startswith('|'):
                    # Table ended
                    break
            
            if table_rows:
                # Use headers if available, otherwise default
                if not headers:
                    headers = ['Category', 'Current Spend', 'Suggested Budget', 'Action Required']
                return pd.DataFrame(table_rows, columns=headers)
                
        except Exception as e:
            print(f"Error parsing table: {e}")
        
        return None
    
    @staticmethod
    def extract_metrics(text: str) -> Dict[str, Any]:
        """
        Extract key metrics from AI response
        
        Returns:
            Dictionary with extracted metrics
        """
        metrics = {}
        
        # Extract waste score
        waste_match = re.search(r'Waste Score[:\s]+([A-F])', text, re.IGNORECASE)
        if waste_match:
            metrics['waste_score'] = waste_match.group(1)
        
        # Extract savings amounts
        savings_match = re.search(r'Monthly Savings[:\s]+₹?([\d,]+)', text)
        if savings_match:
            metrics['monthly_savings'] = float(savings_match.group(1).replace(',', ''))
        
        annual_match = re.search(r'Annual Savings[:\s]+₹?([\d,]+)', text)
        if annual_match:
            metrics['annual_savings'] = float(annual_match.group(1).replace(',', ''))
        
        # Extract new budget
        budget_match = re.search(r'New Monthly Budget[:\s]+₹?([\d,]+)', text)
        if budget_match:
            metrics['new_budget'] = float(budget_match.group(1).replace(',', ''))
        
        return metrics
    
    @staticmethod
    def extract_action_items(text: str) -> List[str]:
        """
        Extract action items from AI response
        
        Returns:
            List of action items
        """
        actions = []
        
        # Find action items section
        action_section = re.search(r'ACTION ITEMS[:\s]*(.*?)(?=\n\n|\Z)', text, re.DOTALL)
        if action_section:
            action_text = action_section.group(1)
            # Extract bullet points
            items = re.findall(r'[-•*]\s*(.*?)(?=\n|$)', action_text)
            actions = [item.strip() for item in items if item.strip()]
        
        return actions[:3]  # Max 3 action items
    
    @staticmethod
    def parse_json_response(text: str) -> Optional[Dict]:
        """
        Parse JSON from AI response
        
        Args:
            text: Response text that may contain JSON
        
        Returns:
            Parsed JSON or None
        """
        try:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try direct parsing
            return json.loads(text)
        except:
            return None