"""
Network visualization module for city road networks.
Handles interactive network graphs and plots.
"""

import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional, Tuple
import pandas as pd
from ..core.graph import CityGraph

class NetworkPlotter:
    """Handles network visualization and plotting"""
    
    @staticmethod
    def create_network_graph(city_graph: CityGraph, highlight_path: Optional[List[str]] = None) -> go.Figure:
        """Create a network graph showing the city road network"""
        if not city_graph.nodes:
            # Create empty figure
            fig = go.Figure()
            fig.update_layout(
                title='City Road Network',
                xaxis_title='',
                yaxis_title='',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        # Convert to NetworkX for layout
        G = city_graph.to_networkx()
        
        # Get positions using spring layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Create edge traces - separate for regular and highlighted edges
        regular_edge_x = []
        regular_edge_y = []
        highlighted_edge_x = []
        highlighted_edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            # Check if this edge is part of the highlighted path
            is_highlighted = False
            if highlight_path:
                for i in range(len(highlight_path) - 1):
                    if (highlight_path[i] == edge[0] and highlight_path[i+1] == edge[1]) or \
                       (highlight_path[i] == edge[1] and highlight_path[i+1] == edge[0]):
                        is_highlighted = True
                        break
            
            if is_highlighted:
                highlighted_edge_x.extend([x0, x1, None])
                highlighted_edge_y.extend([y0, y1, None])
            else:
                regular_edge_x.extend([x0, x1, None])
                regular_edge_y.extend([y0, y1, None])
        
        # Create regular edge trace
        regular_edge_trace = go.Scatter(
            x=regular_edge_x, y=regular_edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        )
        
        # Create highlighted edge trace
        highlighted_edge_trace = None
        if highlighted_edge_x:
            highlighted_edge_trace = go.Scatter(
                x=highlighted_edge_x, y=highlighted_edge_y,
                line=dict(width=3, color='red'),
                hoverinfo='none',
                mode='lines',
                showlegend=False
            )
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            degree = city_graph.get_degree(node)
            node_text.append(f"Intersection {node}<br>Connections: {degree}")
            
            # Color nodes based on properties
            if highlight_path and node in highlight_path:
                node_colors.append('red')  # Path nodes
                node_sizes.append(25)
            elif degree == 1:
                node_colors.append('orange')  # Dead ends
                node_sizes.append(20)
            elif degree >= 4:
                node_colors.append('green')  # Major intersections
                node_sizes.append(22)
            else:
                node_colors.append('lightblue')  # Regular intersections
                node_sizes.append(18)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        # Create figure with appropriate traces
        traces = [regular_edge_trace, node_trace]
        if highlighted_edge_trace:
            traces.insert(0, highlighted_edge_trace)
        
        fig = go.Figure(data=traces,
                       layout=go.Layout(
                           title='City Road Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    @staticmethod
    def create_weighted_network_graph(city_graph: CityGraph, highlight_path: Optional[List[str]] = None, 
                                    highlight_mst: Optional[List[tuple]] = None) -> go.Figure:
        """Create a weighted network graph with edge weights displayed"""
        if not city_graph.nodes:
            fig = go.Figure()
            fig.update_layout(
                title='Weighted City Road Network',
                xaxis_title='',
                yaxis_title='',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        # Convert to NetworkX for layout
        G = city_graph.to_networkx()
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Create edge traces - separate by color
        edge_traces = []
        
        # Group edges by color
        edge_groups = {
            'default': {'x': [], 'y': [], 'text': [], 'width': 2},
            'highlighted': {'x': [], 'y': [], 'text': [], 'width': 4},
            'mst': {'x': [], 'y': [], 'text': [], 'width': 3}
        }
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            # Get edge weight and format text
            weight = city_graph.get_edge_weight(edge[0], edge[1])
            distance = city_graph.get_edge_distance(edge[0], edge[1])
            speed = city_graph.get_edge_speed_limit(edge[0], edge[1])
            
            if city_graph.get_metric_type() == "time":
                edge_text = f"Time: {weight:.3f}h<br>Distance: {distance:.1f}km<br>Speed: {speed:.0f}km/h"
            else:
                edge_text = f"Distance: {weight:.1f}km<br>Speed: {speed:.0f}km/h<br>Time: {distance/speed:.3f}h"
            
            # Determine edge group based on highlighting
            if highlight_path:
                is_path_edge = False
                for i in range(len(highlight_path) - 1):
                    if (highlight_path[i] == edge[0] and highlight_path[i+1] == edge[1]) or \
                       (highlight_path[i] == edge[1] and highlight_path[i+1] == edge[0]):
                        is_path_edge = True
                        break
                if is_path_edge:
                    group = 'highlighted'
                else:
                    group = 'default'
            elif highlight_mst:
                is_mst_edge = (edge[0], edge[1]) in highlight_mst or (edge[1], edge[0]) in highlight_mst
                if is_mst_edge:
                    group = 'mst'
                else:
                    group = 'default'
            else:
                group = 'default'
            
            # Add to appropriate group
            edge_groups[group]['x'].extend([x0, x1, None])
            edge_groups[group]['y'].extend([y0, y1, None])
            # For line segments, we need to add text for each segment point
            edge_groups[group]['text'].extend([edge_text, edge_text, ''])
        
        # Create traces for each group
        if edge_groups['default']['x']:
            edge_traces.append(go.Scatter(
                x=edge_groups['default']['x'],
                y=edge_groups['default']['y'],
                line=dict(width=edge_groups['default']['width'], color='#888'),
                hoverinfo='text',
                text=edge_groups['default']['text'],
                mode='lines',
                showlegend=False
            ))
        
        if edge_groups['highlighted']['x']:
            edge_traces.append(go.Scatter(
                x=edge_groups['highlighted']['x'],
                y=edge_groups['highlighted']['y'],
                line=dict(width=edge_groups['highlighted']['width'], color='red'),
                hoverinfo='text',
                text=edge_groups['highlighted']['text'],
                mode='lines',
                showlegend=False
            ))
        
        if edge_groups['mst']['x']:
            edge_traces.append(go.Scatter(
                x=edge_groups['mst']['x'],
                y=edge_groups['mst']['y'],
                line=dict(width=edge_groups['mst']['width'], color='green'),
                hoverinfo='text',
                text=edge_groups['mst']['text'],
                mode='lines',
                showlegend=False
            ))
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            degree = city_graph.get_degree(node)
            node_text.append(f"Intersection {node}<br>Connections: {degree}")
            
            # Color nodes based on properties
            if highlight_path and node in highlight_path:
                node_colors.append('red')
                node_sizes.append(25)
            elif degree == 1:
                node_colors.append('orange')
                node_sizes.append(20)
            elif degree >= 4:
                node_colors.append('green')
                node_sizes.append(22)
            else:
                node_colors.append('lightblue')
                node_sizes.append(18)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        # Combine all traces
        all_traces = edge_traces + [node_trace]
        
        fig = go.Figure(data=all_traces,
                       layout=go.Layout(
                           title='Weighted City Road Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    @staticmethod
    def create_components_visualization(city_graph: CityGraph) -> go.Figure:
        """Create visualization showing connected components"""
        if not city_graph.nodes:
            fig = go.Figure()
            fig.update_layout(
                title='Connected Components',
                xaxis_title='',
                yaxis_title='',
                annotations=[dict(text="No intersections yet!", x=0.5, y=0.5, showarrow=False)]
            )
            return fig
        
        from ..core.algorithms import GraphAlgorithms
        components = GraphAlgorithms.get_components(city_graph)
        
        if len(components) == 1:
            # Single component - show regular network
            return NetworkPlotter.create_network_graph(city_graph)
        
        # Multiple components - create separate subgraphs
        fig = go.Figure()
        
        # Color palette for components
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        for i, component in enumerate(components):
            # Create subgraph for this component
            subgraph = {node: city_graph.adjacency_list[node] for node in component}
            
            # Create NetworkX graph for layout
            G = nx.Graph()
            for node in component:
                G.add_node(node)
                for neighbor in subgraph[node]:
                    if neighbor in component:
                        G.add_edge(node, neighbor)
            
            if G.nodes():
                pos = nx.spring_layout(G, k=1, iterations=50)
                
                # Add edges
                edge_x = []
                edge_y = []
                for edge in G.edges():
                    x0, y0 = pos[edge[0]]
                    x1, y1 = pos[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                
                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=2, color=colors[i % len(colors)]),
                    hoverinfo='none',
                    mode='lines',
                    showlegend=False
                )
                fig.add_trace(edge_trace)
                
                # Add nodes
                node_x = []
                node_y = []
                node_text = []
                for node in G.nodes():
                    x, y = pos[node]
                    node_x.append(x)
                    node_y.append(y)
                    node_text.append(f"Component {i+1}: {node}")
                
                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    hoverinfo='text',
                    text=node_text,
                    textposition="middle center",
                    marker=dict(
                        size=20,
                        color=colors[i % len(colors)],
                        line=dict(width=2, color='white')
                    ),
                    showlegend=False
                )
                fig.add_trace(node_trace)
        
        fig.update_layout(
            title=f'Connected Components ({len(components)} components)',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        return fig 