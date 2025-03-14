# Import required libraries
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
app.layout = html.Div(children=[
                            html.H1('SpaceX Launch Records Dashboard',
                            style={'textAlign': 'center', 'color': '#503D36',
                            'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                            dcc.Dropdown(id='site-dropdown',
		                            options=[
                			          {'label': 'All Sites', 'value': 'ALL'},
			                          {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
			                          ],
			                          value='ALL',
			                          placeholder="Select a Launch Site here",
			                          searchable=True
		                         ),

                            html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                #dcc.Graph(figure=px.histogram(spacex_df, x='Launch Site', y='class', histfunc='sum')),
                                #dcc.Graph(figure=px.pie(spacex_df, values='class', names='Launch Site')),
                                #dcc.Graph(figure=px.pie(spacex_df, values='class', names=spacex_df['Launch Site']=='CCAFS LC-40')),
                            dcc.Graph(id='success-pie-chart'),

                            html.Br(),
                            html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                            dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={ 0: '0',
                                        1000: '1000',
                                        2000: '2000',
                                        3000: '3000',
                                        4000: '4000',
                                        5000: '5000',
                                        6000: '6000',
                                        7000: '7000',
                                        8000: '8000',
                                        9000: '9000',
                                        10000: '10000'
                                },
                                value=[0, 10000]
                            ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                            
                            html.P("Scatter Chart Payload"),
                            html.Div(dcc.Graph(id='success-payload-scatter-chart')
                            )                             

                  ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
# NOTE: component_property='figure' and component_property='value' ARE fixed arguments that
#       are not mentioned anywhere in the code
# NOTE: return fig is also a FIXED parameter name not mentioned anywhere and it is assumed
#       that is returned by the callback function somehow

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
              Output(component_id='success-payload-scatter-chart', component_property='figure')],
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider',component_property='value')
              )

def get_pie_chart(entered_site,slider_values):
    min_value=slider_values[0]
    max_value=slider_values[1]
    #filtered_df=spacex_df
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] >= min_value ]
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] <= max_value ]
    scatter_df=filtered_df['Launch Site']==entered_site
    if entered_site == 'ALL':
      fig1 = px.pie(filtered_df, values='class',
      names='Launch Site',
      title='ALL SITES')
      fig2 = px.scatter(filtered_df, x=filtered_df['Payload Mass (kg)'], y=filtered_df['class'],color=filtered_df['Booster Version Category'])
      fig2.update_layout(
          xaxis_title='Payload Mass (kg)', # x-axis name
          yaxis_title='class', # y-axis name
      )
      return [fig1,fig2]
    else:
      fig1 = px.pie(filtered_df, values='class',
      names=filtered_df['Launch Site']==entered_site,
      title=entered_site)
      fig2 = px.scatter(scatter_df, x=filtered_df['Payload Mass (kg)'], y=filtered_df['class'],color=filtered_df['Booster Version Category'])
      fig2.update_layout(
          xaxis_title='Payload Mass (kg)', # x-axis name
          yaxis_title='class', # y-axis name
      )
      return [fig1,fig2]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
