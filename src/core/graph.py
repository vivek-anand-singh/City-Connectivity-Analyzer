"""
Core graph data structure for city road networks.
Handles basic graph operations like adding/removing nodes and edges.
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

class CityGraph:
    """Represents a city's road network as a graph"""
    
    def __init__(self, metric_type="distance"):
        self.adjacency_list: Dict[str, List[str]] = {}
        self.nodes: Set[str] = set()
        self.edge_weights: Dict[Tuple[str, str], float] = {}  # Store edge weights
        self.metric_type = metric_type  # "distance" or "time"
        self.speed_limits: Dict[Tuple[str, str], float] = {}  # Store speed limits for time calculation
    
    def add_node(self, node: str) -> bool:
        """Add a node (intersection) to the graph"""
        if node not in self.nodes:
            self.nodes.add(node)
            self.adjacency_list[node] = []
            return True
        return False
    
    def remove_node(self, node: str) -> bool:
        """Remove a node and all its connections"""
        if node in self.nodes:
            # Remove all edges connected to this node
            for neighbor in self.adjacency_list[node]:
                if neighbor in self.adjacency_list:
                    self.adjacency_list[neighbor].remove(node)
                # Remove edge weights
                edge1, edge2 = (node, neighbor), (neighbor, node)
                self.edge_weights.pop(edge1, None)
                self.edge_weights.pop(edge2, None)
            
            # Remove the node
            self.nodes.remove(node)
            del self.adjacency_list[node]
            return True
        return False
    
    def add_edge(self, node1: str, node2: str, weight: float = 1.0, speed_limit: float = 30.0) -> bool:
        """Add an edge (road) between two nodes with optional weight and speed limit"""
        if node1 not in self.nodes or node2 not in self.nodes:
            return False
        
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)
        
        # Store edge weight (both directions for undirected graph)
        self.edge_weights[(node1, node2)] = weight
        self.edge_weights[(node2, node1)] = weight
        
        # Store speed limit (both directions)
        self.speed_limits[(node1, node2)] = speed_limit
        self.speed_limits[(node2, node1)] = speed_limit
        return True
    
    def remove_edge(self, node1: str, node2: str) -> bool:
        """Remove an edge between two nodes"""
        if node1 in self.adjacency_list and node2 in self.adjacency_list[node1]:
            self.adjacency_list[node1].remove(node2)
        if node2 in self.adjacency_list and node1 in self.adjacency_list[node2]:
            self.adjacency_list[node2].remove(node1)
        
        # Remove edge weights
        edge1, edge2 = (node1, node2), (node2, node1)
        self.edge_weights.pop(edge1, None)
        self.edge_weights.pop(edge2, None)
        return True
    
    def get_edge_weight(self, node1: str, node2: str) -> float:
        """Get the weight of an edge between two nodes based on current metric type"""
        base_weight = self.edge_weights.get((node1, node2), 1.0)
        
        if self.metric_type == "time":
            # Convert distance to time using speed limit
            speed_limit = self.speed_limits.get((node1, node2), 30.0)  # Default 30 km/h
            return base_weight / speed_limit  # Time = Distance / Speed (in hours)
        else:
            # Return distance as is
            return base_weight
    
    def get_edge_distance(self, node1: str, node2: str) -> float:
        """Get the distance of an edge (regardless of metric type)"""
        return self.edge_weights.get((node1, node2), 1.0)
    
    def get_edge_time(self, node1: str, node2: str) -> float:
        """Get the travel time of an edge (regardless of metric type)"""
        distance = self.edge_weights.get((node1, node2), 1.0)
        speed_limit = self.speed_limits.get((node1, node2), 30.0)
        return distance / speed_limit
    
    def get_edge_speed_limit(self, node1: str, node2: str) -> float:
        """Get the speed limit of an edge"""
        return self.speed_limits.get((node1, node2), 30.0)
    
    def get_degree(self, node: str) -> int:
        """Get the degree (number of connections) of a node"""
        return len(self.adjacency_list.get(node, []))
    
    def get_all_degrees(self) -> Dict[str, int]:
        """Get degrees of all nodes"""
        return {node: self.get_degree(node) for node in self.nodes}
    
    def clear(self):
        """Clear all data from the graph"""
        self.adjacency_list.clear()
        self.nodes.clear()
        self.edge_weights.clear()
        self.speed_limits.clear()
    
    def set_metric_type(self, metric_type: str):
        """Set the metric type for weight calculations"""
        self.metric_type = metric_type
    
    def get_metric_type(self) -> str:
        """Get the current metric type"""
        return self.metric_type
    
    def to_networkx(self):
        """Convert to NetworkX graph for advanced operations"""
        import networkx as nx
        G = nx.Graph()
        
        # Add nodes
        for node in self.nodes:
            G.add_node(node)
        
        # Add edges with weights
        for node1 in self.nodes:
            for node2 in self.adjacency_list.get(node1, []):
                if node1 < node2:  # Avoid duplicates in undirected graph
                    weight = self.get_edge_weight(node1, node2)
                    G.add_edge(node1, node2, weight=weight)
        
        return G
    
    def get_adjacency_list_str(self) -> str:
        """Get a formatted string representation of the adjacency list"""
        if not self.nodes:
            return "Empty graph"
        
        result = []
        for node in sorted(self.nodes):
            neighbors = sorted(self.adjacency_list.get(node, []))
            if neighbors:
                neighbor_str = ", ".join(neighbors)
                result.append(f"{node}: {neighbor_str}")
            else:
                result.append(f"{node}: (no connections)")
        
        return "\n".join(result) 