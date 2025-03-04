import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from src.forecasting import forecast_indicators

# Initialize the Dash app
app = dash.Dash(__name__)

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Load the data
def load_data():
    try:
        # Load the unemployment rate data
        unemployment_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'unemployment_rate.csv')
        # Transform unemployment data from wide to long format
        unemployment_data = unemployment_data.melt(
            id_vars=['Country Name'],
            var_name='Year',
            value_name='Rate'
        )
        unemployment_data['Year'] = pd.to_numeric(unemployment_data['Year'])  # Convert Year to numeric
        
        gdp_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'gdp.csv')
        inflation_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'inflation.csv')
        
        return unemployment_data, gdp_data, inflation_data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

# Load the trained model
model = joblib.load(PROJECT_ROOT / 'data' / 'model' / 'unemployment_model_xgb.joblib')

# Load the data
unemployment_data, gdp_data, inflation_data = load_data()

# App layout
app.layout = html.Div([
    html.H1("Unemployment Rate Prediction Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Input Section
    html.Div([
        html.Div([
            html.Label("Select Country"),
            dcc.Dropdown(
                id='country-selector',
                options=[
                    {'label': 'India', 'value': 'India'},
                    {'label': 'Pakistan', 'value': 'Pakistan'}
                ],
                value='India'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Enter Year"),
            dcc.Input(
                id='year-input',
                type='number',
                min=2024,
                max=2030,
                value=2024,
                step=1
            )
        ], style={'width': '20%', 'display': 'inline-block', 'marginRight': '20px'}),


        
        html.Button(
            'Predict',
            id='predict-button',
            n_clicks=0,
            style={
                'backgroundColor': '#4CAF50',
                'color': 'white',
                'padding': '10px 20px',
                'marginTop': '20px',
                'border': 'none',
                'borderRadius': '4px',
                'cursor': 'pointer'
            }
        )
    ], style={'marginBottom': '30px'}),
    
    # Results Section
    html.Div([
        html.Div(id='prediction-output', style={'textAlign': 'center', 'marginBottom': '20px'}),
        dcc.Graph(id='historical-trend'),
        dcc.Graph(id='prediction-graph')
    ])
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

@app.callback(
    [
        Output('prediction-output', 'children'),
        Output('historical-trend', 'figure'),
        Output('prediction-graph', 'figure')
    ],
    [
        Input('predict-button', 'n_clicks')
    ],
    [
        State('country-selector', 'value'),
        State('year-input', 'value')
    ]
)
def update_prediction(n_clicks, country, year):
    if n_clicks > 0:
        # Get forecasted economic indicators including sector
        indicators = forecast_indicators(country, year)
        
        # Create country indicator variable
        country_pakistan = 1 if country == 'Pakistan' else 0

        # Calculate sector indicators based on sector value
        sector_total = indicators['sector_value']
        sector_industry = sector_total * 0.3  # Assuming 30% industry share
        sector_services = sector_total * 0.5  # Assuming 50% services share

        # Prepare input features for prediction
        input_features = np.array([
            [year, indicators['population_count'], indicators['inflation_rate'], 
             indicators['gdp_growth'], indicators['labor_force_count'], 
             indicators['sector_value'], country_pakistan, sector_industry, sector_services]
        ])
        
        # Make prediction
        predicted_rate = model.predict(input_features)[0]
        
        # Filter data for selected country and create historical trend plot
        country_data = unemployment_data[unemployment_data['Country Name'] == country]
        historical_fig = px.line(
            country_data,
            x='Year',
            y='Rate',
            title=f'Historical Unemployment Rate in {country}',
            labels={'Rate': 'Unemployment Rate (%)', 'Year': 'Year'}
        )
        
        # Create prediction visualization with all features
        prediction_data = pd.DataFrame({
            'Feature': ['GDP Growth Rate', 'Inflation Rate', 'Population (Millions)', 
                       'Labor Force (Millions)', 'Sector Value'],
            'Value': [indicators['gdp_growth'], indicators['inflation_rate'], 
                      indicators['population_count']/1e6, indicators['labor_force_count']/1e6, 
                      indicators['sector_value']]
        })
        
        prediction_fig = px.bar(
            prediction_data,
            x='Feature',
            y='Value',
            title=f'Input Features for {year} Prediction',
            labels={'Value': 'Value'}
        )
        
        return [
            html.Div([
                html.H3(f"Predicted Unemployment Rate for {country} in {year}:"),
                html.H2(f"{predicted_rate:.2f}%", style={'color': '#4CAF50'})
            ]),
            historical_fig,
            prediction_fig
        ]
    
    # Return empty figures if no prediction made
    return [
        'Enter parameters and click Predict',
        {},
        {}
    ]

if __name__ == '__main__':
    app.run_server(debug=True)