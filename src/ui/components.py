"""
Reusable UI components for the Expense Roaster
"""

import streamlit as st
from typing import Dict, Any, Optional, Callable
import pandas as pd

class UIComponents:
    """Factory for reusable UI components"""
    
    @staticmethod
    def metric_card(
        label: str,
        value: Any,
        delta: Optional[str] = None,
        delta_color: str = "normal",
        help_text: Optional[str] = None
    ):
        """Create a styled metric card"""
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-delta {'delta-positive' if delta_color == "normal" else "delta-negative"}">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def roast_box(content: str):
        """Display AI roast in a styled box"""
        st.markdown(f"""
        <div class="roast-box">
            {content}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def section_header(title: str, subtitle: Optional[str] = None):
        """Display a section header"""
        st.markdown(f"""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="font-weight: 700; color: #1e293b;">{title}</h2>
            {f'<p style="color: #64748b; margin-top: -0.5rem;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def divider():
        """Display a styled divider"""
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    @staticmethod
    def action_button(label: str, primary: bool = True, key: Optional[str] = None):
        """Create a styled action button"""
        class_name = "" if primary else "btn-secondary"
        return st.button(label, key=key, use_container_width=True)
    
    @staticmethod
    def info_alert(message: str, type: str = "info"):
        """Display an info alert"""
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "success": "✅",
            "error": "❌"
        }
        colors = {
            "info": "#3b82f6",
            "warning": "#f59e0b",
            "success": "#10b981",
            "error": "#ef4444"
        }
        
        st.markdown(f"""
        <div style="
            background: {colors.get(type, '#3b82f6')}10;
            border-left: 4px solid {colors.get(type, '#3b82f6')};
            padding: 1rem 1.2rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            color: #1e293b;
        ">
            {icons.get(type, '')} {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def expense_table(df: pd.DataFrame, height: int = 400):
        """Display expense data in a styled table"""
        st.dataframe(
            df,
            use_container_width=True,
            height=height,
            column_config={
                "Amount": st.column_config.NumberColumn(
                    "Amount (₹)",
                    format="₹%.2f"
                )
            }
        )