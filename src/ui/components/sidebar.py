"""
Sidebar components for the City Connectivity Analyzer.
Handles all sidebar controls and interactions.
"""

import streamlit as st
from typing import Optional
from ...core.graph import CityGraph
from ...utils.data_loader import DataLoader

class SidebarComponents:
    """Sidebar UI components and controls"""
    
    @staticmethod
    def render_metric_selector(city_graph: CityGraph) -> str:
        """Render metric type selection"""
        st.subheader("📊 Analysis Type")
        metric_type = st.selectbox(
            "Choose Metric Type",
            options=["distance", "time"],
            format_func=lambda x: "Distance-based" if x == "distance" else "Time-based",
            key="metric_selector"
        )
        
        if metric_type != st.session_state.get('metric_type', 'distance'):
            st.session_state.metric_type = metric_type
            city_graph.set_metric_type(metric_type)
            st.rerun()
        
        st.info(f"Currently analyzing by: **{'Distance' if metric_type == 'distance' else 'Time'}**")
        return metric_type
    
    @staticmethod
    def render_node_controls(city_graph: CityGraph):
        """Render node (intersection) management controls"""
        st.subheader("Intersections (Nodes)")
        col1, col2 = st.columns(2)
        
        with col1:
            new_node = st.text_input("Add Intersection", placeholder="e.g., A, B, C")
            if st.button("Add Node"):
                if new_node and new_node.strip():
                    if city_graph.add_node(new_node.strip()):
                        st.success(f"Added intersection: {new_node}")
                        st.rerun()
                    else:
                        st.error("Intersection already exists!")
        
        with col2:
            remove_node = st.selectbox("Remove Intersection", 
                                     options=[''] + list(city_graph.nodes))
            if st.button("Remove Node") and remove_node:
                if city_graph.remove_node(remove_node):
                    st.success(f"Removed intersection: {remove_node}")
                    st.rerun()
    
    @staticmethod
    def render_edge_controls(city_graph: CityGraph):
        """Render edge (road) management controls"""
        st.subheader("Roads (Edges)")
        if len(city_graph.nodes) >= 2:
            nodes_list = list(city_graph.nodes)
            col1, col2 = st.columns(2)
            
            with col1:
                node1 = st.selectbox("From", options=nodes_list)
                node2 = st.selectbox("To", options=nodes_list)
                weight = st.number_input("Distance (km)", min_value=0.1, value=1.0, step=0.1)
                speed_limit = st.number_input("Speed Limit (km/h)", min_value=5.0, value=30.0, step=5.0)
                if st.button("Add Road"):
                    if node1 != node2:
                        if city_graph.add_edge(node1, node2, weight, speed_limit):
                            st.success(f"Added road: {node1} → {node2}")
                            st.rerun()
                        else:
                            st.error("Road already exists!")
                    else:
                        st.error("Cannot connect intersection to itself!")
            
            with col2:
                existing_edges = []
                for n1 in nodes_list:
                    for n2 in city_graph.adjacency_list.get(n1, []):
                        if n1 < n2:  # Avoid duplicates
                            weight = city_graph.get_edge_distance(n1, n2)
                            speed = city_graph.get_edge_speed_limit(n1, n2)
                            existing_edges.append(f"{n1} - {n2} ({weight}km, {speed}km/h)")
                
                if existing_edges:
                    remove_edge = st.selectbox("Remove Road", options=[''] + existing_edges)
                    if st.button("Remove Road") and remove_edge:
                        edge_info = remove_edge.split(" (")[0]
                        n1, n2 = edge_info.split(" - ")
                        if city_graph.remove_edge(n1, n2):
                            st.success(f"Removed road: {remove_edge}")
                            st.rerun()
        else:
            st.info("Add at least 2 intersections to connect roads")
    
    @staticmethod
    def render_sample_data_controls(city_graph: CityGraph):
        """Render sample data loading controls"""
        st.subheader("Sample Data")
        sample_cities = DataLoader.get_sample_cities()
        selected_city = st.selectbox("Choose Sample City", [''] + list(sample_cities.keys()))
        
        if st.button("Load Sample City") and selected_city:
            DataLoader.load_city_by_name(city_graph, selected_city)
            st.success(f"Loaded {sample_cities[selected_city]}!")
            st.rerun()
        
        if st.button("Clear All"):
            city_graph.clear()
            st.session_state.current_path = None
            st.session_state.current_mst = None
            st.success("Cleared all data!")
            st.rerun()
    
    @staticmethod
    def render_network_info(city_graph: CityGraph):
        """Render network information in sidebar"""
        if city_graph.nodes:
            st.subheader("📈 Network Info")
            
            # Basic stats
            total_nodes = len(city_graph.nodes)
            total_edges = sum(len(neighbors) for neighbors in city_graph.adjacency_list.values()) // 2
            
            st.metric("Intersections", total_nodes)
            st.metric("Roads", total_edges)
            
            # Density
            if total_nodes > 1:
                max_possible_edges = total_nodes * (total_nodes - 1) // 2
                density = total_edges / max_possible_edges
                st.metric("Density", f"{density:.3f}")
            
            # Connectivity status
            from ...core.algorithms import ConnectivityAlgorithm
            is_connected = ConnectivityAlgorithm.is_connected(city_graph)
            status = "✅ Connected" if is_connected else "❌ Disconnected"
            st.info(f"**Status:** {status}")
    
    @staticmethod
    def render_sidebar(city_graph: CityGraph) -> str:
        """Render the complete sidebar"""
        with st.sidebar:
            st.header("🏗️ Graph Controls")
            
            # Metric selector
            metric_type = SidebarComponents.render_metric_selector(city_graph)
            
            # Node controls
            SidebarComponents.render_node_controls(city_graph)
            
            # Edge controls
            SidebarComponents.render_edge_controls(city_graph)
            
            # Sample data controls
            SidebarComponents.render_sample_data_controls(city_graph)
            
            # Network info
            SidebarComponents.render_network_info(city_graph)
        
        return metric_type 