"""
Web Interface for Stock Scanner
Modern dashboard built with Dash and Plotly
"""
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import logging
import threading
import time

from stock_scanner import StockScanner
import config

logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize the stock scanner
scanner = StockScanner()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Small Cap Stock Scanner"

# Define color scheme
colors = {
    'background': '#0f1419',
    'surface': '#1a1f2e',
    'primary': '#00d4aa',
    'secondary': '#5294cf',
    'success': '#26a69a',
    'warning': '#ffc107',
    'danger': '#ef5350',
    'text': '#ffffff',
    'muted': '#9e9e9e'
}

def create_header():
    """Create the app header"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("🚀 Small Cap Stock Scanner", 
                       className="text-center mb-0",
                       style={'color': colors['primary'], 'fontWeight': 'bold'}),
                html.P("Real-time monitoring of small-cap stocks with short squeeze potential",
                      className="text-center text-muted mb-4")
            ])
        ])
    ], fluid=True, className="py-3", style={'backgroundColor': colors['surface']})

def create_stats_cards():
    """Create statistics cards"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊", className="text-center mb-2"),
                    html.H5("Stocks Analyzed", className="text-center text-muted"),
                    html.H3(id="total-stocks", className="text-center", 
                           style={'color': colors['primary']})
                ])
            ], style={'backgroundColor': colors['surface'], 'border': 'none'})
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🎯", className="text-center mb-2"),
                    html.H5("Top Gainers", className="text-center text-muted"),
                    html.H3(id="top-gainers-count", className="text-center",
                           style={'color': colors['success']})
                ])
            ], style={'backgroundColor': colors['surface'], 'border': 'none'})
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💥", className="text-center mb-2"),
                    html.H5("Squeeze Candidates", className="text-center text-muted"),
                    html.H3(id="squeeze-count", className="text-center",
                           style={'color': colors['warning']})
                ])
            ], style={'backgroundColor': colors['surface'], 'border': 'none'})
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("⏰", className="text-center mb-2"),
                    html.H5("Market Status", className="text-center text-muted"),
                    html.H5(id="market-status", className="text-center")
                ])
            ], style={'backgroundColor': colors['surface'], 'border': 'none'})
        ], md=3)
    ], className="mb-4")

def create_control_panel():
    """Create control panel"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button("🔄 Refresh Data", id="refresh-btn", color="primary", className="me-2"),
                    dbc.Button("💾 Save Results", id="save-btn", color="secondary", className="me-2"),
                    dbc.Button("⚙️ Auto-Scan", id="auto-scan-btn", color="success")
                ], md=8),
                dbc.Col([
                    html.Div(id="last-update", className="text-muted text-end")
                ], md=4)
            ])
        ])
    ], style={'backgroundColor': colors['surface'], 'border': 'none'}, className="mb-4")

def create_data_table(table_id, title, columns):
    """Create a data table component"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5(title, className="mb-0", style={'color': colors['text']})
        ], style={'backgroundColor': colors['surface'], 'border': 'none'}),
        dbc.CardBody([
            dash_table.DataTable(
                id=table_id,
                columns=columns,
                data=[],
                sort_action="native",
                sort_mode="multi",
                page_action="native",
                page_current=0,
                page_size=10,
                style_cell={
                    'backgroundColor': colors['background'],
                    'color': colors['text'],
                    'border': f'1px solid {colors["surface"]}',
                    'textAlign': 'left',
                    'padding': '10px'
                },
                style_header={
                    'backgroundColor': colors['surface'],
                    'color': colors['primary'],
                    'fontWeight': 'bold',
                    'border': f'1px solid {colors["surface"]}'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': colors['surface']
                    }
                ],
                tooltip_data=[],
                tooltip_duration=None
            )
        ], style={'backgroundColor': colors['background']})
    ], style={'backgroundColor': colors['surface'], 'border': 'none'}, className="mb-4")

