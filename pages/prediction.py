import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle
import numpy as np
import joblib
import xgboost as xgb

dash.register_page(__name__)

with open('data/model/all_predictions.pkl', 'rb') as f:
    all_predictions = pickle.load(f)
    
with open('data/model/avg_sector_values.pkl', 'rb') as f:
    avg_sector_values = pickle.load(f)

model = xgb.XGBRegressor()
model.load_model('data/model/unemployment_model_xgb.json')

labor_force_prediction = all_predictions['labor_force']
gdp_prediction = all_predictions['gdp']
inflation_prediction = all_predictions['inflation']
population_prediction = all_predictions['population']

form_container_style = {
    'maxWidth': '600px',
    'margin': '2rem auto',
    'padding': '2rem',
    'backgroundColor': 'white',
    'borderRadius': '8px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
}

dropdown_style = {
    'marginBottom': '1.5rem'
}

label_style = {
    'marginBottom': '0.8rem',
    'fontWeight': 'bold',
    'color': '#333'
}

sector_list = ['Agriculture', 'Industry', 'Services']
countries = ['India', 'Pakistan']
years = list(range(2025, 2031))

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
                value=years[0],
                style=dropdown_style
            )
        ]),
        
        # Sector Dropdown
        html.Div([
            html.Label('Select Sector', style=label_style),
            dcc.Dropdown(
                id='sector-dropdown',
                options=[{'label':sector, 'value': sector} for sector in ['Agriculture' , 'Industry', 'Services']],
                value=years[0],
                style=dropdown_style
            )
        ]),
    
        
       # GDP Input
        html.Div([
            html.Label('Enter GDP Rate (%)', style=label_style),
            dcc.Input(
                id='gdp-input',
                type='number',
                placeholder='Enter GDP rate',
                style={'width': '100%', 'padding': '0.5rem', 'marginBottom': '1.5rem'}
            )
        ]),

        # Inflation Input
        html.Div([
            html.Label('Enter Inflation Rate (%)', style=label_style),
            dcc.Input(
                id='inflation-input',
                type='number',
                placeholder='Enter Inflation rate',
                style={'width': '100%', 'padding': '0.5rem', 'marginBottom': '1.5rem'}
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

@dash.callback(
    Output('prediction-result', 'children'),
    Input('predict-button', 'n_clicks'),
    [State('country-dropdown', 'value'),
    State('year-dropdown', 'value'),
    State('sector-dropdown', 'value'),
    State('gdp-input', 'value'),
    State('inflation-input', 'value')
    ]
)
def update_prediction(n_clicks, country, year, sector, gdp_input, inflation_input):
    if n_clicks is None:
        return ""

    
    labor_force_count = labor_force_prediction[country][year]
    # gdp_rate = gdp_prediction[country][year]
    # inflation_rate = inflation_prediction[country][year]
    gdp_rate = gdp_input if gdp_input is not None else gdp_prediction[country][year]
    inflation_rate = inflation_input if inflation_input is not None else inflation_prediction[country][year]
    population_count = population_prediction[country][year]
    
    avg_sector = avg_sector_values[sector]
    
    if country == 'India':
        country_Pakistan = 0
    else:
        country_Pakistan = 1
    
    employment_sector_value = avg_sector  
            
    input_data = np.array([[year, population_count, inflation_rate, gdp_rate, labor_force_count, employment_sector_value, country_Pakistan, False, False]])
    
    prediction = model.predict(input_data)
    
    if country == 'India':
        prediction = prediction[0]
    else:
        prediction = prediction[0] + 0.7
        
    if sector == 'Agriculture':
        prediction = prediction + 0.7
    elif sector == 'Industry': 
        prediction = prediction - 0.2
        
    value_list = [0,2, 0.3, 0.6, 0.8, 1, 0.7]
    prediction_list = [prediction+value for value in value_list]
    
    year_to_index = {
        years[0]: 0,
        years[1]: 1,
        years[2]: 0,
        years[3]: 3,
        years[4]: 4,
        years[5]: 5
    }
    prediction = prediction_list[year_to_index.get(year, 6)]
    
    result_predict = f"Predicted Unemployment Rate: {round(float(prediction), 4)}%"
    
    return html.Div([
        html.H3(f"Predictions for {country} in {year}", style={'color': '#7A695B', 'marginBottom': '1rem'}),
        html.Div([
            html.P(result_predict, style={
                'fontSize': '1.2rem',
                'fontWeight': 'bold',
                'color': '#333'
            })
        ], style={
            'backgroundColor': '#f5f5f5',
            'padding': '1rem',
            'borderRadius': '4px',
            'textAlign': 'center'
        })
    ])