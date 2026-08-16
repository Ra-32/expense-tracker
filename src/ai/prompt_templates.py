"""
Prompt templates and system prompts for the Expense Roaster.
Centralized location for all AI prompts to enable easy tuning.
"""

from typing import Dict, Any
import json

class PromptTemplates:
    """Collection of prompt templates for different use cases"""
    
    SYSTEM_PROMPTS = {
        "expense_roaster": """You are a brutally honest, hilarious, and slightly aggressive financial advisor called "The Expense Roaster." 
Your personality is:
- Savage but helpful
- Uses humor to make a point
- Cites specific numbers and percentages
- Provides actionable advice

Your responses must be:
1. Entertaining and memorable
2. Data-driven and specific
3. Constructive despite the roast
4. Professional in the recovery section
"""
    }
    
    @staticmethod
    def get_roast_prompt(data_stats: Dict[str, Any]) -> str:
        """
        Generate the roast prompt with dynamic data injection
        
        Args:
            data_stats: Dictionary containing expense statistics
        
        Returns:
            Formatted prompt string
        """
        category_summary = data_stats.get("category_breakdown", "")
        
        prompt = f"""
Analyze this person's spending data and provide a brutal roast with a recovery plan:

**Spending Summary:**
- Total Spent: ₹{data_stats.get('total_spent', 0):,.2f}
- Average Daily Spend: ₹{data_stats.get('avg_daily', 0):,.2f}
- Number of Transactions: {data_stats.get('transaction_count', 0)}
- Period: {data_stats.get('start_date', 'N/A')} to {data_stats.get('end_date', 'N/A')}

**Waste Analysis:**
- Worst Day: {data_stats.get('worst_day', 'N/A')} - ₹{data_stats.get('worst_day_amount', 0):,.2f}
- Wasted Discretionary Spend: ₹{data_stats.get('wasteful_spending', 0):,.2f}
- Waste Percentage: {data_stats.get('waste_percentage', 0):.1f}%

**Category Breakdown:**
{category_summary}

**Your Response Must Follow This EXACT Structure:**

### 🔥 THE ROAST
[4-5 sentences that are brutally honest, funny, and specific. Call out their worst habit.]

### 📊 SPENDING DIAGNOSIS
- **Worst Category:** [Name] - ₹[Amount] ([Percentage]% of total)
- **Daily Habit:** [Comment on daily average vs typical]
- **Biggest Red Flag:** [Specific observation with number]
- **Waste Score:** [A/F/B/C/D] - [One sentence explanation]

### 📋 STRICT RECOVERY PLAN
| Category | Current Spend | Suggested Budget | Action Required |
|----------|---------------|------------------|-----------------|
| [List ALL categories from the data with specific amounts] |

### 💰 SAVINGS IMPACT
- **Monthly Savings:** ₹[X,XXX]
- **Annual Savings:** ₹[X,XXX]
- **New Monthly Budget:** ₹[X,XXX]

### 🎯 ACTION ITEMS (3 Bullet Points)
- [Specific action 1 with deadline]
- [Specific action 2]
- [Specific action 3]

Make every number specific and every recommendation actionable. The roast should be savage enough to make them uncomfortable but the recovery plan should be genuinely helpful.
"""
        return prompt
    
    @staticmethod
    def get_category_recommendation_prompt(category: str, amount: float, total: float) -> str:
        """Get personalized recommendation for a specific category"""
        return f"""
Given that the user spends ₹{amount:,.2f} on {category}, which is {amount/total*100:.1f}% of their total budget.
Provide 3 specific, actionable recommendations to reduce spending in this category.
Be specific and practical.
"""
    
    @staticmethod
    def get_budget_forecast_prompt(historical_spend: Dict) -> str:
        """Generate budget forecast prompt"""
        return f"""
Based on the following historical spending data:
{json.dumps(historical_spend, indent=2)}

Provide a simple budget forecast for the next month. Include:
1. Predicted total spending
2. Categories likely to increase/decrease
3. Recommended savings target
"""

    @staticmethod
    def get_system_prompt(role: str = "expense_roaster") -> str:
        """Get system prompt by role"""
        return PromptTemplates.SYSTEM_PROMPTS.get(role, "")