# Define table columns
gainers_columns = [
    {"name": "Symbol", "id": "symbol", "type": "text"},
    {"name": "Company", "id": "company_name", "type": "text"},
    {"name": "Price", "id": "current_price", "type": "numeric", "format": {"specifier": "$,.2f"}},
    {"name": "Change %", "id": "daily_change", "type": "numeric", "format": {"specifier": ".2f"}},
    {"name": "Volume Ratio", "id": "volume_ratio", "type": "numeric", "format": {"specifier": ".2f"}},
    {"name": "Market Cap", "id": "market_cap", "type": "numeric", "format": {"specifier": "$,.0f"}},
    {"name": "Sector", "id": "sector", "type": "text"}
]

squeeze_columns = [
    {"name": "Symbol", "id": "symbol", "type": "text"},
    {"name": "Squeeze Score", "id": "squeeze_score", "type": "numeric", "format": {"specifier": ".1f"}},
    {"name": "Risk Level", "id": "risk_level", "type": "text"},
    {"name": "Short %", "id": "short_interest", "type": "numeric", "format": {"specifier": ".1f"}},
    {"name": "Days to Cover", "id": "days_to_cover", "type": "numeric", "format": {"specifier": ".1f"}},
    {"name": "Price", "id": "current_price", "type": "numeric", "format": {"specifier": "$,.2f"}},
    {"name": "Change %", "id": "daily_change", "type": "numeric", "format": {"specifier": ".2f"}},
    {"name": "Recommendation", "id": "recommendation", "type": "text"}
]

# App layout
app.layout = dbc.Container([
    create_header(),
    create_stats_cards(),
    create_control_panel(),
    
    # Main content tabs
    dbc.Tabs([
        dbc.Tab(label="📈 Top Gainers", tab_id="gainers-tab"),
        dbc.Tab(label="💥 Short Squeeze", tab_id="squeeze-tab"),
        dbc.Tab(label="🎯 Overall Rankings", tab_id="overall-tab"),
        dbc.Tab(label="📊 Analytics", tab_id="analytics-tab")
    ], id="main-tabs", active_tab="gainers-tab", className="mb-4"),
    
    # Tab content
    html.Div(id="tab-content"),
    
    # Toast notifications
    dbc.Toast(
        id="notification-toast",
        header="Notification",
        is_open=False,
        dismissable=True,
        duration=4000,
        style={"position": "fixed", "top": 20, "right": 20, "width": 350}
    ),
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    ),
    
    # Store for data
    dcc.Store(id='data-store')
    
], fluid=True, style={'backgroundColor': colors['background'], 'minHeight': '100vh'})

