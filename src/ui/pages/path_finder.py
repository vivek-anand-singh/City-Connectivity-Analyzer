"""
Path Finder Page
Renders the path finding interface and visualization.
"""

import streamlit as st
from src.core.algorithms import GraphAlgorithms
from src.ui.components.metrics_cards import MetricsCards
from src.visualization.network_plots import NetworkPlotter

def render_path_finder():
    """Render the path finder tab"""
    st.header("🛣️ Path Finder")
    
    if len(st.session_state.city_graph.nodes) < 2:
        st.warning("Need at least 2 intersections to find paths")
        return
    
    nodes_list = list(st.session_state.city_graph.nodes)
    col1, col2 = st.columns(2)
    
    with col1:
        start_node = st.selectbox("Start Intersection", nodes_list)
        end_node = st.selectbox("End Intersection", nodes_list)
        
        if st.button("Find Shortest Path"):
            if start_node != end_node:
                path, distance = GraphAlgorithms.dijkstra_shortest_path(
                    st.session_state.city_graph, start_node, end_node
                )
                st.session_state.current_path = path
                
                if path:
                    st.success(f"Path found! Distance: {distance:.2f}")
                else:
                    st.error("No path found between these intersections")
            else:
                st.warning("Start and end intersections must be different")
    
    with col2:
        if st.session_state.current_path:
            st.subheader("Shortest Path")
            path_str = " → ".join(st.session_state.current_path)
            st.write(f"**Route:** {path_str}")
            
            # Path metrics
            MetricsCards.render_path_metrics(st.session_state.city_graph, st.session_state.current_path)
    
    # Path visualization
    if st.session_state.current_path:
        st.subheader("Path Visualization")
        path_fig = NetworkPlotter.create_network_graph(st.session_state.city_graph, st.session_state.current_path)
        st.plotly_chart(path_fig, use_container_width=True) 