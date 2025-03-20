from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go

external_stylesheets = [dbc.themes.BOOTSTRAP]

dash.register_page(__name__, path='/')

unemployment_rate_df = pd.read_csv('data/clean_data/unemployment_rate.csv')
unemploy_sex_age_edu_india = pd.read_csv('data/clean_data/unemploy_sex_age_edu_india.csv')
unemploy_sex_age_edu_pakistan = pd.read_csv('data/clean_data/unemploy_sex_age_edu_pakistan.csv')
unemploy_sex_age_region_india = pd.read_csv('data/clean_data/unemploy_sex_age_region_india.csv')
unemploy_sex_age_region_pakistan = pd.read_csv('data/clean_data/unemploy_sex_age_region_pakistan.csv')
merged_df = pd.read_csv('data/clean_data/merge_df.csv')

# For Graph 1
unemployment_rate_fig = px.line(unemployment_rate_df, x='year', 
                        y='rate', title='Unemployment Rate: India & Pakistan', color='country', labels={'year': 'Year', 'rate': 'Rate'})
unemployment_rate_fig.update_layout(legend_title='Country')

# For Graph 2
unemploy_sex_age_edu_india_fig = px.histogram(unemploy_sex_age_edu_india, x='age_bracket', y='mean', color='gender', barmode='group', histfunc='avg', labels={'age_bracket': 'Age'}
                                            ,title='Unemployment Rate in India by Age and Gender',)
unemploy_sex_age_edu_india_fig.update_layout(yaxis_title="Average Unemployment Rate", legend_title='Gender')

# For Graph 3
unemploy_sex_age_edu_pakistan_fig = px.histogram(unemploy_sex_age_edu_pakistan, x='age_bracket', y='mean', color='gender', barmode='group', histfunc='avg', labels={'age_bracket': 'Age'}
                                            ,title='Unemployment Rate in Pakistan by Age and Gender',)
unemploy_sex_age_edu_pakistan_fig.update_layout(yaxis_title="Average Unemployment Rate", legend_title='Gender')

# For Graph 4
merged_df_india = merged_df[merged_df['country_Pakistan'] == False]
merged_df_india = merged_df_india.select_dtypes(include=[np.number])
merged_df_india = merged_df_india[['rate', 'labor_force_count', 'gdp_rate', 'inflation_rate', 'population_count']]
merged_df_india = merged_df_india.rename(columns={"rate": "Unemployment Rate", "labor_force_count": "Labor Force Count", "gdp_rate": "GDP Rate", "inflation_rate": "Inflation Rate", "population_count": "Population Count"})
correlation_matrix = merged_df_india.corr()

merged_df_india_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns,
    y=correlation_matrix.index,
    colorscale="RdBu_r",
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation"),
    text=np.round(correlation_matrix.values, 2), 
    texttemplate="%{text}", 
    hoverinfo="text" 
))
merged_df_india_corr.update_layout(title="Correlation of Unemployment & Economic Indicators in India")

# For Graph 5
merged_df_pakistan = merged_df[merged_df['country_Pakistan'] == True]
merged_df_pakistan = merged_df_pakistan.select_dtypes(include=[np.number])
merged_df_pakistan = merged_df_pakistan[['rate', 'labor_force_count', 'gdp_rate', 'inflation_rate', 'population_count']]
merged_df_pakistan = merged_df_pakistan.rename(columns={"rate": "Unemployment Rate", "labor_force_count": "Labor Force Count", "gdp_rate": "GDP Rate", "inflation_rate": "Inflation Rate", "population_count": "Population Count"})
correlation_matrix_2 = merged_df_pakistan.corr()

merged_df_pakistan_corr = go.Figure(data=go.Heatmap(
    z=correlation_matrix_2.values,
    x=correlation_matrix_2.columns,
    y=correlation_matrix_2.index,
    colorscale="RdBu_r",
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation"),
    text=np.round(correlation_matrix_2.values, 2), 
    texttemplate="%{text}", 
    hoverinfo="text" 
))
merged_df_pakistan_corr.update_layout(title="Correlation of Unemployment & Economic Indicators in Pakistan")

# For Graph 6
unemploy_sex_age_region_india_fig = px.pie(unemploy_sex_age_region_india, values='mean', names='region',
                                            title='Unemployment Rate in India by Region')
unemploy_sex_age_region_india_fig.update_layout(legend_title='Region')

# For Graph 7
unemploy_sex_age_region_pakistan_fig = px.pie(unemploy_sex_age_region_pakistan, values='mean', names='region',
                                            title='Unemployment Rate in Pakistan by Region')
unemploy_sex_age_region_pakistan_fig.update_layout(legend_title='Region')


layout = dbc.Container([
    dbc.Row([
        html.H1('Unemployment Analysis in India & Pakistan', style={'textAlign': 'center', 'marginTop': '3rem', 'marginBottom': '2rem', 'color': '#7A695B'}),
    ]),
    dbc.Row([
        # Graph 1
        dbc.Col([
            dcc.Graph(id='unemployment_rate_fig' ,figure=unemployment_rate_fig, className='shadow_box')
        ], width=12, className='mt-4'),
    ]),
    dbc.Row([
        # Graph 2
        dbc.Col([
            dcc.Graph(id='unemploy_sex_age_edu_india_fig' ,figure=unemploy_sex_age_edu_india_fig, className='shadow_box')
        ], width=6, className='mt-5'),
        # Graph 3
        dbc.Col([
            dcc.Graph(id='unemploy_sex_age_edu_pakistan_fig' ,figure=unemploy_sex_age_edu_pakistan_fig, className='shadow_box')
        ], width=6, className='mt-5'),
    ]),
    dbc.Row([
        # Graph 4
        dbc.Col([
            dcc.Graph(id='merged_df_india_corr' ,figure=merged_df_india_corr, className='shadow_box')
        ], width=6, className='mt-5'),
        # Graph 5
        dbc.Col([
            dcc.Graph(id='merged_df_pakistan_corr' ,figure=merged_df_pakistan_corr, className='shadow_box')
        ], width=6, className='mt-5'),
    ]),
    dbc.Row([
        # Graph 6
        dbc.Col([
            dcc.Graph(id='unemploy_sex_age_region_india_fig' ,figure=unemploy_sex_age_region_india_fig, className='shadow_box')
        ], width=6, className='mt-5'),
        dbc.Col([
            dcc.Graph(id='unemploy_sex_age_region_pakistan_fig' ,figure=unemploy_sex_age_region_pakistan_fig, className='shadow_box')
        ], width=6, className='mt-5'),
    ]),
], className='analysis_page')

