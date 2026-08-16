"""
The Expense Roaster - Professional AI-Powered Financial Dashboard
B.Tech Capstone Project | Streamlit + Google Gemini AI
"""

import streamlit as st
from src.core.config import setup_environment
from src.core.constants import APP_CONFIG
from src.ui.css import load_custom_css
from src.ui.sidebar import render_sidebar
from src.ui.dashboard import render_dashboard
from src.state.session_state import initialize_session_state
import pandas as pd
import os

# Setup environment
setup_environment()

# ============================================================
# 🎯 PAGE CONFIGURATION - Professional Dashboard
# ============================================================

st.set_page_config(
    page_title="💰 The Expense Roaster - AI Financial Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Initialize session state
initialize_session_state()

# ============================================================
# 🎯 MAIN APPLICATION
# ============================================================

def main():
    """Main application entry point"""
    
    # ============================================================
    # 🎯 PROFESSIONAL HEADER WITH BRANDING
    # ============================================================
    
    # Main Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <h1 style="font-size: 4rem; font-weight: 800; background: linear-gradient(135deg, #FF6B6B, #FFA94D, #FFD93D); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">
            💰 The Expense Roaster 🔥
        </h1>
        <p style="font-size: 1.2rem; color: #6B7280; margin-top: 0.2rem;">
            AI-Powered Spending Analysis • Financial Recovery • Smart Insights
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin: 0.5rem 0;">
            <span style="background: #FF6B6B20; color: #FF6B6B; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                🚀 Xpress RK
            </span>
            <span style="background: #4D96FF20; color: #4D96FF; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                🤖 RK PRODUCTION
            </span>
            <span style="background: #10B98120; color: #10B981; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                📊 v2.0
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Divider
    st.markdown("---")
    
    # Render sidebar
    render_sidebar()
    
    # Render main dashboard
    render_dashboard()
    
    # ============================================================
    # 🎯 FOOTER
    # ============================================================
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 0.5rem 0; border-top: 1px solid #e2e8f0; margin-top: 2rem;">
        <p style="color: #94a3b8; font-size: 0.85rem;">
            🔒 Your data stays local • No data stored • Built with ❤️ using Streamlit + RK
        </p>
        <p style="color: #cbd5e1; font-size: 0.75rem;">
            © 2026 The Expense Roaster | All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()