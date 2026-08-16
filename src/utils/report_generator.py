"""
HTML Report Generator for Expense Roaster
Generates professional HTML reports with charts and AI analysis
"""

import pandas as pd
import base64
from io import StringIO
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, Any, Optional
import streamlit as st

class ReportGenerator:
    """Generate professional HTML reports with charts and AI analysis"""
    
    @staticmethod
    def generate_html_report(
        df: pd.DataFrame,
        stats: Dict[str, Any],
        roast_text: str,
        chart_images: Dict[str, str]  # Base64 encoded images
    ) -> str:
        """
        Generate a complete HTML report
        
        Args:
            df: Expense DataFrame
            stats: Statistics dictionary
            roast_text: AI roast content
            chart_images: Dictionary of base64 encoded chart images
        
        Returns:
            HTML string
        """
        
        # Get date for report
        report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Calculate summary metrics
        total_spent = stats['total_spent']
        avg_daily = stats['avg_daily']
        waste_pct = stats['waste_percentage']
        top_category = stats['category_spending'].index[0] if not stats['category_spending'].empty else "N/A"
        top_amount = stats['category_spending'].values[0] if not stats['category_spending'].empty else 0
        
        # Get category breakdown for table
        category_table = ""
        for cat, amount in stats['category_spending'].items():
            pct = (amount / total_spent * 100) if total_spent > 0 else 0
            category_table += f"""
            <tr>
                <td>{cat}</td>
                <td>₹{amount:,.2f}</td>
                <td>{pct:.1f}%</td>
                <td>
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
    <title>Expense Roaster Report</title>
    <style>
        /* ===== GLOBAL STYLES ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f8fafc;
            color: #1e293b;
            line-height: 1.6;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        
        /* ===== HEADER ===== */
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 50px 60px 40px;
            position: relative;
        }}
        
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #FF6B6B, #FFA94D, #FFD93D);
        }}
        
        .header h1 {{
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #FF6B6B, #FFA94D, #FFD93D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }}
        
        .header .subtitle {{
            font-size: 1.1rem;
            color: #94a3b8;
            -webkit-text-fill-color: #94a3b8;
        }}
        
        .header .meta {{
            display: flex;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .header .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #cbd5e1;
            font-size: 0.9rem;
        }}
        
        .header .meta-item .icon {{
            font-size: 1.2rem;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            background: rgba(255, 107, 107, 0.15);
            color: #FF6B6B;
            -webkit-text-fill-color: #FF6B6B;
            margin-left: 10px;
        }}
        
        /* ===== SUMMARY CARDS ===== */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            padding: 30px 60px;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .summary-card {{
            text-align: center;
            padding: 16px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        
        .summary-card .label {{
            font-size: 0.8rem;
            color: #94a3b8;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .summary-card .value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #1e293b;
            margin-top: 4px;
        }}
        
        .summary-card .delta {{
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 2px;
        }}
        
        .card-waste .value {{ color: #FF6B6B; }}
        .card-total .value {{ color: #4D96FF; }}
        .card-daily .value {{ color: #10B981; }}
        .card-top .value {{ color: #FFA94D; }}
        
        /* ===== CONTENT ===== */
        .content {{
            padding: 40px 60px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-title .emoji {{
            font-size: 1.8rem;
        }}
        
        /* ===== CHARTS ===== */
        .charts-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }}
        
        .chart-container {{
            background: #f8fafc;
            border-radius: 16px;
            padding: 20px;
            border: 1px solid #e2e8f0;
        }}
        
        .chart-container h3 {{
            font-size: 1rem;
            color: #64748b;
            margin-bottom: 12px;
            text-align: center;
        }}
        
        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        
        /* ===== CATEGORY TABLE ===== */
        .table-wrap {{
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }}
        
        table th {{
            background: #f1f5f9;
            padding: 14px 20px;
            text-align: left;
            font-weight: 600;
            color: #475569;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        table td {{
            padding: 12px 20px;
            border-bottom: 1px solid #f1f5f9;
        }}
        
        table tr:hover td {{
            background: #f8fafc;
        }}
        
        /* ===== ROAST BOX ===== */
        .roast-box {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 30px 35px;
            border-radius: 16px;
            color: #e2e8f0;
            border-left: 5px solid #FF6B6B;
        }}
        
        .roast-box h3 {{
            color: #FF6B6B;
            font-size: 1.3rem;
            margin-bottom: 12px;
        }}
        
        .roast-box h4 {{
            color: #FFA94D;
            margin-top: 20px;
            margin-bottom: 8px;
        }}
        
        .roast-box table {{
            margin: 12px 0;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .roast-box table th {{
            background: rgba(255, 107, 107, 0.15);
            color: #FFA94D;
        }}
        
        .roast-box table td {{
            color: #cbd5e1;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        .roast-box ul {{
            list-style: none;
            padding: 0;
        }}
        
        .roast-box ul li {{
            padding: 8px 0 8px 28px;
            position: relative;
        }}
        
        .roast-box ul li::before {{
            content: '▸';
            position: absolute;
            left: 8px;
            color: #FF6B6B;
            font-weight: bold;
        }}
        
        .roast-box .highlight {{
            color: #FF6B6B;
            font-weight: 600;
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            text-align: center;
            padding: 30px 60px;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            color: #94a3b8;
            font-size: 0.85rem;
        }}
        
        .footer .brand {{
            font-weight: 600;
            color: #1e293b;
        }}
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {{
            .header {{ padding: 30px 24px; }}
            .header h1 {{ font-size: 2rem; }}
            .content {{ padding: 24px; }}
            .summary-grid {{ grid-template-columns: 1fr 1fr; padding: 20px 24px; }}
            .charts-grid {{ grid-template-columns: 1fr; }}
            .summary-card .value {{ font-size: 1.4rem; }}
            .roast-box {{ padding: 20px; }}
            .footer {{ padding: 20px 24px; }}
        }}
        
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; border-radius: 0; }}
            .header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
            .roast-box {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- ===== HEADER ===== -->
        <div class="header">
            <h1>💰 The Expense Roaster</h1>
            <div class="subtitle">
                AI-Powered Spending Analysis Report
                <span class="badge">🔥 Generated</span>
            </div>
            <div class="meta">
                <span class="meta-item">
                    <span class="icon">📅</span>
                    {report_date}
                </span>
                <span class="meta-item">
                    <span class="icon">📊</span>
                    {len(df)} Transactions
                </span>
                <span class="meta-item">
                    <span class="icon">📂</span>
                    {df['Category'].nunique() if 'Category' in df.columns else 'N/A'} Categories
                </span>
                <span class="meta-item">
                    <span class="icon">🤖</span>
                    Powered by Gemini AI
                </span>
            </div>
        </div>
        
        <!-- ===== SUMMARY CARDS ===== -->
        <div class="summary-grid">
            <div class="summary-card card-total">
                <div class="label">💰 Total Spent</div>
                <div class="value">₹{total_spent:,.0f}</div>
                <div class="delta">30-day period</div>
            </div>
            <div class="summary-card card-daily">
                <div class="label">📅 Daily Average</div>
                <div class="value">₹{avg_daily:,.0f}</div>
                <div class="delta">per day</div>
            </div>
            <div class="summary-card card-waste">
                <div class="label">🎯 Waste Score</div>
                <div class="value">{waste_pct:.0f}%</div>
                <div class="delta">₹{stats['wasteful_spending']:,.0f} wasted</div>
            </div>
            <div class="summary-card card-top">
                <div class="label">🏆 Top Category</div>
                <div class="value">{top_category}</div>
                <div class="delta">₹{top_amount:,.0f} spent</div>
            </div>
        </div>
        
        <!-- ===== CONTENT ===== -->
        <div class="content">
            
            <!-- ===== CHARTS ===== -->
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📊</span> Spending Visualizations
                </div>
                <div class="charts-grid">
                    <div class="chart-container">
                        <h3>🍩 Spending by Category</h3>
                        <img src="data:image/png;base64,{chart_images.get('pie', '')}" alt="Pie Chart">
                    </div>
                    <div class="chart-container">
                        <h3>📊 Category Breakdown</h3>
                        <img src="data:image/png;base64,{chart_images.get('bar', '')}" alt="Bar Chart">
                    </div>
                </div>
                
                {f'''
                <div class="chart-container" style="margin-top: 20px;">
                    <h3>📈 Daily Spending Trend</h3>
                    <img src="data:image/png;base64,{chart_images.get('line', '')}" alt="Line Chart">
                </div>
                ''' if chart_images.get('line') else ''}
            </div>
            
            <!-- ===== CATEGORY BREAKDOWN ===== -->
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📋</span> Category Breakdown
                </div>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th>Amount Spent</th>
                                <th>Percentage</th>
                                <th>Distribution</th>
                            </tr>
                        </thead>
                        <tbody>
                            {category_table}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- ===== AI ROAST ===== -->
            <div class="section">
                <div class="section-title">
                    <span class="emoji">🔥</span> AI Roast & Recovery Plan
                </div>
                <div class="roast-box">
                    {roast_text}
                </div>
            </div>
            
        </div>
        
        <!-- ===== FOOTER ===== -->
        <div class="footer">
            <p>
                <span class="brand">💰 The Expense Roaster</span> — 
                AI-Powered Financial Analysis & Recovery
            </p>
            <p style="margin-top: 4px; font-size: 0.75rem;">
                🔒 Your data stays private • Generated on {report_date}
            </p>
            <p style="margin-top: 4px; font-size: 0.75rem; color: #cbd5e1;">
                © 2026 All Rights Reserved • Built with ❤️ using Streamlit + RK
            </p>
        </div>
    </div>
</body>
</html>
"""
        
        return html

    @staticmethod
    def generate_report_filename() -> str:
        """Generate a unique report filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"expense_roast_report_{timestamp}.html"