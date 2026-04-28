python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset
data = pd.read_excel('Distribution of Beneficiaries 2022.xlsx')

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('Beneficiaries Distribution Dashboard'),
    dcc.Dropdown(
        id='quarter-dropdown',
        options=[
            {'label': 'Q1', 'value': 'Q1'},
            {'label': 'Q2', 'value': 'Q2'},
            {'label': 'Q3', 'value': 'Q3'},
            {'label': 'Q4', 'value': 'Q4'}
        ],
        value='Q1',
        placeholder='Select a Quarter'
    ),
    dcc.Graph(id='beneficiary-chart'),
    html.Div(id='summary-stats')
])

# Callback to update chart and stats
@app.callback(
    [Output('beneficiary-chart', 'figure'),
     Output('summary-stats', 'children')],
    [Input('quarter-dropdown', 'value')]
)
def update_dashboard(selected_quarter):
    filtered_data = data[data['Quarter'] == selected_quarter]
    
    # Create chart
    fig = px.bar(filtered_data, x='Type', y='Count', color='Gender', title=f'Beneficiary Distribution for {selected_quarter}')
    
    # Create summary statistics
    total_beneficiaries = filtered_data['Count'].sum()
    male_count = filtered_data[filtered_data['Gender'] == 'Male']['Count'].sum()
    female_count = filtered_data[filtered_data['Gender'] == 'Female']['Count'].sum()
    
    summary = f"Total Beneficiaries: {total_beneficiaries}, Males: {male_count}, Females: {female_count}"
    
    return fig, summary

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
