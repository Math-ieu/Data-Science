# Import required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(
    "D:/My works/Data-Science/Capstone/spacex_launch_dash.csv")
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites',
                                                     'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40',
                                                  'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E',
                                                  'value': 'VAFB SLC-4E'
                                                  },
                                                 {'label': 'KSC LC-39A',
                                                  'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40',
                                                  'value': 'CCAFS SLC-40'},
                                             ],
                                             value='ALL',
                                             placeholder="Select Site",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )
def total_success_site(site):
    if site == 'ALL':
        spacex_df_success = spacex_df[spacex_df['class'] == 1]
        all_sites_success = spacex_df_success.groupby(
            'Launch Site')['class'].sum()
        fig = px.pie(all_sites_success,
                     values=all_sites_success.values,
                     names=all_sites_success.index,
                     title='Total successful launches count for all sites')
    else:
        lancements_site = spacex_df[spacex_df['Launch Site'] == site]
        success = len(lancements_site[lancements_site['class'] == 1])
        failed = len(lancements_site[lancements_site['class'] == 0])

        fig = px.pie(names=['Success', 'Failed'], values=[
                     success, failed], title=f'Success vs. Failed Launches at {site}')
    return fig
    # TASK 4:
    # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def payload_lauch(site, payload):
    if site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)',
                         y='class', color='Booster Version')
    else:

        fig = px.scatter(spacex_df[(spacex_df['Launch Site'] == site) & ((spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1]))], x='Payload Mass (kg)',
                         y='class', color='Booster Version')
    return fig

    # Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
