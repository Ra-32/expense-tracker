"""
Main dashboard renderer for the Expense Roaster
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import base64
from src.ui.components import UIComponents
from src.ui.visualizations import ChartRenderer
from src.data.data_processor import DataProcessor
from src.ai.factory import get_llm_provider
from src.ai.prompt_templates import PromptTemplates
from src.ai.response_parser import ResponseParser
from src.state.session_state import SessionStateManager
from src.utils.report_generator import ReportGenerator
from src.core.constants import CATEGORY_COLORS
import time

def render_dashboard():
    """Render the main dashboard"""
    
    if st.session_state.df is None or st.session_state.df.empty:
        render_welcome_state()
        return
    
    df = st.session_state.df
    render_quick_stats(df)
    
    tab1, tab2, tab3 = st.tabs([
        "📝 Data Editor",
        "📊 Visualizations",
        "🔥 AI Roast"
    ])
    
    with tab1:
        render_data_editor(df)
    
    with tab2:
        render_visualizations(df)
    
    with tab3:
        render_ai_roast(df)

def render_quick_stats(df: pd.DataFrame):
    """Display quick statistics cards at the top"""
    processor = DataProcessor(df)
    stats = processor.get_statistics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="💰 Total Spent",
            value=f"₹{stats['total_spent']:,.0f}",
            delta=f"{stats['transaction_count']} transactions"
        )
    
    with col2:
        st.metric(
            label="📅 Daily Average",
            value=f"₹{stats['avg_daily']:,.0f}",
            delta="per day"
        )
    
    with col3:
        waste_pct = stats['waste_percentage']
        st.metric(
            label="🎯 Waste Score",
            value=f"{waste_pct:.0f}%",
            delta=f"₹{stats['wasteful_spending']:,.0f} wasted",
            delta_color="inverse" if waste_pct > 30 else "normal"
        )
    
    with col4:
        top_category = stats['category_spending'].index[0] if not stats['category_spending'].empty else "N/A"
        top_amount = stats['category_spending'].values[0] if not stats['category_spending'].empty else 0
        st.metric(
            label="🏆 Top Category",
            value=top_category,
            delta=f"₹{top_amount:,.0f}"
        )
    
    with col5:
        if stats['worst_day']:
            st.metric(
                label="🔥 Worst Day",
                value=f"₹{stats['worst_day_amount']:,.0f}",
                delta=str(stats['worst_day'])[:10]
            )
        else:
            st.metric(
                label="🔥 Worst Day",
                value="N/A",
                delta="No date data"
            )
    
    st.markdown("---")

def render_welcome_state():
    """Render welcome state when no data is loaded"""
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%); border-radius: 24px; margin: 2rem 0;">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: #1e293b;">👋 Welcome to The Expense Roaster!</h2>
        <p style="font-size: 1.1rem; color: #64748b; max-width: 600px; margin: 1rem auto;">
            Upload your expense CSV or generate sample data from the sidebar.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin: 1.5rem 0;">
            <div style="background: white; padding: 1rem 2rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size: 2rem;">📤</div>
                <div style="font-weight: 600;">Upload CSV</div>
            </div>
            <div style="background: white; padding: 1rem 2rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size: 2rem;">📊</div>
                <div style="font-weight: 600;">View Charts</div>
            </div>
            <div style="background: white; padding: 1rem 2rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size: 2rem;">🔥</div>
                <div style="font-weight: 600;">Get Roasted</div>
            </div>
        </div>
        <p style="font-size: 0.95rem; color: #94a3b8;">
            🔒 Your data stays in your browser session and is never stored.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_data_editor(df: pd.DataFrame):
    """Render the data editor tab"""
    st.subheader("✏️ Edit Your Expenses")
    st.caption("Double-click any cell to edit. Changes are automatically saved.")
    
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor",
        column_config={
            "Date": st.column_config.DateColumn("Date"),
            "Amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
            "Category": st.column_config.SelectboxColumn(
                "Category",
                options=["Food", "Entertainment", "Transport", "Shopping", "Bills", 
                        "Healthcare", "Education", "Rent", "Insurance", "Other"]
            )
        }
    )
    
    st.session_state.df = edited_df
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Transactions", len(edited_df))
    with col2:
        st.metric("💰 Total Spent", f"₹{edited_df['Amount'].sum():,.2f}")
    with col3:
        st.metric("📈 Average Amount", f"₹{edited_df['Amount'].mean():,.2f}")
    with col4:
        st.metric("📊 Categories", edited_df['Category'].nunique())

def render_visualizations(df: pd.DataFrame):
    """Render the visualizations tab"""
    st.subheader("📊 Spending Visualizations")
    st.caption("Interactive charts to understand your spending patterns")
    
    processor = DataProcessor(df)
    stats = processor.get_statistics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🍩 Spending by Category")
        ChartRenderer.pie_chart(
            stats['category_spending'],
            title="Where Your Money Goes"
        )
    
    with col2:
        st.markdown("### 📊 Category Breakdown")
        ChartRenderer.bar_chart(
            stats['category_spending'],
            title="Spending by Category"
        )
    
    if stats['daily_spending'] is not None:
        st.markdown("---")
        st.markdown("### 📈 Daily Spending Trend")
        ChartRenderer.line_chart(stats['daily_spending'])

def render_ai_roast(df: pd.DataFrame):
    """Render the AI roast tab with report download"""
    st.subheader("🔥 AI Roast & Recovery Plan")
    st.caption("Get brutally honest feedback on your spending habits")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔥 ROAST MY EXPENSES!", use_container_width=True):
            with st.spinner("🧠 Analyzing your spending habits..."):
                processor = DataProcessor(df)
                stats = processor.get_statistics()
                
                llm = get_llm_provider()
                system_prompt = PromptTemplates.get_system_prompt("expense_roaster")
                user_prompt = PromptTemplates.get_roast_prompt(stats)
                
                response = llm.generate_content(
                    prompt=user_prompt,
                    system_prompt=system_prompt
                )
                
                if response.success:
                    st.session_state.roast_result = response.content
                    st.session_state.roast_generated = True
                    st.session_state.roast_metadata = {
                        'provider': response.provider,
                        'model': response.model
                    }
                    # Store stats for report
                    st.session_state.report_stats = stats
                else:
                    st.error(f"❌ AI Error: {response.error}")
                    st.info("💡 Tip: Check your API key configuration")
    
    st.markdown("---")
    
    if st.session_state.roast_generated and st.session_state.roast_result:
        roast_text = st.session_state.roast_result
        stats = st.session_state.report_stats
        
        # Display roast
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 2rem; border-radius: 20px; 
                    border-left: 6px solid #FF6B6B; margin: 1.5rem 0; color: #e2e8f0; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
            {roast_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Parse recovery table
        recovery_df = ResponseParser.extract_recovery_table(roast_text)
        if recovery_df is not None:
            st.markdown("### 📋 Recovery Plan")
            st.dataframe(recovery_df, use_container_width=True, hide_index=True)
        
        # Extract metrics
        metrics = ResponseParser.extract_metrics(roast_text)
        if metrics:
            st.markdown("### 💰 Savings Impact")
            cols = st.columns(3)
            for idx, (key, value) in enumerate(metrics.items()):
                with cols[idx % 3]:
                    label_map = {
                        'monthly_savings': 'Monthly Savings',
                        'annual_savings': 'Annual Savings',
                        'new_budget': 'New Budget'
                    }
                    st.metric(label_map.get(key, key), f"₹{value:,.2f}")
        
        # ============================================================
        # 📥 DOWNLOAD FULL HTML REPORT
        # ============================================================
        st.markdown("---")
        st.markdown("### 📥 Download Complete Report")
        
        with st.spinner("📊 Generating comprehensive HTML report..."):
            # Generate charts as images
            chart_images = {}
            
            # Pie chart
            if not stats['category_spending'].empty:
                fig_pie = px.pie(
                    values=stats['category_spending'].values,
                    names=stats['category_spending'].index,
                    color=stats['category_spending'].index,
                    color_discrete_map=CATEGORY_COLORS,
                    hole=0.3
                )
                fig_pie.update_layout(
                    showlegend=True,
                    legend=dict(orientation="v", yanchor="middle", x=1.05),
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                img_bytes = fig_pie.to_image(format="png", width=500, height=400, scale=2)
                chart_images['pie'] = base64.b64encode(img_bytes).decode()
            
            # Bar chart
            if not stats['category_spending'].empty:
                fig_bar = px.bar(
                    x=stats['category_spending'].index,
                    y=stats['category_spending'].values,
                    color=stats['category_spending'].index,
                    color_discrete_map=CATEGORY_COLORS,
                    text=stats['category_spending'].values
                )
                fig_bar.update_layout(
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Category",
                    yaxis_title="Amount (₹)"
                )
                fig_bar.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
                img_bytes = fig_bar.to_image(format="png", width=500, height=400, scale=2)
                chart_images['bar'] = base64.b64encode(img_bytes).decode()
            
            # Line chart (if daily data exists)
            if stats['daily_spending'] is not None and not stats['daily_spending'].empty:
                fig_line = px.line(
                    x=stats['daily_spending'].index,
                    y=stats['daily_spending'].values,
                    title=""
                )
                fig_line.update_layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Date",
                    yaxis_title="Amount (₹)"
                )
                fig_line.update_traces(line_color='#4D96FF', line_width=3)
                img_bytes = fig_line.to_image(format="png", width=700, height=300, scale=2)
                chart_images['line'] = base64.b64encode(img_bytes).decode()
            
            # Generate HTML report
            html_report = ReportGenerator.generate_html_report(
                df=df,
                stats=stats,
                roast_text=roast_text,
                chart_images=chart_images
            )
            
            # Download button
            st.download_button(
                label="📥 Download Complete Report (HTML)",
                data=html_report,
                file_name=ReportGenerator.generate_report_filename(),
                mime="text/html",
                use_container_width=True,
                help="Download a complete HTML report with all charts, statistics, and AI analysis"
            )
            
            # Also provide Markdown download
            md_report = f"""
# The Expense Roaster - Financial Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{roast_text}

---
*Report generated by The Expense Roaster | Powered by Gemini AI*
"""
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=md_report,
                file_name=f"expense_roast_report_{time.strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Reset button
        if st.button("🔄 Generate New Roast"):
            st.session_state.roast_generated = False
            st.session_state.roast_result = None
            st.rerun()