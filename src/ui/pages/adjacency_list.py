"""
Adjacency List Page
Renders the adjacency list and edge details.
"""

import streamlit as st

def render_adjacency_list():
    """Render the adjacency list tab"""
    st.header("📋 Adjacency List")
    
    adjacency_str = st.session_state.city_graph.get_adjacency_list_str()
    st.code(adjacency_str, language="text")
    
    # Show edge details
    st.subheader("Edge Details")
    if st.session_state.city_graph.edge_weights:
        edge_data = []
        for (n1, n2), weight in st.session_state.city_graph.edge_weights.items():
            if n1 < n2:  # Avoid duplicates
                speed = st.session_state.city_graph.get_edge_speed_limit(n1, n2)
                time = st.session_state.city_graph.get_edge_time(n1, n2)
                edge_data.append({
                    "From": n1,
                    "To": n2,
                    "Distance (km)": f"{weight:.2f}",
                    "Speed (km/h)": f"{speed:.1f}",
                    "Time (h)": f"{time:.3f}"
                })
        
        if edge_data:
            st.dataframe(edge_data, use_container_width=True) 