import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

def create_time_series_model(data, country):
    """Create and train time series models for forecasting with trend analysis."""
    years = np.array(range(2005, 2024))
    values = data[data['Country Name'] == country].iloc[0, 1:].astype(float).values
    
    # Add polynomial features for trend analysis
    X = np.column_stack([years.reshape(-1, 1), np.square(years.reshape(-1, 1))])
    y = values.reshape(-1, 1)
    
    # Calculate weights that give more importance to recent years
    weights = np.exp(np.linspace(0, 2, len(years)))  # Increased weight difference
    weights = weights / np.sum(weights)
    
    # Create and train model with sample weights
    model = LinearRegression()
    model.fit(X, y, sample_weight=weights)
    
    return model

def load_historical_data():
    """Load and prepare historical data for forecasting."""
    try:
        # Load data files
        gdp_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'gdp.csv')
        inflation_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'inflation.csv')
        population_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'population.csv')
        labor_force_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'labour_force_participation.csv')
        sector_data = pd.read_csv(PROJECT_ROOT / 'data' / 'raw' / 'employment_by_sector.csv')
        
        # Process GDP and inflation data (already in correct format)
        gdp_data = gdp_data[['Country Name'] + [str(year) for year in range(2005, 2024)]]
        inflation_data = inflation_data[['Country Name'] + [str(year) for year in range(2005, 2024)]]
        
        # Process population data
        population_data = population_data[['Country Name'] + [str(year) for year in range(2005, 2024)]]
        
        # Process labor force data
        labor_force_data = labor_force_data[['Country Name'] + [str(year) for year in range(2005, 2024)]]
        
        # Process sector data
        sector_data = sector_data[sector_data['Disaggregation'].isin(['Agriculture, total', 'Industry, total', 'Services, total'])]
        sector_data['sector'] = sector_data['Disaggregation'].str.split(', ').str[0].str.lower()
        
        return {
            'gdp': gdp_data,
            'inflation': inflation_data,
            'population': population_data,
            'labor_force': labor_force_data,
            'sector': sector_data
        }
    except Exception as e:
        print(f"Error loading historical data: {str(e)}")
        raise

def create_time_series_model(data, country):
    """Create and train time series models for forecasting with trend analysis."""
    years = np.array(range(2005, 2024))
    values = data[data['Country Name'] == country].iloc[0, 1:].astype(float).values
    
    # Add polynomial features for trend analysis
    X = np.column_stack([years.reshape(-1, 1), np.square(years.reshape(-1, 1))])
    y = values.reshape(-1, 1)
    
    # Calculate weights that give more importance to recent years
    weights = np.exp(np.linspace(0, 2, len(years)))  # Increased weight difference
    weights = weights / np.sum(weights)
    
    # Create and train model with sample weights
    model = LinearRegression()
    model.fit(X, y, sample_weight=weights)
    
    return model

def forecast_indicators(country, future_year):
    """Forecast economic indicators for a specific country and year using time series models."""
    try:
        # Load historical data
        historical_data = load_historical_data()
        
        # Create time series models for each indicator
        gdp_model = create_time_series_model(historical_data['gdp'], country)
        inflation_model = create_time_series_model(historical_data['inflation'], country)
        population_model = create_time_series_model(historical_data['population'], country)
        labor_force_model = create_time_series_model(historical_data['labor_force'], country)
        
        # Calculate years since last historical data point
        years_ahead = future_year - 2023  # 2023 is the last historical year
        
        # Enhanced non-linear trend component for long-term predictions with more year-to-year variation
        trend_factor = np.log1p(years_ahead) * (1 + 0.08 * years_ahead) * (1 + 0.02 * np.sin(years_ahead)) if years_ahead > 0 else 0
        
        # Enhanced seasonal adjustment factors with more complex cycles for better differentiation
        seasonal_factor = (
            np.sin(2 * np.pi * (future_year - 2005) / 10) +  # 10-year cycle
            0.7 * np.sin(2 * np.pi * (future_year - 2005) / 5) +  # 5-year cycle
            0.5 * np.sin(2 * np.pi * (future_year - 2005) / 3) +  # 3-year cycle
            0.3 * np.cos(2 * np.pi * (future_year - 2005) / 7) +  # 7-year cycle with phase shift
            0.2 * np.sin(2 * np.pi * (future_year - 2005) / 2)    # 2-year cycle for short-term variations
        ) / 2.5  # Normalize with larger denominator for more controlled variations
        
        # Make predictions with enhanced trend and seasonal adjustments
        future_X = np.array([[future_year, future_year**2]])
        
        gdp_prediction = float(gdp_model.predict(future_X)[0]) * (1 + 0.03 * trend_factor + 0.015 * seasonal_factor)
        inflation_prediction = float(inflation_model.predict(future_X)[0]) * (1 + 0.025 * trend_factor + 0.01 * seasonal_factor)
        population_prediction = float(population_model.predict(future_X)[0]) * (1 + 0.015 * trend_factor + 0.003 * seasonal_factor)
        labor_force_prediction = float(labor_force_model.predict(future_X)[0]) * (1 + 0.02 * trend_factor + 0.005 * seasonal_factor)
        
        # Enhanced sector data prediction with dynamic growth factors
        sector_data = historical_data['sector'][historical_data['sector']['Country Name'] == country]
        base_sector_value = sector_data[sector_data['Year'].between(2018, 2022)]['Value'].mean()
        growth_rate = 0.01 + 0.005 * years_ahead  # Increasing growth rate for future years
        latest_sector_data = base_sector_value * (1 + growth_rate) ** years_ahead
        
        return {
            'gdp_growth': gdp_prediction,
            'inflation_rate': inflation_prediction,
            'population_count': int(population_prediction),
            'labor_force_count': int(labor_force_prediction),
            'sector_value': latest_sector_data
        }
    except Exception as e:
        print(f"Error forecasting indicators: {str(e)}")
        raise