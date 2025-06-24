"""
City Connectivity Analyzer - Main Application
A modular Streamlit application for analyzing city road networks using graph algorithms.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.core.graph import CityGraph
from src.core.algorithms import GraphAlgorithms
from src.core.metrics import NetworkMetrics
from src.utils.data_loader import DataLoader
from src.ui.styles import get_custom_css
from src.ui.components.sidebar import SidebarComponents
from src.ui.components.metrics_cards import MetricsCards
from src.visualization.network_plots import NetworkPlotter
from src.visualization.charts import ChartCreator
from src.ui.pages import (
    render_network_view,
    render_analysis,
    render_path_finder,
    render_advanced_algorithms,
    render_statistics,
    render_adjacency_list,
    render_welcome_screen
)

# Page configuration
st.set_page_config(
    page_title="City Connectivity Analyzer",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'city_graph' not in st.session_state:
    st.session_state.city_graph = CityGraph()
if 'current_path' not in st.session_state:
    st.session_state.current_path = None
if 'current_mst' not in st.session_state:
    st.session_state.current_mst = None
if 'metric_type' not in st.session_state:
    st.session_state.metric_type = "distance"

def main():
    """Main application function"""
    # Header
    st.markdown('<h1 class="main-header">🏙️ City Connectivity Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive road network analysis with graph algorithms")
    
    # Sidebar
    metric_type = SidebarComponents.render_sidebar(st.session_state.city_graph)
    
    # Main content
    if st.session_state.city_graph.nodes:
        render_main_content()
    else:
        render_welcome_screen()

def render_main_content():
    """Render the main content area with tabs"""
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🗺️ Network View", "🔍 Analysis", "🛣️ Path Finder", "🚀 Advanced Algorithms", "📊 Statistics", "📋 Adjacency List"
    ])
    
    with tab1:
        render_network_view()
    
    with tab2:
        render_analysis()
    
    with tab3:
        render_path_finder()
    
    with tab4:
        render_advanced_algorithms()
    
    with tab5:
        render_statistics()
    
    with tab6:
        render_adjacency_list()

if __name__ == "__main__":
    main() 