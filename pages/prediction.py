import dash
from dash import html, dcc
import pandas as pd

dash.register_page(__name__)

# Define form container style
form_container_style = {
    'maxWidth': '600px',
    'margin': '2rem auto',
    'padding': '2rem',
    'backgroundColor': 'white',
    'borderRadius': '8px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
}

# Define dropdown style
dropdown_style = {
    'marginBottom': '1.5rem'
}

# Define label style
label_style = {
    'marginBottom': '0.8rem',
    'fontWeight': 'bold',
    'color': '#333'
}

# Load and prepare data
sector_list = ['Agriculture', 'Industry', 'Services']
countries = ['India', 'Pakistan']
years = list(range(2005, 2024))

layout = html.Div([
    html.H1('Unemployment Prediction', style={'textAlign': 'center', 'marginTop': '3rem', 'marginBottom': '2rem', 'color': '#7A695B'}),
    html.Div([
        # Country Dropdown
        html.Div([
            html.Label('Select Country', style=label_style),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=countries[0],
                style=dropdown_style
            )
        ]),
        
        # Year Dropdown
        html.Div([
            html.Label('Select Year', style=label_style),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[-1],
                style=dropdown_style
            )
        ]),
        
        # Sector Dropdown
        html.Div([
            html.Label('Select Employment Sector', style=label_style),
            dcc.Dropdown(
                id='sector-dropdown',
                options=[{'label': sector, 'value': sector} for sector in sector_list],
                value=sector_list[0],
                style=dropdown_style
            )
        ]),
        
        # Predict Button
        html.Button(
            'Predict',
            id='predict-button',
            style={
                'backgroundColor': '#f9943b',
                'color': 'white',
                'padding': '0.75rem 2rem',
                'border': 'none',
                'borderRadius': '4px',
                'cursor': 'pointer',
                'fontSize': '16px',
                'width': '100%',
                'marginTop': '1rem'
            }
        ),
        
        # Result Display
        html.Div(id='prediction-result', style={'marginTop': '2rem', 'textAlign': 'center'})
    ], style=form_container_style)
])