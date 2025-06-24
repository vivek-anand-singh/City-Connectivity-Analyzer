"""
Algorithms package for city road network analysis.
"""

from .dijkstra import DijkstraAlgorithm
from .kruskal import KruskalAlgorithm
from .connectivity import ConnectivityAlgorithm

# Legacy compatibility - import all algorithms into a single class
class GraphAlgorithms:
    """Legacy class that combines all algorithms for backward compatibility"""
    
    @staticmethod
    def dijkstra_shortest_path(city_graph, start: str, end: str):
        """Find shortest path using Dijkstra's algorithm"""
        return DijkstraAlgorithm.find_shortest_path(city_graph, start, end)
    
    @staticmethod
    def kruskal_mst(city_graph):
        """Find Minimum Spanning Tree using Kruskal's algorithm"""
        return KruskalAlgorithm.find_mst(city_graph)
    
    @staticmethod
    def is_connected(city_graph):
        """Check if the graph is connected"""
        return ConnectivityAlgorithm.is_connected(city_graph)
    
    @staticmethod
    def find_path(city_graph, start: str, end: str):
        """Find any path between two nodes"""
        return ConnectivityAlgorithm.find_path(city_graph, start, end)
    
    @staticmethod
    def has_cycle(city_graph):
        """Detect cycles in the graph"""
        return ConnectivityAlgorithm.has_cycle(city_graph)
    
    @staticmethod
    def find_dead_ends(city_graph):
        """Find nodes with degree 1 (dead ends)"""
        return ConnectivityAlgorithm.find_dead_ends(city_graph)
    
    @staticmethod
    def get_components(city_graph):
        """Find all connected components"""
        return ConnectivityAlgorithm.get_components(city_graph)
    
    @staticmethod
    def _dfs(city_graph, node: str, visited: set):
        """DFS helper function"""
        return ConnectivityAlgorithm._dfs(city_graph, node, visited)
    
    @staticmethod
    def _dfs_cycle_detection(city_graph, node: str, visited: set, parent: dict, parent_node):
        """DFS helper for cycle detection"""
        return ConnectivityAlgorithm._dfs_cycle_detection(city_graph, node, visited, parent, parent_node)
    
    @staticmethod
    def _dfs_component(city_graph, node: str, visited: set, component: set):
        """DFS helper for component detection"""
        return ConnectivityAlgorithm._dfs_component(city_graph, node, visited, component)

__all__ = [
    'DijkstraAlgorithm',
    'KruskalAlgorithm', 
    'ConnectivityAlgorithm',
    'GraphAlgorithms'
] 