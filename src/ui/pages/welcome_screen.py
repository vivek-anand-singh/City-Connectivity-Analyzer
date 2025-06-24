"""
Welcome Screen Page
Renders the welcome screen when no data is present.
"""

import streamlit as st

def render_welcome_screen():
    """Render the welcome screen when no data is present"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 🚀 Welcome to City Connectivity Analyzer!
        
        This app helps you analyze road networks using **graph algorithms**.
        
        **Key Features:**
        - 🗺️ Visual road network representation
        - 🔍 Connectivity and cycle detection
        - 🛣️ Path finding between intersections
        - 🚀 Advanced algorithms (Dijkstra, Kruskal MST)
        - ⏱️ Time vs Distance optimization
        - 📊 Network statistics and analysis
        - 📋 Adjacency list visualization
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Getting Started
        
        1. **Add Intersections**: Use the sidebar to add intersections (nodes)
        2. **Connect Roads**: Add roads (edges) between intersections
        3. **Load Sample Data**: Try the sample cities for quick exploration
        4. **Analyze Network**: Use the tabs to explore different aspects
        
        ### 🧮 Algorithms Available
        
        - **Dijkstra's Algorithm**: Shortest path finding
        - **Kruskal's Algorithm**: Minimum spanning tree
        - **DFS/BFS**: Connectivity and cycle detection
        - **Degree Analysis**: Dead end detection
        - **Component Analysis**: Disconnected parts identification
        """) 