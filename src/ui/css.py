"""
Custom CSS styles for the Expense Roaster UI
Professional, modern design with animations and responsive layout
"""

import streamlit as st

def load_custom_css():
    """Load all custom CSS styles"""
    
    css = """
    <style>
        /* ===== GLOBAL STYLES ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .main {
            padding: 0rem 1rem;
        }
        
        /* ===== HEADER STYLES ===== */
        .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FF6B6B 0%, #FFA94D 50%, #FFD93D 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            padding: 1rem 0;
            letter-spacing: -0.02em;
            animation: fadeInDown 0.8s ease;
        }
        
        .sub-header {
            text-align: center;
            color: #6B7280;
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: -0.5rem;
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease;
        }
        
        /* ===== ANIMATIONS ===== */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 20px rgba(255, 107, 107, 0.2);
            }
            50% {
                box-shadow: 0 0 40px rgba(255, 107, 107, 0.4);
            }
        }
        
        /* ===== METRIC CARDS ===== */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid rgba(255,255,255,0.8);
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1a202c;
            line-height: 1.2;
        }
        
        .metric-label {
            font-size: 0.85rem;
            color: #6B7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .metric-delta {
            font-size: 0.9rem;
            font-weight: 600;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            display: inline-block;
            margin-top: 0.3rem;
        }
        
        .delta-positive {
            color: #10B981;
            background: rgba(16, 185, 129, 0.1);
        }
        
        .delta-negative {
            color: #EF4444;
            background: rgba(239, 68, 68, 0.1);
        }
        
        /* ===== ROAST BOX ===== */
        .roast-box {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            border-radius: 20px;
            border-left: 6px solid #FF6B6B;
            margin: 1.5rem 0;
            color: #e2e8f0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            animation: fadeInUp 0.6s ease;
        }
        
        .roast-box h3 {
            color: #FF6B6B;
            font-weight: 700;
            margin-top: 0;
        }
        
        .roast-box h4 {
            color: #FFA94D;
            margin-top: 1.2rem;
        }
        
        .roast-box table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        
        .roast-box table th {
            background: rgba(255, 107, 107, 0.2);
            padding: 0.8rem;
            text-align: left;
            font-weight: 600;
            color: #FFA94D;
        }
        
        .roast-box table td {
            padding: 0.6rem 0.8rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        
        .roast-box table tr:hover {
            background: rgba(255,255,255,0.03);
        }
        
        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(135deg, #FF6B6B 0%, #ee5a24 100%);
            color: white;
            border-radius: 30px;
            padding: 0.7rem 2.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
            letter-spacing: 0.02em;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(0px);
        }
        
        .btn-secondary > button {
            background: linear-gradient(135deg, #4D96FF 0%, #3b82f6 100%);
            box-shadow: 0 4px 15px rgba(77, 150, 255, 0.3);
        }
        
        .btn-secondary > button:hover {
            box-shadow: 0 8px 25px rgba(77, 150, 255, 0.4);
        }
        
        /* ===== DIVIDER ===== */
        .section-divider {
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, #e2e8f0, transparent);
            margin: 2rem 0;
        }
        
        /* ===== TAB STYLES ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background: #f1f5f9;
            border-radius: 12px;
            padding: 0.3rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            color: #64748b;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: white;
            color: #1e293b;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        
        /* ===== SIDEBAR ===== */
        .sidebar-content {
            padding: 1rem 0.5rem;
        }
        
        .sidebar-logo {
            text-align: center;
            padding: 1rem 0;
        }
        
        .sidebar-logo img {
            width: 80px;
            height: 80px;
        }
        
        /* ===== WELCOME STATE ===== */
        .welcome-container {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            border-radius: 24px;
            margin: 2rem 0;
        }
        
        .welcome-container h2 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
        }
        
        .welcome-container p {
            font-size: 1.1rem;
            color: #64748b;
            max-width: 600px;
            margin: 1rem auto;
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2.2rem;
            }
            
            .metric-value {
                font-size: 1.5rem;
            }
            
            .roast-box {
                padding: 1.2rem;
            }
        }
        
        /* ===== DATA EDITOR ===== */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
        
        /* ===== TOOLTIP ===== */
        .info-tooltip {
            color: #64748b;
            cursor: help;
            border-bottom: 1px dashed #cbd5e1;
        }
        
        /* ===== LOADING SPINNER ===== */
        .stSpinner > div {
            border-color: #FF6B6B !important;
        }
        
        /* ===== CUSTOM SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)