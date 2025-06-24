"""
UI styling and CSS for the City Connectivity Analyzer.
Centralizes all styling to maintain consistency.
"""

def get_custom_css() -> str:
    """Get custom CSS styles for the application"""
    return """
    <style>
        /* Main header styling */
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Metric cards */
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .metric-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }
        
        /* Status indicators */
        .status-connected {
            background-color: #d4edda;
            color: #155724;
            padding: 0.5rem;
            border-radius: 0.5rem;
            border: 1px solid #c3e6cb;
            font-weight: bold;
        }
        
        .status-disconnected {
            background-color: #f8d7da;
            color: #721c24;
            padding: 0.5rem;
            border-radius: 0.5rem;
            border: 1px solid #f5c6cb;
            font-weight: bold;
        }
        
        .status-cycle {
            background-color: #fff3cd;
            color: #856404;
            padding: 0.5rem;
            border-radius: 0.5rem;
            border: 1px solid #ffeaa7;
            font-weight: bold;
        }
        
        .status-no-cycle {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 0.5rem;
            border-radius: 0.5rem;
            border: 1px solid #bee5eb;
            font-weight: bold;
        }
        
        /* Path visualization */
        .path-node {
            background-color: #ff6b6b;
            color: white;
            padding: 0.3rem 0.6rem;
            border-radius: 0.3rem;
            font-weight: bold;
            margin: 0.1rem;
            display: inline-block;
        }
        
        .path-arrow {
            color: #ff6b6b;
            font-weight: bold;
            margin: 0 0.5rem;
        }
        
        /* Component visualization */
        .component-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .component-title {
            font-weight: bold;
            color: #495057;
            margin-bottom: 0.5rem;
        }
        
        .component-nodes {
            color: #6c757d;
            font-family: monospace;
        }
        
        /* Sidebar styling */
        .sidebar-section {
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid #e9ecef;
        }
        
        .sidebar-title {
            font-weight: bold;
            color: #495057;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        /* Form styling */
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            font-weight: bold;
            color: #495057;
            margin-bottom: 0.3rem;
        }
        
        /* Button styling */
        .btn-primary {
            background-color: #1f77b4;
            border-color: #1f77b4;
            color: white;
            border-radius: 0.3rem;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        
        .btn-primary:hover {
            background-color: #1565c0;
            border-color: #1565c0;
        }
        
        .btn-success {
            background-color: #28a745;
            border-color: #28a745;
            color: white;
            border-radius: 0.3rem;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        
        .btn-danger {
            background-color: #dc3545;
            border-color: #dc3545;
            color: white;
            border-radius: 0.3rem;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        
        /* Table styling */
        .data-table {
            background-color: white;
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .table-header {
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
            padding: 0.75rem;
        }
        
        .table-row {
            padding: 0.5rem;
            border-bottom: 1px solid #e9ecef;
        }
        
        .table-row:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        /* Chart containers */
        .chart-container {
            background-color: white;
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        /* Info boxes */
        .info-box {
            background-color: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .info-box-title {
            font-weight: bold;
            color: #1976d2;
            margin-bottom: 0.5rem;
        }
        
        /* Warning boxes */
        .warning-box {
            background-color: #fff3e0;
            border: 1px solid #ffcc02;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .warning-box-title {
            font-weight: bold;
            color: #f57c00;
            margin-bottom: 0.5rem;
        }
        
        /* Success boxes */
        .success-box {
            background-color: #e8f5e8;
            border: 1px solid #4caf50;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .success-box-title {
            font-weight: bold;
            color: #2e7d32;
            margin-bottom: 0.5rem;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .metric-card {
                padding: 0.75rem;
            }
            
            .sidebar-section {
                padding: 0.75rem;
            }
        }
        
        /* Animation for loading states */
        .loading {
            opacity: 0.6;
            pointer-events: none;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
    </style>
    """

def get_status_class(status: bool, status_type: str = "connected") -> str:
    """Get CSS class for status indicators"""
    if status_type == "connected":
        return "status-connected" if status else "status-disconnected"
    elif status_type == "cycle":
        return "status-cycle" if status else "status-no-cycle"
    else:
        return "status-connected" if status else "status-disconnected"

def get_metric_card_html(title: str, value: str, unit: str = "") -> str:
    """Generate HTML for a metric card"""
    return f"""
    <div class="metric-card">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.3rem;">{title}</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: #1f77b4;">{value}{unit}</div>
    </div>
    """

def get_info_box_html(title: str, content: str) -> str:
    """Generate HTML for an info box"""
    return f"""
    <div class="info-box">
        <div class="info-box-title">{title}</div>
        <div>{content}</div>
    </div>
    """

def get_warning_box_html(title: str, content: str) -> str:
    """Generate HTML for a warning box"""
    return f"""
    <div class="warning-box">
        <div class="warning-box-title">{title}</div>
        <div>{content}</div>
    </div>
    """

def get_success_box_html(title: str, content: str) -> str:
    """Generate HTML for a success box"""
    return f"""
    <div class="success-box">
        <div class="success-box-title">{title}</div>
        <div>{content}</div>
    </div>
    """ 