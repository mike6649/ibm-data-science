# Import required libraries
from logging import PlaceHolder
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', searchable=True, placeholder="Select a launch site here", options=[
                                    {'label': 'ALL', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                               dcc.RangeSlider(id='payload-slider', min=min_payload, max=max_payload, step=1000,
                               value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', component_property='value')])
def update_pie_chart(value):
    if value == 'ALL':
        df = spacex_df.groupby('Launch Site')['class'].sum().to_frame().reset_index()
        return px.pie(df, names='Launch Site', values='class')
    else:
        df = spacex_df[spacex_df['Launch Site'] == value].groupby('class').count().reset_index()
        print(df.head())
        return px.pie(df, names='class', values='Flight Number');
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
)
def update_payload(dropdown_val, payload_val):
    if dropdown_val == 'ALL':
        df = spacex_df
    else:
        df = spacex_df[spacex_df['Launch Site'] == dropdown_val]
    df = df[(spacex_df['Payload Mass (kg)'] >= payload_val[0]) & (spacex_df['Payload Mass (kg)'] < payload_val[1])]
    return px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')

# Run the app
if __name__ == '__main__':
    app.run_server()
