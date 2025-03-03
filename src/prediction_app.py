import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import os
import sys
from pathlib import Path

# Get the absolute path to the project root
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and prepare the data
def load_data():
    try:
        gdp_path = PROJECT_ROOT / 'data' / 'raw' / 'gdp.csv'
        unemployment_path = PROJECT_ROOT / 'data' / 'raw' / 'unemployment_sex_age_edu.csv'
        education_path = PROJECT_ROOT / 'data' / 'raw' / 'education_stats.csv'  # New
        labor_path = PROJECT_ROOT / 'data' / 'raw' / 'labor_stats.csv'  # New
        economic_path = PROJECT_ROOT / 'data' / 'raw' / 'economic_indicators.csv'  # New
        
        # Load main datasets
        df = pd.read_csv(gdp_path)
        unemployment_df = pd.read_csv(unemployment_path)
        
        # Load additional datasets if they exist
        additional_data = {}
        if education_path.exists():
            additional_data['education'] = pd.read_csv(education_path)
        if labor_path.exists():
            additional_data['labor'] = pd.read_csv(labor_path)
        if economic_path.exists():
            additional_data['economic'] = pd.read_csv(economic_path)
            
        return df, unemployment_df, additional_data
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

# Replace the direct data loading with the new function
try:
    df, unemployment_df, additional_data = load_data()
except Exception as e:
    print(f"Application failed to start: {str(e)}")
    sys.exit(1)

# Helper function to clean year values
def clean_year(year_val):
    try:
        # If it's already numeric, return as is
        if isinstance(year_val, (int, float)):
            return year_val
        
        # Handle quarterly format (e.g., "2024Q2")
        if isinstance(year_val, str) and 'Q' in year_val:
            return int(year_val.split('Q')[0])
        
        # Try direct conversion
        return int(year_val)
    except (ValueError, TypeError):
        return None

# Data preprocessing function
def prepare_data():
    try:
        # Transform GDP data from wide to long format
        year_columns = [col for col in df.columns if any(str(year) in col for year in range(1960, 2025))]
        id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
        
        # Create GDP data
        gdp_data = df.melt(
            id_vars=id_vars,
            value_vars=year_columns,
            var_name='Year',
            value_name='GDP_Value'
        )
        
        # Print initial data info
        print("\nInitial Data Shapes:")
        print(f"Raw GDP data: {df.shape}")
        print(f"Raw Unemployment data: {unemployment_df.shape}")
        
        # Clean and prepare unemployment data
        unemployment_data = unemployment_df.rename(columns={
            'ref_area.label': 'Country Name',
            'time': 'Year',
            'obs_value': 'Unemployment_Rate'
        })
        
        # Convert years to numeric in both datasets
        gdp_data['Year'] = pd.to_numeric(gdp_data['Year'].apply(clean_year), errors='coerce')
        unemployment_data['Year'] = pd.to_numeric(unemployment_data['Year'].apply(clean_year), errors='coerce')
        
        # Filter recent years
        current_year = 2024
        start_year = current_year - 20
        
        gdp_data = gdp_data[
            (gdp_data['Year'].notna()) & 
            (gdp_data['Year'] >= start_year) & 
            (gdp_data['Year'] <= current_year)
        ].copy()
        
        unemployment_data = unemployment_data[
            (unemployment_data['Year'].notna()) & 
            (unemployment_data['Year'] >= start_year) & 
            (unemployment_data['Year'] <= current_year)
        ].copy()
        
        # Calculate average unemployment rate by country and year
        unemployment_avg = unemployment_data.groupby(
            ['Country Name', 'Year']
        )['Unemployment_Rate'].mean().reset_index()
        
        print("\nProcessed Data Shapes:")
        print(f"GDP data: {gdp_data.shape}")
        print(f"Unemployment data: {unemployment_avg.shape}")
        
        # Merge datasets
        data = pd.merge(gdp_data, unemployment_avg, on=['Country Name', 'Year'], how='inner')
        
        # Calculate GDP growth rate
        data['GDP_Growth'] = data.groupby('Country Name')['GDP_Value'].pct_change() * 100
        
        # Clean up final dataset
        data = data.dropna(subset=['GDP_Growth', 'Unemployment_Rate'])
        
        # Print final data info
        print("\nFinal Dataset Info:")
        print(f"Shape: {data.shape}")
        print("\nSample of final data:")
        print(data[['Country Name', 'Year', 'GDP_Growth', 'Unemployment_Rate']].head())
        print("\nUnique countries:", data['Country Name'].unique())
        print("Year range:", data['Year'].min(), "-", data['Year'].max())
        
        features = ['GDP_Growth']
        target = 'Unemployment_Rate'
        
        return data, features, target
        
    except Exception as e:
        print(f"\nDetailed error in prepare_data:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Data state when error occurred:")
        for var in ['df', 'unemployment_df', 'data']:
            if var in locals():
                print(f"{var} shape:", eval(f"{var}.shape"))
        raise

