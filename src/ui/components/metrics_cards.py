"""
Metrics cards components for displaying network statistics.
"""

import streamlit as st
from typing import Dict, List
from ...core.graph import CityGraph
from ...core.metrics import NetworkMetrics
from ...ui.styles import get_metric_card_html

class MetricsCards:
    """Components for displaying network metrics and statistics"""
    
    @staticmethod
    def render_basic_metrics(city_graph: CityGraph):
        """Render basic network metrics"""
        stats = NetworkMetrics.get_network_stats(city_graph)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Intersections", stats['total_nodes'])
        with col2:
            st.metric("Total Roads", stats['total_edges'])
        with col3:
            st.metric("Network Density", f"{stats['density']:.3f}")
        with col4:
            st.metric("Average Degree", f"{stats['avg_degree']:.1f}")
    
    @staticmethod
    def render_advanced_metrics(city_graph: CityGraph):
        """Render advanced network metrics"""
        stats = NetworkMetrics.get_network_stats(city_graph)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Dead Ends", stats['dead_ends'])
        with col2:
            st.metric("Components", stats['components'])
        with col3:
            st.metric("Avg Distance", f"{stats['avg_distance']:.2f} km")
        with col4:
            st.metric("Avg Time", f"{stats['avg_time']:.3f} hours")
    
    @staticmethod
    def render_connectivity_status(city_graph: CityGraph):
        """Render connectivity status with visual indicators"""
        from ...core.algorithms import ConnectivityAlgorithm
        
        is_connected = ConnectivityAlgorithm.is_connected(city_graph)
        has_cycles = ConnectivityAlgorithm.has_cycle(city_graph)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if is_connected:
                st.success("✅ Network is fully connected")
            else:
                st.error("❌ Network is not connected")
                components = ConnectivityAlgorithm.get_components(city_graph)
                st.write(f"Number of components: {len(components)}")
        
        with col2:
            if has_cycles:
                st.warning("🔄 Network contains cycles")
            else:
                st.info("🔄 No cycles detected")
    
    @staticmethod
    def render_degree_distribution(city_graph: CityGraph):
        """Render degree distribution information"""
        degree_dist = NetworkMetrics.get_degree_distribution(city_graph)
        
        if degree_dist:
            st.subheader("Degree Distribution")
            for degree, count in sorted(degree_dist.items()):
                st.write(f"Degree {degree}: {count} intersection(s)")
        else:
            st.info("No degree distribution data available")
    
    @staticmethod
    def render_centrality_metrics(city_graph: CityGraph):
        """Render centrality metrics"""
        centrality_metrics = NetworkMetrics.get_centrality_metrics(city_graph)
        
        if centrality_metrics:
            st.subheader("Centrality Metrics")
            
            # Degree centrality
            if 'degree' in centrality_metrics:
                st.write("**Degree Centrality:**")
                degree_data = centrality_metrics['degree']
                for node, centrality in sorted(degree_data.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• {node}: {centrality:.3f}")
            
            # Betweenness centrality
            if 'betweenness' in centrality_metrics:
                st.write("**Betweenness Centrality:**")
                betweenness_data = centrality_metrics['betweenness']
                for node, centrality in sorted(betweenness_data.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• {node}: {centrality:.3f}")
            
            # Closeness centrality
            if 'closeness' in centrality_metrics:
                st.write("**Closeness Centrality:**")
                closeness_data = centrality_metrics['closeness']
                for node, centrality in sorted(closeness_data.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• {node}: {centrality:.3f}")
        else:
            st.info("No centrality metrics available")
    
    @staticmethod
    def render_efficiency_metrics(city_graph: CityGraph):
        """Render network efficiency metrics"""
        efficiency_metrics = NetworkMetrics.get_network_efficiency(city_graph)
        
        if efficiency_metrics:
            st.subheader("Network Efficiency")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Global Efficiency", f"{efficiency_metrics['global_efficiency']:.3f}")
            with col2:
                st.metric("Local Efficiency", f"{efficiency_metrics['local_efficiency']:.3f}")
            with col3:
                st.metric("Connectivity Score", f"{efficiency_metrics['connectivity_score']:.3f}")
        else:
            st.info("No efficiency metrics available")
    
    @staticmethod
    def render_component_details(city_graph: CityGraph):
        """Render detailed component information"""
        from ...core.algorithms import ConnectivityAlgorithm
        
        components = ConnectivityAlgorithm.get_components(city_graph)
        
        if len(components) > 1:
            st.subheader("Connected Components")
            st.write(f"Network has {len(components)} disconnected components:")
            
            for i, component in enumerate(components, 1):
                with st.expander(f"Component {i} ({len(component)} intersections)"):
                    st.write(f"**Intersections:** {', '.join(sorted(component))}")
                    
                    # Calculate component stats
                    component_edges = 0
                    for node in component:
                        for neighbor in city_graph.adjacency_list.get(node, []):
                            if neighbor in component:
                                component_edges += 1
                    component_edges //= 2  # Avoid double counting
                    
                    st.write(f"**Internal roads:** {component_edges}")
                    
                    if len(component) > 1:
                        max_possible = len(component) * (len(component) - 1) // 2
                        density = component_edges / max_possible if max_possible > 0 else 0
                        st.write(f"**Component density:** {density:.3f}")
        else:
            st.success("Network is fully connected (single component)")
    
    @staticmethod
    def render_path_metrics(city_graph: CityGraph, path: List[str]):
        """Render metrics for a specific path"""
        if not path or len(path) < 2:
            return
        
        st.subheader("Path Metrics")
        
        # Calculate path statistics
        total_distance = 0
        total_time = 0
        path_details = []
        
        for i in range(len(path) - 1):
            n1, n2 = path[i], path[i+1]
            distance = city_graph.get_edge_distance(n1, n2)
            time = city_graph.get_edge_time(n1, n2)
            speed = city_graph.get_edge_speed_limit(n1, n2)
            
            total_distance += distance
            total_time += time
            
            path_details.append({
                "From": n1,
                "To": n2,
                "Distance (km)": f"{distance:.2f}",
                "Time (h)": f"{time:.3f}",
                "Speed (km/h)": f"{speed:.1f}"
            })
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Distance", f"{total_distance:.2f} km")
        with col2:
            st.metric("Total Time", f"{total_time:.3f} hours")
        with col3:
            st.metric("Path Length", f"{len(path) - 1} roads")
        
        # Show path details
        with st.expander("Path Details"):
            st.dataframe(path_details, use_container_width=True)
    
    @staticmethod
    def render_mst_metrics(city_graph: CityGraph, mst_edges: List[tuple]):
        """Render metrics for Minimum Spanning Tree"""
        if not mst_edges:
            return
        
        st.subheader("MST Metrics")
        
        # Calculate MST statistics
        total_weight = 0
        mst_details = []
        
        for node1, node2 in mst_edges:
            weight = city_graph.get_edge_weight(node1, node2)
            distance = city_graph.get_edge_distance(node1, node2)
            time = city_graph.get_edge_time(node1, node2)
            speed = city_graph.get_edge_speed_limit(node1, node2)
            
            total_weight += weight
            
            mst_details.append({
                "From": node1,
                "To": node2,
                "Weight": f"{weight:.3f}",
                "Distance (km)": f"{distance:.2f}",
                "Time (h)": f"{time:.3f}",
                "Speed (km/h)": f"{speed:.1f}"
            })
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Weight", f"{total_weight:.3f}")
        with col2:
            st.metric("MST Edges", len(mst_edges))
        with col3:
            total_edges = sum(len(neighbors) for neighbors in city_graph.adjacency_list.values()) // 2
            efficiency = len(mst_edges) / total_edges if total_edges > 0 else 0
            st.metric("Efficiency", f"{efficiency:.3f}")
        
        # Show MST details
        with st.expander("MST Details"):
            st.dataframe(mst_details, use_container_width=True) 