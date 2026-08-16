"""
Sidebar components for the Expense Roaster
"""

import streamlit as st
import pandas as pd
from src.data.mock_data import generate_mock_data
from src.data.data_validator import DataValidator
from src.core.constants import APP_CONFIG, MESSAGES

def render_sidebar():
    """Render the sidebar with controls"""
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2 style="margin-bottom: 0;">💰</h2>
            <p style="color: #6B7280; font-size: 0.8rem; margin-top: 0;">v2.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🎯 Control Panel")
        
        # Data Source Selection
        data_source = st.radio(
            "📂 Data Source",
            ["📊 Use Sample Data", "📤 Upload CSV"],
            index=0,
            help="Choose to generate sample data or upload your own CSV"
        )
        
        if data_source == "📤 Upload CSV":
            uploaded_file = st.file_uploader(
                "Upload your expense CSV",
                type=['csv', 'xlsx'],
                help="CSV should have columns: Date, Category, Description, Amount"
            )
            
            if uploaded_file is not None:
                try:
                    # Read the file
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Validate data
                    validator = DataValidator(df)
                    is_valid, errors = validator.validate_expense_data()
                    
                    if is_valid:
                        # Process data
                        df = validator.clean_data()
                        st.session_state.df = df
                        st.session_state.roast_generated = False
                        st.session_state.roast_result = None
                        st.success(MESSAGES["success_upload"].format(count=len(df)))
                    else:
                        for error in errors:
                            st.error(error)
                        
                except Exception as e:
                    st.error(f"⚠️ Error reading file: {str(e)}")
        
        else:
            if st.button("🔄 Generate Sample Data", use_container_width=True):
                df = generate_mock_data()
                st.session_state.df = df
                st.session_state.roast_generated = False
                st.session_state.roast_result = None
                st.success("✅ Sample data generated with 30 transactions!")
        
        # Display data summary
        if st.session_state.df is not None and not st.session_state.df.empty:
            st.markdown("---")
            st.markdown("### 📊 Data Summary")
            
            df = st.session_state.df
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Transactions", len(df))
            with col2:
                st.metric("Total Spent", f"₹{df['Amount'].sum():,.0f}")
            
            if 'Category' in df.columns:
                st.markdown("#### Top Categories")
                top_categories = df.groupby('Category')['Amount'].sum().nlargest(3)
                for cat, amount in top_categories.items():
                    st.progress(
                        min(amount / df['Amount'].sum(), 1.0),
                        text=f"{cat}: ₹{amount:,.0f}"
                    )
            
            st.markdown("---")
            st.caption(f"🔒 {MESSAGES['data_stays_local']}")
        
        # Footer
        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit + AI")