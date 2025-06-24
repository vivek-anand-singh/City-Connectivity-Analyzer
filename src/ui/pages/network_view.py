"""
Network View Page
Renders the network visualization and basic metrics.
"""

import streamlit as st
from src.visualization.network_plots import NetworkPlotter
from src.ui.components.metrics_cards import MetricsCards

def render_network_view():
    """Render the network view tab"""
    st.header("🗺️ Network View")
    
    # Network visualization
    fig = NetworkPlotter.create_network_graph(st.session_state.city_graph, st.session_state.current_path)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show basic network info
    MetricsCards.render_basic_metrics(st.session_state.city_graph)
    
    # Weighted network view
    st.subheader("Weighted Network View")
    weighted_fig = NetworkPlotter.create_weighted_network_graph(
        st.session_state.city_graph, 
        st.session_state.current_path,
        st.session_state.current_mst
    )
    st.plotly_chart(weighted_fig, use_container_width=True) 