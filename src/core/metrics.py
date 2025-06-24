"""
Network metrics and statistics for city road network analysis.
Provides comprehensive network analysis and statistics calculation.
"""

from typing import Dict, List, Set
from .graph import CityGraph
from .algorithms import DijkstraAlgorithm, ConnectivityAlgorithm

class NetworkMetrics:
    """Network analysis and statistics for city road networks"""
    
    @staticmethod
    def get_network_stats(city_graph: CityGraph) -> Dict:
        """Get comprehensive network statistics"""
        if not city_graph.nodes:
            return {
                'total_nodes': 0,
                'total_edges': 0,
                'density': 0.0,
                'avg_degree': 0.0,
                'dead_ends': 0,
                'components': 0,
                'is_connected': True,
                'has_cycles': False,
                'avg_distance': 0.0,
                'avg_time': 0.0
            }
        
        # Basic counts
        total_nodes = len(city_graph.nodes)
        total_edges = sum(len(neighbors) for neighbors in city_graph.adjacency_list.values()) // 2
        
        # Calculate density (actual edges / possible edges)
        max_possible_edges = total_nodes * (total_nodes - 1) // 2
        density = total_edges / max_possible_edges if max_possible_edges > 0 else 0.0
        
        # Average degree
        total_degree = sum(city_graph.get_degree(node) for node in city_graph.nodes)
        avg_degree = total_degree / total_nodes if total_nodes > 0 else 0.0
        
        # Dead ends
        dead_ends = len(ConnectivityAlgorithm.find_dead_ends(city_graph))
        
        # Components
        components = ConnectivityAlgorithm.get_components(city_graph)
        num_components = len(components)
        
        # Connectivity
        is_connected = ConnectivityAlgorithm.is_connected(city_graph)
        
        # Cycles
        has_cycles = ConnectivityAlgorithm.has_cycle(city_graph)
        
        # Average edge metrics
        avg_distance = NetworkMetrics._calculate_avg_edge_metric(city_graph, 'distance')
        avg_time = NetworkMetrics._calculate_avg_edge_metric(city_graph, 'time')
        
        return {
            'total_nodes': total_nodes,
            'total_edges': total_edges,
            'density': round(density, 4),
            'avg_degree': round(avg_degree, 2),
            'dead_ends': dead_ends,
            'components': num_components,
            'is_connected': is_connected,
            'has_cycles': has_cycles,
            'avg_distance': round(avg_distance, 2),
            'avg_time': round(avg_time, 4),
            'component_details': components
        }
    
    @staticmethod
    def _calculate_avg_edge_metric(city_graph: CityGraph, metric_type: str) -> float:
        """Calculate average edge metric (distance or time)"""
        if not city_graph.edge_weights:
            return 0.0
        
        total_metric = 0.0
        edge_count = 0
        
        for (node1, node2), weight in city_graph.edge_weights.items():
            if node1 < node2:  # Count each edge only once
                if metric_type == 'time':
                    total_metric += city_graph.get_edge_time(node1, node2)
                else:
                    total_metric += weight
                edge_count += 1
        
        return total_metric / edge_count if edge_count > 0 else 0.0
    
    @staticmethod
    def get_degree_distribution(city_graph: CityGraph) -> Dict[int, int]:
        """Get distribution of node degrees"""
        degree_counts = {}
        for node in city_graph.nodes:
            degree = city_graph.get_degree(node)
            degree_counts[degree] = degree_counts.get(degree, 0) + 1
        return degree_counts
    
    @staticmethod
    def get_centrality_metrics(city_graph: CityGraph) -> Dict[str, Dict[str, float]]:
        """Calculate centrality metrics for nodes"""
        if not city_graph.nodes:
            return {}
        
        # Degree centrality
        degree_centrality = {}
        max_degree = max(city_graph.get_degree(node) for node in city_graph.nodes)
        
        for node in city_graph.nodes:
            degree = city_graph.get_degree(node)
            degree_centrality[node] = degree / max_degree if max_degree > 0 else 0.0
        
        # Betweenness centrality (simplified)
        betweenness_centrality = NetworkMetrics._calculate_betweenness_centrality(city_graph)
        
        # Closeness centrality (simplified)
        closeness_centrality = NetworkMetrics._calculate_closeness_centrality(city_graph)
        
        return {
            'degree': degree_centrality,
            'betweenness': betweenness_centrality,
            'closeness': closeness_centrality
        }
    
    @staticmethod
    def _calculate_betweenness_centrality(city_graph: CityGraph) -> Dict[str, float]:
        """Calculate betweenness centrality for all nodes"""
        betweenness = {node: 0.0 for node in city_graph.nodes}
        
        # For each pair of nodes, find shortest paths
        nodes_list = list(city_graph.nodes)
        for i, start in enumerate(nodes_list):
            for end in nodes_list[i+1:]:
                path, _ = DijkstraAlgorithm.find_shortest_path(city_graph, start, end)
                if path and len(path) > 2:
                    # Count intermediate nodes
                    for node in path[1:-1]:
                        betweenness[node] += 1.0
        
        # Normalize
        total_pairs = len(nodes_list) * (len(nodes_list) - 1) // 2
        if total_pairs > 0:
            for node in betweenness:
                betweenness[node] /= total_pairs
        
        return betweenness
    
    @staticmethod
    def _calculate_closeness_centrality(city_graph: CityGraph) -> Dict[str, float]:
        """Calculate closeness centrality for all nodes"""
        closeness = {}
        
        for node in city_graph.nodes:
            total_distance = 0.0
            reachable_nodes = 0
            
            for other_node in city_graph.nodes:
                if other_node != node:
                    _, distance = DijkstraAlgorithm.find_shortest_path(city_graph, node, other_node)
                    if distance != float('inf'):
                        total_distance += distance
                        reachable_nodes += 1
            
            if reachable_nodes > 0:
                closeness[node] = reachable_nodes / total_distance
            else:
                closeness[node] = 0.0
        
        return closeness
    
    @staticmethod
    def get_network_efficiency(city_graph: CityGraph) -> Dict[str, float]:
        """Calculate network efficiency metrics"""
        if not city_graph.nodes or len(city_graph.nodes) < 2:
            return {
                'global_efficiency': 0.0,
                'local_efficiency': 0.0,
                'connectivity_score': 0.0
            }
        
        # Global efficiency (average inverse shortest path length)
        total_inverse_distance = 0.0
        total_pairs = 0
        
        nodes_list = list(city_graph.nodes)
        for i, start in enumerate(nodes_list):
            for end in nodes_list[i+1:]:
                _, distance = DijkstraAlgorithm.find_shortest_path(city_graph, start, end)
                if distance != float('inf'):
                    total_inverse_distance += 1.0 / distance
                total_pairs += 1
        
        global_efficiency = total_inverse_distance / total_pairs if total_pairs > 0 else 0.0
        
        # Connectivity score (percentage of reachable pairs)
        reachable_pairs = 0
        for i, start in enumerate(nodes_list):
            for end in nodes_list[i+1:]:
                path, _ = DijkstraAlgorithm.find_shortest_path(city_graph, start, end)
                if path:
                    reachable_pairs += 1
        
        connectivity_score = reachable_pairs / total_pairs if total_pairs > 0 else 0.0
        
        # Local efficiency (simplified - average clustering coefficient)
        local_efficiency = NetworkMetrics._calculate_local_efficiency(city_graph)
        
        return {
            'global_efficiency': round(global_efficiency, 4),
            'local_efficiency': round(local_efficiency, 4),
            'connectivity_score': round(connectivity_score, 4)
        }
    
    @staticmethod
    def _calculate_local_efficiency(city_graph: CityGraph) -> float:
        """Calculate local efficiency (simplified clustering coefficient)"""
        if not city_graph.nodes:
            return 0.0
        
        total_clustering = 0.0
        valid_nodes = 0
        
        for node in city_graph.nodes:
            neighbors = city_graph.adjacency_list.get(node, [])
            if len(neighbors) >= 2:
                # Count connections between neighbors
                neighbor_connections = 0
                for i, n1 in enumerate(neighbors):
                    for n2 in neighbors[i+1:]:
                        if n2 in city_graph.adjacency_list.get(n1, []):
                            neighbor_connections += 1
                
                max_possible = len(neighbors) * (len(neighbors) - 1) // 2
                if max_possible > 0:
                    total_clustering += neighbor_connections / max_possible
                    valid_nodes += 1
        
        return total_clustering / valid_nodes if valid_nodes > 0 else 0.0 