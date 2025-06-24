# 🏙️ City Connectivity Analyzer

An interactive web application that models a city's road network as a graph and allows users to analyze connectivity, find paths, detect cycles, and identify dead ends using fundamental graph algorithms.

## 🚀 Features

### Core Functionality
- **Interactive Graph Building**: Add/remove intersections (nodes) and roads (edges)
- **Network Visualization**: Beautiful interactive network graphs
- **Connectivity Analysis**: Check if the city is fully connected
- **Path Finding**: Find shortest paths between any two intersections
- **Cycle Detection**: Identify cycles in the road network
- **Dead End Detection**: Find intersections with only one connection

### Graph Algorithms Implemented
- **BFS (Breadth-First Search)**: For shortest path finding
- **DFS (Depth-First Search)**: For connectivity checking and cycle detection
- **Degree Analysis**: For dead end detection
- **Component Analysis**: For identifying disconnected parts

### Visualization Features
- **Interactive Network Graphs**: Drag, zoom, and explore the network
- **Color-Coded Nodes**: Different colors for different intersection types
- **Path Highlighting**: Visualize routes between intersections
- **Component Visualization**: Show disconnected parts with different colors
- **Statistics Charts**: Bar charts and metrics for network analysis

## 🏗️ Project Structure

```
City-Connectivity-Analyzer/
├── app.py                  # Streamlit frontend application (entry point)
├── requirements.txt        # Python dependencies
├── setup.py                # Project setup
├── README.md               # Project documentation
└── src/
    ├── core/
    │   ├── graph.py        # Core graph class and operations
    │   ├── metrics.py      # Graph metrics and analysis
    │   └── algorithms/     # Graph algorithms (dijkstra, kruskal, connectivity)
    ├── ui/
    │   ├── components/     # UI components (sidebar, metrics cards)
    │   └── pages/          # Streamlit pages (network view, analysis, etc.)
    ├── utils/
    │   └── data_loader.py  # Data loading utilities
    └── visualization/
        ├── charts.py       # Chart visualizations
        └── network_plots.py# Network graph visualizations
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vivek-anand-singh/City-Connectivity-Analyzer.git
   cd City-Connectivity-Analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage

### Getting Started

1. **Add Intersections**: Use the sidebar to add intersections (nodes) like A, B, C, etc.
2. **Connect Roads**: Add roads (edges) between intersections
3. **Analyze Network**: Use the tabs to explore different aspects of your network
4. **Load Sample Data**: Click "Load Sample City" to see a pre-built example

### Example Workflow

**Building a Simple City**:
1. Add intersections: A, B, C, D
2. Connect roads: A-B, B-C, C-D, D-A
3. Check connectivity: Should be fully connected
4. Find path: A to C (should be A → B → C)
5. Detect cycles: Should find the cycle A → B → C → D → A

## 🧮 Algorithms Explained

### Connectivity Check (DFS)
- **Purpose**: Determine if all intersections are reachable from each other
- **Algorithm**: Depth-First Search from any starting point
- **Result**: "Connected" if all nodes are visited, "Not Connected" otherwise

### Path Finding (BFS)
- **Purpose**: Find shortest path between two intersections
- **Algorithm**: Breadth-First Search with path tracking
- **Result**: List of intersections forming the shortest route

### Cycle Detection (DFS with Parent Tracking)
- **Purpose**: Identify if the network contains cycles
- **Algorithm**: DFS with parent node tracking to detect back edges
- **Result**: "Has Cycles" or "No Cycles"

### Dead End Detection (Degree Analysis)
- **Purpose**: Find intersections with only one connection
- **Algorithm**: Count connections (degree) for each node
- **Result**: List of nodes with degree = 1

### Component Analysis (DFS)
- **Purpose**: Identify disconnected parts of the network
- **Algorithm**: Multiple DFS runs to find all connected components
- **Result**: Number and composition of connected components

## 📊 Key Metrics

The application tracks several important network properties:

- **Total Intersections**: Number of nodes in the network
- **Total Roads**: Number of edges in the network
- **Network Density**: Ratio of actual edges to possible edges
- **Average Connections**: Average degree of all intersections
- **Dead Ends**: Number of intersections with only one connection
- **Connected Components**: Number of disconnected parts
- **Connectivity Status**: Whether the network is fully connected
- **Cycle Status**: Whether the network contains cycles

## 🎨 UI Features

### Modern Interface
- **Responsive Design**: Works on desktop and mobile
- **Interactive Charts**: Plotly-based visualizations
- **Real-time Updates**: Immediate feedback on network changes
- **Tabbed Interface**: Organized sections for different functions

### Visual Elements
- **Color Coding**: 
  - 🔵 Light Blue: Regular intersections
  - 🟢 Green: Major intersections (4+ connections)
  - 🟠 Orange: Dead ends (1 connection)
  - 🔴 Red: Path nodes (when viewing routes)
- **Network Graphs**: Interactive road network visualization
- **Statistics Cards**: Clear display of network metrics
- **Status Indicators**: Visual feedback for connectivity and cycles

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **NetworkX**: Graph algorithms and analysis
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

### Data Structures
- **Adjacency List**: Main graph representation
- **Graph Class**: Core graph operations and algorithms (see `src/core/graph.py`)
- **NetworkX Integration**: For advanced graph analysis

### Performance
- **Efficient Algorithms**: Optimized for networks up to 100+ intersections
- **Real-time Processing**: Immediate calculation of all metrics
- **Memory Efficient**: Minimal memory footprint for typical use cases

## 🚀 Advanced Features

### Multiple Analysis Views
1. **Network View**: Visual representation of the road network
2. **Analysis**: Connectivity, cycles, dead ends, and components
3. **Path Finder**: Route planning between intersections
4. **Statistics**: Comprehensive network metrics
5. **Adjacency List**: Raw graph structure display

### Interactive Controls
- **Add/Remove Nodes**: Dynamic intersection management
- **Add/Remove Edges**: Dynamic road network building
- **Sample Data**: Pre-built examples for demonstration
- **Clear All**: Reset the entire network

### Comprehensive Analytics
- **Network Statistics**: Detailed metrics and properties
- **Degree Distribution**: Analysis of connection patterns
- **Component Visualization**: Visual representation of disconnected parts
- **Path Visualization**: Highlighted routes between intersections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Installation Problems**: Ensure you have Python 3.8+ installed
2. **Display Issues**: Check that Plotly is properly configured
3. **Performance**: For large networks (>50 intersections), consider using the sample data first

### Getting Help

- Check the documentation in each module
- Review the algorithm implementations in `src/core/graph.py` and `src/core/algorithms/`
- Examine the visualization utilities in `src/visualization/`

## 🎯 Educational Value

This project is perfect for learning:

- **Graph Theory Fundamentals**: Nodes, edges, connectivity, cycles
- **Graph Algorithms**: BFS, DFS, path finding, component analysis
- **Network Analysis**: Degree distribution, density, connectivity
- **Interactive Visualization**: Network graphs and data visualization
- **Web Development**: Streamlit applications and user interfaces

## 🎯 Future Enhancements

### Planned Features
- **Weighted Edges**: Road distances and travel times
- **Directed Graphs**: One-way streets and traffic flow
- **Advanced Algorithms**: Dijkstra's shortest path, minimum spanning trees
- **Export Options**: Save/load network configurations
- **Mobile Optimization**: Better mobile interface

### Algorithm Improvements
- **Multiple Path Finding**: Show all possible paths
- **Traffic Flow Analysis**: Simulate traffic patterns
- **Network Optimization**: Suggest road improvements
- **Real-time Updates**: Dynamic network modifications

---

**Happy Network Analysis! 🏙️✨** 