# Callbacks
@app.callback(
    [Output('data-store', 'data'),
     Output('notification-toast', 'is_open'),
     Output('notification-toast', 'children'),
     Output('notification-toast', 'header')],
    [Input('refresh-btn', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    prevent_initial_call=False
)
def update_data(refresh_clicks, n_intervals):
    """Update data from scanner"""
    try:
        # Get fresh data
        results = scanner.get_cached_results()
        
        # If no cached data, trigger a scan
        if not results.get('top_gainers') and not results.get('squeeze_candidates'):
            logger.info("No cached data, triggering new scan...")
            results = scanner.scan_stocks()
        
        return results, False, "", ""
        
    except Exception as e:
        logger.error(f"Error updating data: {e}")
        return {}, True, f"Error updating data: {str(e)}", "Error"

@app.callback(
    [Output('total-stocks', 'children'),
     Output('top-gainers-count', 'children'),
     Output('squeeze-count', 'children'),
     Output('market-status', 'children'),
     Output('market-status', 'style'),
     Output('last-update', 'children')],
    [Input('data-store', 'data')]
)
def update_stats(data):
    """Update statistics cards"""
    try:
        if not data:
            return "0", "0", "0", "Unknown", {}, "Never updated"
        
        total_stocks = data.get('total_stocks_analyzed', 0)
        gainers_count = len(data.get('top_gainers', []))
        squeeze_count = len(data.get('squeeze_candidates', []))
        market_open = data.get('market_open', False)
        
        market_status = "🟢 OPEN" if market_open else "🔴 CLOSED"
        market_color = colors['success'] if market_open else colors['danger']
        
        last_update = data.get('last_update', 0)
        if last_update:
            update_time = datetime.fromtimestamp(last_update).strftime("%H:%M:%S")
            last_update_text = f"Last updated: {update_time}"
        else:
            last_update_text = "Never updated"
        
        return (str(total_stocks), str(gainers_count), str(squeeze_count), 
                market_status, {'color': market_color}, last_update_text)
        
    except Exception as e:
        logger.error(f"Error updating stats: {e}")
        return "Error", "Error", "Error", "Error", {}, "Error"

@app.callback(
    Output('tab-content', 'children'),
    [Input('main-tabs', 'active_tab'),
     Input('data-store', 'data')]
)
def render_tab_content(active_tab, data):
    """Render content based on active tab"""
    try:
        if not data:
            return html.Div("Loading data...", className="text-center p-4")
        
        if active_tab == "gainers-tab":
            gainers_data = data.get('top_gainers', [])
            return create_data_table("gainers-table", "🚀 Top Daily Gainers", gainers_columns)
        
        elif active_tab == "squeeze-tab":
            squeeze_data = data.get('squeeze_candidates', [])
            return create_data_table("squeeze-table", "💥 Short Squeeze Candidates", squeeze_columns)
        
        elif active_tab == "overall-tab":
            overall_data = data.get('overall_recommendations', [])
            return create_data_table("overall-table", "🎯 Overall Top Recommendations", gainers_columns)
        
        elif active_tab == "analytics-tab":
            return create_analytics_tab(data)
        
        return html.Div("Select a tab to view data")
        
    except Exception as e:
        logger.error(f"Error rendering tab content: {e}")
        return html.Div(f"Error loading content: {str(e)}")

@app.callback(
    Output('gainers-table', 'data'),
    [Input('data-store', 'data')]
)
def update_gainers_table(data):
    """Update gainers table data"""
    if not data:
        return []
    return data.get('top_gainers', [])

@app.callback(
    Output('squeeze-table', 'data'),
    [Input('data-store', 'data')]
)
def update_squeeze_table(data):
    """Update squeeze table data"""
    if not data:
        return []
    return data.get('squeeze_candidates', [])

@app.callback(
    Output('overall-table', 'data'),
    [Input('data-store', 'data')]
)
def update_overall_table(data):
    """Update overall recommendations table data"""
    if not data:
        return []
    return data.get('overall_recommendations', [])

def create_analytics_tab(data):
    """Create analytics tab with charts"""
    try:
        gainers = data.get('top_gainers', [])
        squeeze_candidates = data.get('squeeze_candidates', [])
        
        if not gainers and not squeeze_candidates:
            return html.Div("No data available for analytics", className="text-center p-4")
        
        # Create sector distribution chart
        if gainers:
            df_gainers = pd.DataFrame(gainers)
            if 'sector' in df_gainers.columns:
                sector_fig = px.pie(
                    df_gainers, 
                    names='sector', 
                    title="Sector Distribution - Top Gainers",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                sector_fig.update_layout(
                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    font_color=colors['text']
                )
            else:
                sector_fig = go.Figure()
        else:
            sector_fig = go.Figure()
        
        # Create performance chart
        if gainers:
            performance_fig = px.bar(
                df_gainers.head(10),
                x='symbol',
                y='daily_change',
                title="Top 10 Gainers Performance",
                color='daily_change',
                color_continuous_scale='Greens'
            )
            performance_fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
            )
        else:
            performance_fig = go.Figure()
        
        return dbc.Row([
            dbc.Col([
                dcc.Graph(figure=sector_fig)
            ], md=6),
            dbc.Col([
                dcc.Graph(figure=performance_fig)
            ], md=6)
        ])
        
    except Exception as e:
        logger.error(f"Error creating analytics tab: {e}")
        return html.Div(f"Error creating analytics: {str(e)}")

def start_background_scanner():
    """Start the background scanner"""
    def scanner_thread():
        time.sleep(5)  # Wait 5 seconds before starting
        scanner.start_automated_scanning()
    
    thread = threading.Thread(target=scanner_thread)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    # Start background scanner
    start_background_scanner()
    
    # Run the app
    app.run_server(
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        debug=config.DEBUG_MODE
    )