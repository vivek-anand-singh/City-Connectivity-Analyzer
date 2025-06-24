"""
Advanced Algorithms Page
Renders advanced algorithm implementations like MST.
"""

import streamlit as st
from src.core.algorithms import GraphAlgorithms
from src.ui.components.metrics_cards import MetricsCards
from src.visualization.network_plots import NetworkPlotter

def render_advanced_algorithms():
    """Render the advanced algorithms tab"""
    st.header("🚀 Advanced Algorithms")
    
    # Dijkstra's Algorithm
    st.subheader("Dijkstra's Shortest Path")
    st.write("Find the shortest path between any two intersections.")
    
    # Kruskal's MST
    st.subheader("Kruskal's Minimum Spanning Tree")
    if st.button("Find MST"):
        mst_edges, total_weight = GraphAlgorithms.kruskal_mst(st.session_state.city_graph)
        st.session_state.current_mst = mst_edges
        
        if mst_edges:
            st.success(f"MST found with {len(mst_edges)} edges, total weight: {total_weight:.2f}")
            st.write("**MST Edges:**")
            for edge in mst_edges:
                st.write(f"• {edge[0]} - {edge[1]}")
        else:
            st.warning("No MST found (empty or disconnected graph)")
    
    # MST metrics
    if st.session_state.current_mst:
        MetricsCards.render_mst_metrics(st.session_state.city_graph, st.session_state.current_mst)
        
        # MST visualization
        st.subheader("MST Visualization")
        mst_fig = NetworkPlotter.create_weighted_network_graph(
            st.session_state.city_graph, 
            None, 
            st.session_state.current_mst
        )
        st.plotly_chart(mst_fig, use_container_width=True) 