def train_model(data, features, target):
    try:
        # Validate input data
        if len(data) < 10:
            raise ValueError("Insufficient data for training. Need at least 10 samples.")
            
        X = data[features]
        y = data[target]
        
        # Print training data info
        print("\nTraining Data Info:")
        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        
        # ...rest of existing training code...
        
    except Exception as e:
        print(f"Error in train_model: {str(e)}")
        raise

# Train the model
def train_model(data, features, target):
    X = data[features]
    y = data[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    return model, scaler

# App layout
app.layout = html.Div([
    html.H1("Unemployment Rate Prediction Tool", style={'textAlign': 'center'}),
    
    # Add data summary section
    html.Div([
        html.H3("Dataset Information"),
        html.Ul([
            html.Li(f"Training data from 2017 to 2024"),
            html.Li(f"Coverage: India and Pakistan"),
            html.Li(f"Feature: GDP Growth Rate"),
            html.Li(f"Target: Unemployment Rate")
        ])
    ], style={'margin': '20px'}),
    
    html.Div([
        html.H3("Input Features"),
        html.Div([
            html.Div([
                html.Label("GDP Growth Rate (%)"),
                dcc.Input(id='gdp-growth', type='number', value=2.5, step=0.1),
            ], className='input-group'),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'}),
        
        html.Button(
            'Predict',
            id='predict-button',
            n_clicks=0,
            style={
                'backgroundColor': '#4CAF50',
                'color': 'white',
                'padding': '10px 20px',
                'margin': '20px 0'
            }
        ),
        html.Div(id='prediction-output'),
        dcc.Graph(id='prediction-graph')
    ], style={'margin': '20px'})
], style={'fontFamily': 'Arial, sans-serif'})

# Simplify callback to match actual features
@app.callback(
    [Output('prediction-output', 'children'),
     Output('prediction-graph', 'figure')],
    [Input('predict-button', 'n_clicks')],
    [State('gdp-growth', 'value')]
)
def update_prediction(n_clicks, gdp_growth):
    if n_clicks > 0:
        input_data = np.array([[gdp_growth]])
        prediction = model.predict(scaler.transform(input_data))[0]
        
        # Create scatter plot with historical data
        fig = px.scatter(
            data,
            x='GDP_Growth',
            y='Unemployment_Rate',
            color='Country Name',
            title='Unemployment Rate vs GDP Growth',
            labels={
                'GDP_Growth': 'GDP Growth Rate (%)',
                'Unemployment_Rate': 'Unemployment Rate (%)'
            }
        )
        
        # Add prediction point
        fig.add_scatter(
            x=[gdp_growth],
            y=[prediction],
            mode='markers',
            marker=dict(size=15, symbol='star', color='red'),
            name='Prediction',
            showlegend=True
        )
        
        fig.update_layout(
            title_x=0.5,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        return [
            html.Div([
                html.P("Predicted Unemployment Rate:"),
                html.H2(f"{prediction:.2f}%")
            ])
        ], fig
    
    return 'Enter GDP Growth Rate and click Predict', {}

if __name__ == '__main__':
    try:
        # Prepare data and train model
        data, features, target = prepare_data()
        model, scaler = train_model(data, features, target)
        
        # Run the app
        app.run_server(debug=True)
    except Exception as e:
        print(f"Error starting the application: {str(e)}")
        sys.exit(1)
