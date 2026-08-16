"""
Visualization utilities for charts and plots
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from src.core.constants import CATEGORY_COLORS

class ChartRenderer:
    """Render various types of charts"""
    
    @staticmethod
    def pie_chart(data: pd.Series, title: str = "", height: int = 400):
        """Render an interactive pie chart using Plotly"""
        if data.empty:
            st.info("No data available for chart")
            return
        
        # Convert to DataFrame for Plotly compatibility
        df = data.reset_index()
        df.columns = ['Category', 'Amount']
        
        # Remove any rows with zero or negative values
        df = df[df['Amount'] > 0]
        
        if df.empty:
            st.info("No positive values to display")
            return
        
        fig = px.pie(
            df,
            values='Amount',
            names='Category',
            title=title,
            color='Category',
            color_discrete_map=CATEGORY_COLORS,
            hole=0.3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        
        fig.update_layout(
            height=height,
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", x=1.05),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def bar_chart(data: pd.Series, title: str = "", height: int = 400):
        """Render a bar chart using Plotly"""
        if data.empty:
            st.info("No data available for chart")
            return
        
        # Convert to DataFrame for Plotly compatibility
        df = data.reset_index()
        df.columns = ['Category', 'Amount']
        
        fig = px.bar(
            df,
            x='Category',
            y='Amount',
            title=title,
            color='Category',
            color_discrete_map=CATEGORY_COLORS,
            text='Amount'
        )
        
        fig.update_traces(
            texttemplate='₹%{text:,.0f}',
            textposition='outside'
        )
        
        fig.update_layout(
            height=height,
            xaxis_title="Category",
            yaxis_title="Amount (₹)",
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def line_chart(data, title: str = "", height: int = 300):
        """Render a line chart using Streamlit's native chart"""
        if data is None or (hasattr(data, 'empty') and data.empty):
            st.info("No data available for chart")
            return
        
        # Convert to DataFrame if it's a Series
        if isinstance(data, pd.Series):
            df = data.reset_index()
            df.columns = ['Date', 'Amount']
        else:
            df = data
        
        # Ensure Date is datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
        
        st.line_chart(df, use_container_width=True, height=height)
    
    @staticmethod
    def scatter_chart(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = None):
        """Render a scatter plot using Plotly"""
        if df.empty:
            st.info("No data available for chart")
            return
        
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=f"{y_col} vs {x_col}",
            color_discrete_map=CATEGORY_COLORS
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def treemap(data: pd.Series, title: str = ""):
        """Render a treemap using Plotly"""
        if data.empty:
            st.info("No data available for chart")
            return
        
        # Convert to DataFrame
        df = data.reset_index()
        df.columns = ['Category', 'Amount']
        
        # Remove zero/negative values
        df = df[df['Amount'] > 0]
        
        if df.empty:
            st.info("No positive values to display")
            return
        
        fig = px.treemap(
            df,
            names='Category',
            values='Amount',
            title=title,
            color='Amount',
            color_continuous_scale="Reds"
        )
        
        fig.update_traces(
            textinfo="label+value+percent root"
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)