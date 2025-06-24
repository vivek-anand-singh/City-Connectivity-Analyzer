"""
Analysis Page
Renders network analysis including connectivity, dead ends, and components.
"""

import streamlit as st
from src.core.algorithms import GraphAlgorithms
from src.ui.components.metrics_cards import MetricsCards
from src.visualization.network_plots import NetworkPlotter

def render_analysis():
    """Render the analysis tab"""
    st.header("🔍 Network Analysis")
    
    # Connectivity status
    MetricsCards.render_connectivity_status(st.session_state.city_graph)
    
    # Get analysis results
    dead_ends = GraphAlgorithms.find_dead_ends(st.session_state.city_graph)
    components = GraphAlgorithms.get_components(st.session_state.city_graph)
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dead Ends")
        if dead_ends:
            st.write(f"Found {len(dead_ends)} dead end(s):")
            for dead_end in dead_ends:
                st.write(f"• {dead_end}")
        else:
            st.success("No dead ends found")
    
    with col2:
        st.subheader("Components")
        if len(components) > 1:
            st.write(f"Network has {len(components)} disconnected components:")
            for i, component in enumerate(components, 1):
                st.write(f"Component {i}: {', '.join(sorted(component))}")
        else:
            st.success("Network is fully connected")
    
    # Component details
    MetricsCards.render_component_details(st.session_state.city_graph)
    
    # Components visualization
    st.subheader("Components Visualization")
    components_fig = NetworkPlotter.create_components_visualization(st.session_state.city_graph)
    st.plotly_chart(components_fig, use_container_width=True) 