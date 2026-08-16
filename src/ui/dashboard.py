"""
Main dashboard renderer for the Expense Roaster - With HTML Charts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import base64
import io
from src.ui.visualizations import ChartRenderer
from src.data.data_processor import DataProcessor
from src.ai.factory import get_llm_provider
from src.ai.prompt_templates import PromptTemplates
from src.ai.response_parser import ResponseParser
from src.core.constants import CATEGORY_COLORS

# ============================================================
# DASHBOARD RENDERER - WITH HTML CHARTS (No Chrome needed!)
# ============================================================

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
    """Display quick statistics cards"""
    processor = DataProcessor(df)
    stats = processor.get_statistics()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("💰 Total Spent", f"₹{stats['total_spent']:,.0f}", f"{stats['transaction_count']} transactions")
    with col2:
        st.metric("📅 Daily Average", f"₹{stats['avg_daily']:,.0f}", "per day")
    with col3:
        waste_pct = stats['waste_percentage']
        st.metric("🎯 Waste Score", f"{waste_pct:.0f}%", f"₹{stats['wasteful_spending']:,.0f} wasted", delta_color="inverse" if waste_pct > 30 else "normal")
    with col4:
        top_category = stats['category_spending'].index[0] if not stats['category_spending'].empty else "N/A"
        top_amount = stats['category_spending'].values[0] if not stats['category_spending'].empty else 0
        st.metric("🏆 Top Category", top_category, f"₹{top_amount:,.0f}")
    with col5:
        if stats['worst_day']:
            st.metric("🔥 Worst Day", f"₹{stats['worst_day_amount']:,.0f}", str(stats['worst_day'])[:10])
        else:
            st.metric("🔥 Worst Day", "N/A", "No date data")
    
    st.markdown("---")

def render_welcome_state():
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%); border-radius: 24px; margin: 2rem 0;">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: #1e293b;">👋 Welcome to The Expense Roaster!</h2>
        <p style="font-size: 1.1rem; color: #64748b;">Upload your expense CSV or generate sample data from the sidebar.</p>
        <p style="font-size: 0.95rem; color: #94a3b8;">🔒 Your data stays in your browser session and is never stored.</p>
    </div>
    """, unsafe_allow_html=True)

def render_data_editor(df: pd.DataFrame):
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
    st.subheader("📊 Spending Visualizations")
    st.caption("Interactive charts to understand your spending patterns")
    
    processor = DataProcessor(df)
    stats = processor.get_statistics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🍩 Spending by Category")
        ChartRenderer.pie_chart(stats['category_spending'], title="Where Your Money Goes")
    
    with col2:
        st.markdown("### 📊 Category Breakdown")
        ChartRenderer.bar_chart(stats['category_spending'], title="Spending by Category")
    
    if stats['daily_spending'] is not None:
        st.markdown("---")
        st.markdown("### 📈 Daily Spending Trend")
        ChartRenderer.line_chart(stats['daily_spending'])

