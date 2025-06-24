"""
Data loading utilities for city road networks.
Handles sample data creation and loading.
"""

from typing import Dict, List, Tuple
from ..core.graph import CityGraph

class DataLoader:
    """Utility class for loading sample city data"""
    
    @staticmethod
    def load_sample_data(city_graph: CityGraph):
        """Load sample city data into the graph"""
        # Clear existing data
        city_graph.clear()
        
        # Sample city intersections
        intersections = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        
        # Add intersections
        for intersection in intersections:
            city_graph.add_node(intersection)
        
        # Sample roads with distances and speed limits
        roads = [
            ('A', 'B', 2.5, 40),  # A to B: 2.5km, 40km/h
            ('B', 'C', 3.0, 35),  # B to C: 3.0km, 35km/h
            ('C', 'D', 2.0, 50),  # C to D: 2.0km, 50km/h
            ('D', 'A', 4.0, 30),  # D to A: 4.0km, 30km/h
            ('A', 'E', 1.5, 45),  # A to E: 1.5km, 45km/h
            ('E', 'F', 2.8, 40),  # E to F: 2.8km, 40km/h
            ('F', 'G', 3.2, 35),  # F to G: 3.2km, 35km/h
            ('G', 'H', 1.8, 50),  # G to H: 1.8km, 50km/h
            ('H', 'C', 2.2, 40),  # H to C: 2.2km, 40km/h
            ('B', 'F', 4.5, 30),  # B to F: 4.5km, 30km/h
            ('D', 'G', 3.8, 35),  # D to G: 3.8km, 35km/h
        ]
        
        # Add roads
        for start, end, distance, speed in roads:
            city_graph.add_edge(start, end, distance, speed)
    
    @staticmethod
    def load_small_sample(city_graph: CityGraph):
        """Load a small sample city for quick testing"""
        city_graph.clear()
        
        # Simple 4-node city
        for node in ['A', 'B', 'C', 'D']:
            city_graph.add_node(node)
        
        # Create a simple cycle
        roads = [
            ('A', 'B', 2.0, 40),
            ('B', 'C', 3.0, 35),
            ('C', 'D', 2.5, 45),
            ('D', 'A', 3.5, 30),
        ]
        
        for start, end, distance, speed in roads:
            city_graph.add_edge(start, end, distance, speed)
    
    @staticmethod
    def load_complex_sample(city_graph: CityGraph):
        """Load a more complex city with multiple components"""
        city_graph.clear()
        
        # Larger city with 12 intersections
        intersections = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        
        for intersection in intersections:
            city_graph.add_node(intersection)
        
        # Complex road network
        roads = [
            # Main downtown area (A-D)
            ('A', 'B', 1.5, 30),
            ('B', 'C', 2.0, 35),
            ('C', 'D', 1.8, 40),
            ('D', 'A', 2.2, 25),
            ('A', 'C', 2.5, 30),
            
            # Suburban area (E-H)
            ('E', 'F', 3.0, 50),
            ('F', 'G', 2.5, 45),
            ('G', 'H', 3.2, 40),
            ('H', 'E', 2.8, 55),
            ('E', 'G', 4.0, 35),
            
            # Industrial area (I-L)
            ('I', 'J', 4.5, 60),
            ('J', 'K', 3.8, 55),
            ('K', 'L', 4.2, 50),
            ('L', 'I', 3.5, 65),
            
            # Connecting roads
            ('B', 'F', 5.0, 40),
            ('D', 'H', 4.8, 35),
            ('C', 'I', 6.0, 45),
            ('G', 'K', 5.5, 40),
        ]
        
        for start, end, distance, speed in roads:
            city_graph.add_edge(start, end, distance, speed)
    
    @staticmethod
    def load_disconnected_sample(city_graph: CityGraph):
        """Load a city with disconnected components"""
        city_graph.clear()
        
        # Two separate areas
        for node in ['A', 'B', 'C', 'D', 'E', 'F']:
            city_graph.add_node(node)
        
        # First component: A-B-C
        roads = [
            ('A', 'B', 2.0, 40),
            ('B', 'C', 3.0, 35),
            
            # Second component: D-E-F
            ('D', 'E', 2.5, 45),
            ('E', 'F', 2.8, 40),
        ]
        
        for start, end, distance, speed in roads:
            city_graph.add_edge(start, end, distance, speed)
    
    @staticmethod
    def get_sample_cities() -> Dict[str, str]:
        """Get available sample cities"""
        return {
            'small': 'Small 4-node city with cycle',
            'standard': 'Standard 8-node city with good connectivity',
            'complex': 'Complex 12-node city with multiple areas',
            'disconnected': 'City with disconnected components'
        }
    
    @staticmethod
    def load_city_by_name(city_graph: CityGraph, city_name: str):
        """Load a specific sample city by name"""
        if city_name == 'small':
            DataLoader.load_small_sample(city_graph)
        elif city_name == 'standard':
            DataLoader.load_sample_data(city_graph)
        elif city_name == 'complex':
            DataLoader.load_complex_sample(city_graph)
        elif city_name == 'disconnected':
            DataLoader.load_disconnected_sample(city_graph)
        else:
            raise ValueError(f"Unknown city name: {city_name}") 