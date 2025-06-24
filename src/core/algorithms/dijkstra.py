"""
Dijkstra's algorithm implementation for shortest path finding.
"""

from typing import Dict, List, Set, Optional, Tuple
import heapq
from ..graph import CityGraph

class DijkstraAlgorithm:
    """Implementation of Dijkstra's shortest path algorithm"""
    
    @staticmethod
    def find_shortest_path(city_graph: CityGraph, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        """
        Find shortest path using Dijkstra's algorithm
        Returns: (path, total_distance)
        """
        if start not in city_graph.nodes or end not in city_graph.nodes:
            return None, float('inf')
        
        if start == end:
            return [start], 0.0
        
        # Initialize distances and previous nodes
        distances = {node: float('inf') for node in city_graph.nodes}
        distances[start] = 0.0
        previous = {node: None for node in city_graph.nodes}
        
        # Priority queue: (distance, node)
        pq = [(0.0, start)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # If we reached the end node, we're done
            if current_node == end:
                break
            
            # Check all neighbors
            for neighbor in city_graph.adjacency_list.get(current_node, []):
                if neighbor in visited:
                    continue
                
                # Calculate new distance
                edge_weight = city_graph.get_edge_weight(current_node, neighbor)
                new_distance = current_distance + edge_weight
                
                # If we found a shorter path, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
        
        # Reconstruct path
        if distances[end] == float('inf'):
            return None, float('inf')
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return path, distances[end]
    
    @staticmethod
    def find_all_shortest_paths(city_graph: CityGraph, start: str) -> Dict[str, Tuple[Optional[List[str]], float]]:
        """
        Find shortest paths from start node to all other nodes
        Returns: Dict[node, (path, distance)]
        """
        if start not in city_graph.nodes:
            return {}
        
        # Initialize distances and previous nodes
        distances = {node: float('inf') for node in city_graph.nodes}
        distances[start] = 0.0
        previous = {node: None for node in city_graph.nodes}
        
        # Priority queue: (distance, node)
        pq = [(0.0, start)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            # Check all neighbors
            for neighbor in city_graph.adjacency_list.get(current_node, []):
                if neighbor in visited:
                    continue
                
                # Calculate new distance
                edge_weight = city_graph.get_edge_weight(current_node, neighbor)
                new_distance = current_distance + edge_weight
                
                # If we found a shorter path, update it
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
        
        # Reconstruct all paths
        paths = {}
        for node in city_graph.nodes:
            if node == start:
                paths[node] = ([start], 0.0)
            elif distances[node] == float('inf'):
                paths[node] = (None, float('inf'))
            else:
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = previous[current]
                path.reverse()
                paths[node] = (path, distances[node])
        
        return paths 