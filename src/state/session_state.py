"""
Session state management for the Expense Roaster
"""

import streamlit as st
from typing import Any, Optional
import pandas as pd

class SessionStateManager:
    """Manage session state with type safety"""
    
    KEYS = {
        'df': None,  # DataFrame
        'roast_generated': False,  # Boolean
        'roast_result': None,  # String
        'roast_metadata': None,  # Dict
        'selected_tab': 0,  # Integer
        'filters': {},  # Dict
    }
    
    @classmethod
    def initialize(cls):
        """Initialize all session state variables"""
        for key, default_value in cls.KEYS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @classmethod
    def get_df(cls) -> Optional[pd.DataFrame]:
        """Get the current DataFrame"""
        return st.session_state.get('df', None)
    
    @classmethod
    def set_df(cls, df: pd.DataFrame):
        """Set the DataFrame"""
        st.session_state.df = df
    
    @classmethod
    def get_roast_result(cls) -> Optional[str]:
        """Get the roast result"""
        return st.session_state.get('roast_result', None)
    
    @classmethod
    def set_roast_result(cls, result: str):
        """Set the roast result"""
        st.session_state.roast_result = result
        st.session_state.roast_generated = True
    
    @classmethod
    def clear_roast(cls):
        """Clear the roast result"""
        st.session_state.roast_result = None
        st.session_state.roast_generated = False
    
    @classmethod
    def reset_all(cls):
        """Reset all session state"""
        for key in cls.KEYS.keys():
            if key in st.session_state:
                del st.session_state[key]
        cls.initialize()

def initialize_session_state():
    """Convenience function to initialize session state"""
    SessionStateManager.initialize()