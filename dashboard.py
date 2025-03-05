import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__, use_pages=True)

# Define the navigation bar style
nav_style = {
    'display': 'flex',
    'justifyContent': 'space-between',
    'alignItems': 'center',
    'padding': '1rem',
    'backgroundColor': '#EDF5FF',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    'padding': '20px 40px'
}

# Define the logo style
logo_style = {
    'height': '45px',
    'width': 'auto'
}

button_container_style = {
    'display': 'flex',
    'gap': '1rem'
}

# Define the button style
button_style = {
    'padding': '0.5rem 1rem',
    'backgroundColor': '#f9943b',
    'color': 'white',
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'fontSize': '16px'
}

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    # Navigation Bar
    html.Nav([
        # Logo
        html.Img(src='assets/logo.png', style=logo_style),
        # Buttons Container
        html.Div([
            dcc.Link(html.Button('Analysis', style=button_style), href='/'),
            dcc.Link(html.Button('Prediction', style=button_style), href='/prediction')
        ], style=button_container_style)
    ], style=nav_style),
    
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
