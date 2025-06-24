"""
Statistical charts and visualizations for city road network analysis.
Handles bar charts, pie charts, and other statistical plots.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import pandas as pd
from ..core.graph import CityGraph
from ..core.metrics import NetworkMetrics

class ChartCreator:
    """Creates statistical charts and visualizations"""
    
    @staticmethod
    def create_degree_chart(city_graph: CityGraph) -> go.Figure:
        """Create a bar chart showing intersection degrees"""
        if not city_graph.nodes:
            fig = go.Figure()
            fig.update_layout(
                title='Intersection Degrees',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        degrees = city_graph.get_all_degrees()
        nodes = list(degrees.keys())
        degree_values = list(degrees.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=nodes,
                y=degree_values,
                marker_color='lightblue',
                text=degree_values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Intersection Degrees (Number of Connections)',
            xaxis_title='Intersection',
            yaxis_title='Number of Connections',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_network_stats_chart(stats: Dict) -> go.Figure:
        """Create a chart showing network statistics"""
        if not stats:
            fig = go.Figure()
            fig.update_layout(
                title='Network Statistics',
                annotations=[dict(text="No data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        # Create metrics display
        metrics = [
            ('Total Intersections', stats.get('total_nodes', 0)),
            ('Total Roads', stats.get('total_edges', 0)),
            ('Dead Ends', stats.get('dead_ends', 0)),
            ('Connected Components', stats.get('components', 0))
        ]
        
        labels, values = zip(*metrics)
        colors = ['lightblue', 'lightgreen', 'orange', 'lightcoral']
        
        fig = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Network Statistics Overview',
            xaxis_title='Metric',
            yaxis_title='Count',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_connectivity_status(stats: Dict) -> go.Figure:
        """Create a pie chart showing connectivity status"""
        if not stats:
            fig = go.Figure()
            fig.update_layout(
                title='Connectivity Status',
                annotations=[dict(text="No data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        # Connectivity status
        is_connected = stats.get('is_connected', False)
        has_cycles = stats.get('has_cycles', False)
        
        labels = []
        values = []
        colors = []
        
        if is_connected:
            labels.append('Connected')
            values.append(1)
            colors.append('green')
        else:
            labels.append('Disconnected')
            values.append(1)
            colors.append('red')
        
        if has_cycles:
            labels.append('Has Cycles')
            values.append(1)
            colors.append('orange')
        else:
            labels.append('No Cycles')
            values.append(1)
            colors.append('blue')
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                marker_colors=colors,
                hole=0.3
            )
        ])
        
        fig.update_layout(
            title='Network Properties',
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def create_degree_distribution_chart(city_graph: CityGraph) -> go.Figure:
        """Create a histogram showing degree distribution"""
        if not city_graph.nodes:
            fig = go.Figure()
            fig.update_layout(
                title='Degree Distribution',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        degree_dist = NetworkMetrics.get_degree_distribution(city_graph)
        
        if not degree_dist:
            fig = go.Figure()
            fig.update_layout(
                title='Degree Distribution',
                annotations=[dict(text="No degree data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        degrees = list(degree_dist.keys())
        counts = list(degree_dist.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=degrees,
                y=counts,
                marker_color='lightblue',
                text=counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Degree Distribution',
            xaxis_title='Degree (Number of Connections)',
            yaxis_title='Number of Intersections',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_edge_weight_distribution(city_graph: CityGraph) -> go.Figure:
        """Create a histogram showing edge weight distribution"""
        if not city_graph.edge_weights:
            fig = go.Figure()
            fig.update_layout(
                title='Edge Weight Distribution',
                annotations=[dict(text="No roads yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        weights = []
        for (n1, n2), weight in city_graph.edge_weights.items():
            if n1 < n2:  # Avoid duplicates
                weights.append(weight)
        
        if not weights:
            fig = go.Figure()
            fig.update_layout(
                title='Edge Weight Distribution',
                annotations=[dict(text="No weight data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        fig = go.Figure(data=[
            go.Histogram(
                x=weights,
                nbinsx=10,
                marker_color='lightgreen',
                opacity=0.7
            )
        ])
        
        metric_type = "Time (hours)" if city_graph.get_metric_type() == "time" else "Distance (km)"
        fig.update_layout(
            title='Edge Weight Distribution',
            xaxis_title=metric_type,
            yaxis_title='Number of Roads',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_speed_limit_distribution(city_graph: CityGraph) -> go.Figure:
        """Create a histogram showing speed limit distribution"""
        if not city_graph.speed_limits:
            fig = go.Figure()
            fig.update_layout(
                title='Speed Limit Distribution',
                annotations=[dict(text="No roads yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        speeds = []
        for (n1, n2), speed in city_graph.speed_limits.items():
            if n1 < n2:  # Avoid duplicates
                speeds.append(speed)
        
        if not speeds:
            fig = go.Figure()
            fig.update_layout(
                title='Speed Limit Distribution',
                annotations=[dict(text="No speed data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        fig = go.Figure(data=[
            go.Histogram(
                x=speeds,
                nbinsx=10,
                marker_color='lightcoral',
                opacity=0.7
            )
        ])
        
        fig.update_layout(
            title='Speed Limit Distribution',
            xaxis_title='Speed Limit (km/h)',
            yaxis_title='Number of Roads',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_centrality_chart(city_graph: CityGraph, centrality_type: str = "degree") -> go.Figure:
        """Create a bar chart showing centrality metrics"""
        if not city_graph.nodes:
            fig = go.Figure()
            fig.update_layout(
                title='Centrality Metrics',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        centrality_metrics = NetworkMetrics.get_centrality_metrics(city_graph)
        
        if not centrality_metrics or centrality_type not in centrality_metrics:
            fig = go.Figure()
            fig.update_layout(
                title=f'{centrality_type.title()} Centrality',
                annotations=[dict(text="No centrality data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        centrality_data = centrality_metrics[centrality_type]
        nodes = list(centrality_data.keys())
        values = list(centrality_data.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=nodes,
                y=values,
                marker_color='lightblue',
                text=[f"{v:.3f}" for v in values],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=f'{centrality_type.title()} Centrality',
            xaxis_title='Intersection',
            yaxis_title=f'{centrality_type.title()} Centrality',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_efficiency_chart(city_graph: CityGraph) -> go.Figure:
        """Create a chart showing network efficiency metrics"""
        if not city_graph.nodes:
            fig = go.Figure()
            fig.update_layout(
                title='Network Efficiency',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        efficiency_metrics = NetworkMetrics.get_network_efficiency(city_graph)
        
        if not efficiency_metrics:
            fig = go.Figure()
            fig.update_layout(
                title='Network Efficiency',
                annotations=[dict(text="No efficiency data available!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        metrics = list(efficiency_metrics.keys())
        values = list(efficiency_metrics.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=metrics,
                y=values,
                marker_color='lightgreen',
                text=[f"{v:.3f}" for v in values],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Network Efficiency Metrics',
            xaxis_title='Efficiency Metric',
            yaxis_title='Value',
            showlegend=False
        )
        
        return fig 