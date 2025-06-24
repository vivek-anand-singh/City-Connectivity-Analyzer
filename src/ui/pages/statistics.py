"""
Statistics Page
Renders comprehensive network statistics and charts.
"""

import streamlit as st
from src.core.metrics import NetworkMetrics
from src.ui.components.metrics_cards import MetricsCards
from src.visualization.charts import ChartCreator

def render_statistics():
    """Render the statistics tab"""
    st.header("📊 Network Statistics")
    
    # Basic metrics
    MetricsCards.render_basic_metrics(st.session_state.city_graph)
    
    # Advanced metrics
    MetricsCards.render_advanced_metrics(st.session_state.city_graph)
    
    # Efficiency metrics
    MetricsCards.render_efficiency_metrics(st.session_state.city_graph)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Degree Distribution")
        degree_fig = ChartCreator.create_degree_chart(st.session_state.city_graph)
        st.plotly_chart(degree_fig, use_container_width=True)
        
        st.subheader("Degree Distribution Histogram")
        degree_dist_fig = ChartCreator.create_degree_distribution_chart(st.session_state.city_graph)
        st.plotly_chart(degree_dist_fig, use_container_width=True)
    
    with col2:
        st.subheader("Network Statistics Overview")
        stats = NetworkMetrics.get_network_stats(st.session_state.city_graph)
        stats_fig = ChartCreator.create_network_stats_chart(stats)
        st.plotly_chart(stats_fig, use_container_width=True)
        
        st.subheader("Network Properties")
        connectivity_fig = ChartCreator.create_connectivity_status(stats)
        st.plotly_chart(connectivity_fig, use_container_width=True)
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Edge Weight Distribution")
        weight_fig = ChartCreator.create_edge_weight_distribution(st.session_state.city_graph)
        st.plotly_chart(weight_fig, use_container_width=True)
    
    with col2:
        st.subheader("Speed Limit Distribution")
        speed_fig = ChartCreator.create_speed_limit_distribution(st.session_state.city_graph)
        st.plotly_chart(speed_fig, use_container_width=True)
    
    # Centrality metrics
    st.subheader("Centrality Analysis")
    centrality_type = st.selectbox("Centrality Type", ["degree", "betweenness", "closeness"])
    centrality_fig = ChartCreator.create_centrality_chart(st.session_state.city_graph, centrality_type)
    st.plotly_chart(centrality_fig, use_container_width=True)
    
    # Efficiency chart
    st.subheader("Network Efficiency")
    efficiency_fig = ChartCreator.create_efficiency_chart(st.session_state.city_graph)
    st.plotly_chart(efficiency_fig, use_container_width=True)
    
    # Detailed metrics
    MetricsCards.render_degree_distribution(st.session_state.city_graph)
    MetricsCards.render_centrality_metrics(st.session_state.city_graph) 