def render_ai_roast(df: pd.DataFrame):
    """Render the AI roast tab with HTML report containing interactive charts"""
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
        # 📥 DOWNLOAD HTML REPORT WITH INTERACTIVE CHARTS
        # ============================================================
        st.markdown("---")
        st.markdown("### 📥 Download Complete Report")
        st.info("📊 The HTML report includes interactive charts that you can hover over and explore!")
        
        with st.spinner("📊 Generating HTML report with interactive charts..."):
            # Generate HTML report with interactive charts
            html_report = generate_html_report_with_charts(df, stats, roast_text)
            
            st.download_button(
                label="📥 Download Complete Report (HTML with Interactive Charts)",
                data=html_report,
                file_name=f"expense_roast_report_{time.strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        # Text report as fallback
        report_text = generate_text_report(df, stats, roast_text)
        st.download_button(
            label="📥 Download Report (Text)",
            data=report_text,
            file_name=f"expense_roast_report_{time.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        if st.button("🔄 Generate New Roast"):
            st.session_state.roast_generated = False
            st.session_state.roast_result = None
            st.rerun()


def generate_html_report_with_charts(df: pd.DataFrame, stats: dict, roast_text: str) -> str:
    """Generate HTML report with interactive Plotly charts (No Chrome needed!)"""
    
    # Create the charts as HTML
    pie_chart_html = ""
    bar_chart_html = ""
    line_chart_html = ""
    
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
            plot_bgcolor='rgba(0,0,0,0)',
            height=450
        )
        pie_chart_html = fig_pie.to_html(full_html=False, include_plotlyjs='cdn')
    
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
            yaxis_title="Amount (₹)",
            height=450
        )
        fig_bar.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        bar_chart_html = fig_bar.to_html(full_html=False, include_plotlyjs=False)
    
    # Line chart
    if stats['daily_spending'] is not None and not stats['daily_spending'].empty:
        fig_line = px.line(
            x=stats['daily_spending'].index,
            y=stats['daily_spending'].values
        )
        fig_line.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Amount (₹)",
            height=350
        )
        fig_line.update_traces(line_color='#4D96FF', line_width=3)
        line_chart_html = fig_line.to_html(full_html=False, include_plotlyjs=False)
    
    # Category table
    category_rows = ""
    for cat, amount in stats['category_spending'].items():
        pct = (amount / stats['total_spent'] * 100) if stats['total_spent'] > 0 else 0
        category_rows += f"""
        <tr>
            <td style="padding: 10px 15px; border-bottom: 1px solid #e2e8f0;">{cat}</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #e2e8f0; text-align: right;">₹{amount:,.2f}</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #e2e8f0; text-align: right;">{pct:.1f}%</td>
            <td style="padding: 10px 15px; border-bottom: 1px solid #e2e8f0;">
                <div style="background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #FF6B6B, #FFA94D); height: 100%; width: {min(pct, 100)}%;"></div>
                </div>
            </td>
        </tr>
        """
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Expense Roaster - Financial Report</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; padding: 40px 20px; }}
        .container {{ max-width: 1100px; margin: 0 auto; background: white; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.08); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: white; padding: 50px 60px; }}
        .header h1 {{ font-size: 2.8rem; background: linear-gradient(90deg, #FF6B6B, #FFA94D, #FFD93D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .header .meta {{ display: flex; gap: 30px; margin-top: 20px; flex-wrap: wrap; color: #cbd5e1; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 30px 60px; background: #f8fafc; }}
        .summary-card {{ text-align: center; padding: 16px; background: white; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
        .summary-card .value {{ font-size: 1.8rem; font-weight: 700; color: #1e293b; }}
        .summary-card .label {{ color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        .content {{ padding: 40px 60px; }}
        .section {{ margin-bottom: 40px; }}
        .section-title {{ font-size: 1.5rem; font-weight: 700; color: #1e293b; margin-bottom: 16px; }}
        .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }}
        .chart-container {{ background: #f8fafc; border-radius: 16px; padding: 20px; border: 1px solid #e2e8f0; }}
        .chart-container h3 {{ font-size: 1rem; color: #64748b; margin-bottom: 12px; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #f1f5f9; padding: 14px 20px; text-align: left; font-weight: 600; color: #475569; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.05em; }}
        td {{ padding: 12px 20px; border-bottom: 1px solid #f1f5f9; }}
        tr:hover td {{ background: #f8fafc; }}
        .roast-box {{ background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px 35px; border-radius: 16px; color: #e2e8f0; border-left: 5px solid #FF6B6B; }}
        .roast-box h3 {{ color: #FF6B6B; font-size: 1.3rem; }}
        .roast-box h4 {{ color: #FFA94D; margin-top: 20px; }}
        .roast-box table {{ margin: 12px 0; background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; }}
        .roast-box table th {{ background: rgba(255,107,107,0.15); color: #FFA94D; }}
        .roast-box table td {{ color: #cbd5e1; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .footer {{ text-align: center; padding: 30px; background: #f8fafc; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.85rem; }}
        .footer .brand {{ font-weight: 600; color: #1e293b; }}
        @media (max-width: 768px) {{ .summary-grid {{ grid-template-columns: 1fr 1fr; padding: 20px 24px; }} .charts-grid {{ grid-template-columns: 1fr; }} .header {{ padding: 30px 24px; }} .content {{ padding: 24px; }} .header h1 {{ font-size: 2rem; }} }}
        @media print {{ body {{ background: white; padding: 0; }} .container {{ box-shadow: none; border-radius: 0; }} .header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 The Expense Roaster</h1>
            <p style="color: #94a3b8;">AI-Powered Spending Analysis Report</p>
            <div class="meta">
                <span>📅 {time.strftime('%B %d, %Y at %I:%M %p')}</span>
                <span>📊 {len(df)} Transactions</span>
                <span>📂 {df['Category'].nunique() if 'Category' in df.columns else 'N/A'} Categories</span>
                <span>🤖 Powered by Gemini AI</span>
            </div>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card"><div class="label">💰 Total Spent</div><div class="value">₹{stats['total_spent']:,.0f}</div></div>
            <div class="summary-card"><div class="label">📅 Daily Average</div><div class="value">₹{stats['avg_daily']:,.0f}</div></div>
            <div class="summary-card"><div class="label">🎯 Waste Score</div><div class="value">{stats['waste_percentage']:.0f}%</div></div>
            <div class="summary-card"><div class="label">📊 Transactions</div><div class="value">{len(df)}</div></div>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-title">📊 Spending Visualizations</div>
                <div class="charts-grid">
                    <div class="chart-container">
                        <h3>🍩 Spending by Category</h3>
                        {pie_chart_html}
                    </div>
                    <div class="chart-container">
                        <h3>📊 Category Breakdown</h3>
                        {bar_chart_html}
                    </div>
                </div>
                {f'''
                <div class="chart-container" style="margin-top: 20px;">
                    <h3>📈 Daily Spending Trend</h3>
                    {line_chart_html}
                </div>
                ''' if line_chart_html else ''}
            </div>
            
            <div class="section">
                <div class="section-title">📋 Category Breakdown</div>
                <div style="overflow-x: auto; border-radius: 12px; border: 1px solid #e2e8f0;">
                    <table>
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th style="text-align: right;">Amount Spent</th>
                                <th style="text-align: right;">Percentage</th>
                                <th>Distribution</th>
                            </tr>
                        </thead>
                        <tbody>
                            {category_rows}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">🔥 AI Roast & Recovery Plan</div>
                <div class="roast-box">
                    {roast_text}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><span class="brand">💰 The Expense Roaster</span> — AI-Powered Financial Analysis & Recovery</p>
            <p style="margin-top: 4px; font-size: 0.75rem;">🔒 Your data stays private • Generated on {time.strftime('%B %d, %Y at %I:%M %p')}</p>
            <p style="margin-top: 4px; font-size: 0.75rem; color: #cbd5e1;">© 2026 All Rights Reserved • Built with ❤️ using Streamlit + Google Gemini AI</p>
        </div>
    </div>
</body>
</html>
"""
    return html


def generate_text_report(df: pd.DataFrame, stats: dict, roast_text: str) -> str:
    """Generate a text-based report without images"""
    
    category_text = ""
    total = stats['total_spent']
    for cat, amount in stats['category_spending'].items():
        pct = (amount / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2)
        category_text += f"  {cat:15} ₹{amount:12,.2f}  {pct:5.1f}%  {bar}\n"
    
    report = f"""
{'='*70}
💰 THE EXPENSE ROASTER - FINANCIAL REPORT
{'='*70}

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

📊 SPENDING SUMMARY
{'='*50}
Total Spent:      ₹{stats['total_spent']:12,.2f}
Daily Average:    ₹{stats['avg_daily']:12,.2f}
Waste Score:      {stats['waste_percentage']:5.1f}%
Transactions:     {len(df):12}
Worst Day:        {stats['worst_day'] if stats['worst_day'] else 'N/A'}

📋 CATEGORY BREAKDOWN
{'='*50}
{category_text}

🔥 AI ROAST & RECOVERY PLAN
{'='*50}
{roast_text}

{'='*70}
Report generated by The Expense Roaster | Powered by Gemini AI
{'='*70}
"""
    return report