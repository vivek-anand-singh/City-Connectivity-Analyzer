"""
Connectivity algorithms for graph analysis.
Includes DFS, BFS, component detection, and cycle detection.
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import deque
from ..graph import CityGraph

class ConnectivityAlgorithm:
    """Implementation of connectivity-related algorithms"""
    
    @staticmethod
    def is_connected(city_graph: CityGraph) -> bool:
        """Check if the graph is connected using DFS"""
        if not city_graph.nodes:
            return True
        
        start_node = next(iter(city_graph.nodes))
        visited = set()
        ConnectivityAlgorithm._dfs(city_graph, start_node, visited)
        
        return len(visited) == len(city_graph.nodes)
    
    @staticmethod
    def _dfs(city_graph: CityGraph, node: str, visited: Set[str]):
        """Depth-First Search helper function"""
        visited.add(node)
        for neighbor in city_graph.adjacency_list.get(node, []):
            if neighbor not in visited:
                ConnectivityAlgorithm._dfs(city_graph, neighbor, visited)
    
    @staticmethod
    def find_path(city_graph: CityGraph, start: str, end: str) -> Optional[List[str]]:
        """Find any path between two nodes using BFS"""
        if start not in city_graph.nodes or end not in city_graph.nodes:
            return None
        
        if start == end:
            return [start]
        
        # BFS with path tracking
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current_node, path = queue.popleft()
            
            for neighbor in city_graph.adjacency_list.get(current_node, []):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    @staticmethod
    def has_cycle(city_graph: CityGraph) -> bool:
        """Detect cycles in the graph using DFS with parent tracking"""
        if not city_graph.nodes:
            return False
        
        visited = set()
        parent = {}
        
        for node in city_graph.nodes:
            if node not in visited:
                if ConnectivityAlgorithm._dfs_cycle_detection(city_graph, node, visited, parent, None):
                    return True
        
        return False
    
    @staticmethod
    def _dfs_cycle_detection(city_graph: CityGraph, node: str, visited: Set[str], 
                           parent: Dict[str, str], parent_node: Optional[str]) -> bool:
        """DFS helper for cycle detection"""
        visited.add(node)
        parent[node] = parent_node
        
        for neighbor in city_graph.adjacency_list.get(node, []):
            if neighbor not in visited:
                if ConnectivityAlgorithm._dfs_cycle_detection(city_graph, neighbor, visited, parent, node):
                    return True
            elif neighbor != parent_node:
                # Back edge found - cycle detected
                return True
        
        return False
    
    @staticmethod
    def get_components(city_graph: CityGraph) -> List[Set[str]]:
        """Find all connected components in the graph"""
        if not city_graph.nodes:
            return []
        
        visited = set()
        components = []
        
        for node in city_graph.nodes:
            if node not in visited:
                component = set()
                ConnectivityAlgorithm._dfs_component(city_graph, node, visited, component)
                components.append(component)
        
        return components
    
    @staticmethod
    def _dfs_component(city_graph: CityGraph, node: str, visited: Set[str], component: Set[str]):
        """DFS helper for component detection"""
        visited.add(node)
        component.add(node)
        
        for neighbor in city_graph.adjacency_list.get(node, []):
            if neighbor not in visited:
                ConnectivityAlgorithm._dfs_component(city_graph, neighbor, visited, component)
    
    @staticmethod
    def find_dead_ends(city_graph: CityGraph) -> List[str]:
        """Find nodes with degree 1 (dead ends)"""
        return [node for node in city_graph.nodes if city_graph.get_degree(node) == 1]
    
    @staticmethod
    def find_articulation_points(city_graph: CityGraph) -> List[str]:
        """Find articulation points (nodes whose removal disconnects the graph)"""
        if not city_graph.nodes or len(city_graph.nodes) <= 2:
            return []
        
        articulation_points = []
        
        for node in city_graph.nodes:
            # Create a copy of the graph without this node
            temp_graph = CityGraph(city_graph.get_metric_type())
            
            # Add all nodes except the current one
            for n in city_graph.nodes:
                if n != node:
                    temp_graph.add_node(n)
            
            # Add all edges except those connected to the current node
            for n1 in city_graph.nodes:
                if n1 != node:
                    for n2 in city_graph.adjacency_list.get(n1, []):
                        if n2 != node and n1 < n2:
                            weight = city_graph.get_edge_distance(n1, n2)
                            speed = city_graph.get_edge_speed_limit(n1, n2)
                            temp_graph.add_edge(n1, n2, weight, speed)
            
            # Check if removing this node increases the number of components
            original_components = len(ConnectivityAlgorithm.get_components(city_graph))
            new_components = len(ConnectivityAlgorithm.get_components(temp_graph))
            
            if new_components > original_components:
                articulation_points.append(node)
        
        return articulation_points
    
    @staticmethod
    def find_bridges(city_graph: CityGraph) -> List[Tuple[str, str]]:
        """Find bridges (edges whose removal disconnects the graph)"""
        if not city_graph.nodes:
            return []
        
        bridges = []
        
        # Get all edges
        edges = []
        for node1 in city_graph.nodes:
            for node2 in city_graph.adjacency_list.get(node1, []):
                if node1 < node2:  # Avoid duplicates
                    edges.append((node1, node2))
        
        # Check each edge
        for edge in edges:
            node1, node2 = edge
            
            # Create a copy of the graph without this edge
            temp_graph = CityGraph(city_graph.get_metric_type())
            
            # Add all nodes
            for node in city_graph.nodes:
                temp_graph.add_node(node)
            
            # Add all edges except the current one
            for n1 in city_graph.nodes:
                for n2 in city_graph.adjacency_list.get(n1, []):
                    if n1 < n2 and (n1, n2) != edge:
                        weight = city_graph.get_edge_distance(n1, n2)
                        speed = city_graph.get_edge_speed_limit(n1, n2)
                        temp_graph.add_edge(n1, n2, weight, speed)
            
            # Check if removing this edge increases the number of components
            original_components = len(ConnectivityAlgorithm.get_components(city_graph))
            new_components = len(ConnectivityAlgorithm.get_components(temp_graph))
            
            if new_components > original_components:
                bridges.append(edge)
        
        return bridges 