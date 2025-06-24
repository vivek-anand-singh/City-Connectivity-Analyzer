"""
Kruskal's algorithm implementation for minimum spanning tree.
"""

from typing import Dict, List, Set, Optional, Tuple
from ..graph import CityGraph

class KruskalAlgorithm:
    """Implementation of Kruskal's minimum spanning tree algorithm"""
    
    @staticmethod
    def find_mst(city_graph: CityGraph) -> Tuple[List[Tuple[str, str]], float]:
        """
        Find Minimum Spanning Tree using Kruskal's algorithm
        Returns: (edges_in_mst, total_weight)
        """
        if not city_graph.nodes:
            return [], 0.0
        
        # Get all edges with weights
        edges = []
        for node1 in city_graph.nodes:
            for node2 in city_graph.adjacency_list.get(node1, []):
                if node1 < node2:  # Avoid duplicates in undirected graph
                    weight = city_graph.get_edge_weight(node1, node2)
                    edges.append((weight, node1, node2))
        
        # Sort edges by weight
        edges.sort()
        
        # Union-Find data structure for cycle detection
        parent = {node: node for node in city_graph.nodes}
        rank = {node: 0 for node in city_graph.nodes}
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]
        
        def union(node1, node2):
            root1, root2 = find(node1), find(node2)
            if root1 == root2:
                return False
            
            if rank[root1] < rank[root2]:
                parent[root1] = root2
            elif rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root2] = root1
                rank[root1] += 1
            return True
        
        # Build MST
        mst_edges = []
        total_weight = 0.0
        
        for weight, node1, node2 in edges:
            if union(node1, node2):
                mst_edges.append((node1, node2))
                total_weight += weight
        
        return mst_edges, total_weight
    
    @staticmethod
    def find_mst_with_details(city_graph: CityGraph) -> Dict:
        """
        Find MST with detailed information
        Returns: Dict with edges, weight, and statistics
        """
        mst_edges, total_weight = KruskalAlgorithm.find_mst(city_graph)
        
        # Calculate statistics
        total_edges = sum(len(neighbors) for neighbors in city_graph.adjacency_list.values()) // 2
        mst_edges_count = len(mst_edges)
        efficiency = mst_edges_count / total_edges if total_edges > 0 else 0.0
        
        # Get edge details
        edge_details = []
        for node1, node2 in mst_edges:
            weight = city_graph.get_edge_weight(node1, node2)
            distance = city_graph.get_edge_distance(node1, node2)
            speed = city_graph.get_edge_speed_limit(node1, node2)
            time = city_graph.get_edge_time(node1, node2)
            
            edge_details.append({
                'from': node1,
                'to': node2,
                'weight': weight,
                'distance': distance,
                'speed': speed,
                'time': time
            })
        
        return {
            'edges': mst_edges,
            'total_weight': total_weight,
            'edge_count': mst_edges_count,
            'efficiency': efficiency,
            'edge_details': edge_details
        }
    
    @staticmethod
    def find_mst_by_component(city_graph: CityGraph) -> Dict[str, List[Tuple[str, str]]]:
        """
        Find MST for each connected component separately
        Returns: Dict[component_id, mst_edges]
        """
        from .connectivity import ConnectivityAlgorithm
        
        components = ConnectivityAlgorithm.get_components(city_graph)
        mst_by_component = {}
        
        for i, component in enumerate(components):
            # Create subgraph for this component
            subgraph = CityGraph(city_graph.get_metric_type())
            
            # Add nodes
            for node in component:
                subgraph.add_node(node)
            
            # Add edges within component
            for node1 in component:
                for node2 in city_graph.adjacency_list.get(node1, []):
                    if node2 in component and node1 < node2:
                        weight = city_graph.get_edge_distance(node1, node2)
                        speed = city_graph.get_edge_speed_limit(node1, node2)
                        subgraph.add_edge(node1, node2, weight, speed)
            
            # Find MST for this component
            mst_edges, _ = KruskalAlgorithm.find_mst(subgraph)
            mst_by_component[f"component_{i+1}"] = mst_edges
        
        return mst_by_component 