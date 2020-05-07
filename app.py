#
# LIBRARIES
#

# Dash
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

# Utils
import pandas as pd
import numpy as np
from datetime import datetime

# Self-made
from api_covid import CovidApi

external_stylesheets = [dbc.themes.BOOTSTRAP]

# Placeholder and constant TODO
TIME_PLACEHOLDER = [
    datetime(2019, 10, 12),
    datetime(2020, 4, 25),
]

#
# MAIN APP
#

# Initiate server
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content":"width=device-width, initial-scale=1.0"}
    ],
)

server = app.server

#
# CONSTANTS
#
COLORS = {
    "background": '#FFFFFF'
}

#
# DATASET
#
api = CovidApi()
api.fetch_data(type_data=api.CONFIRMED)
api.fetch_data(type_data=api.DEATHS)
api.fetch_data(type_data=api.RECOVERED)

df2 = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))


#
# LAYOUT
#
app.layout = html.Div(
    id="root",
    className="container",
    style={
        'backgroundColor': COLORS['background'],
    },
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-12 col-sm-12",
                    children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Covid-19 Pandemic Tracker", className="card-title text-center")
                            ])
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-12 col-sm-12",
                    children=[
                        html.Div(
                            id="choropleth-container",
                            children=[
                                html.H5(
                                    "Total confirmed COVID-19 cases across the world",
                                    id="choropleth-title"
                                ),
                                html.P(
                                    "Click on a country to view detailed data on that country"
                                ),
                                dcc.Graph(
                                    id="choropleth-graph",
                                    figure=px.scatter_geo(api.get_data_df(type_data=api.CONFIRMED), 
                                        animation_frame="date",
                                        animation_group="country",
                                        hover_name="country",
                                        custom_data=["date"],
                                        locations="iso_alpha",
                                        projection="natural earth",
                                        size="cases"
                                    )
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-6 col-sm-6",
                    children=[
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id="line-graph",
                                    figure=px.line(
                                        data_frame=df2,
                                        title="Country's Trend"
                                    )
                                )
                            ])
                        )
                    ]
                ),
                html.Div(
                    className="col-6 col-sm-6",
                    children=[
                        dbc.Card(
                            dbc.CardBody([
                                html.H4("Test", className="card-title")
                            ])
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-6 col-sm-6",
                    children=[
                        html.H2("#StayHome", className="text-center")
                    ]
                ),
                html.Div(
                    className="col-6 col-sm-6",
                    children=[
                        html.H2("#StaySafe", className="text-center")
                    ]
                )
            ]
        )
    ]
)


#
# CALLBACKS
#
@app.callback(
    [
        Output('line-graph', 'figure')
    ],
    [
        Input('choropleth-graph', 'clickData')
    ]
)
def handle_choropleth_click(clickData):
    # Get clickData
    data = {
        "name": clickData['points'][0]['hovertext'],
        "code": clickData['points'][0]['location'],
        "cases": clickData['points'][0]['marker.size'],
        "date": clickData['points'][0]['customdata'][0]
    }
    print(data)
    df=api.get_data_df(type_data=api.CONFIRMED)
    print(df.head())

    # Filter DF for line chart
    line_df = df.loc[(df['country'] == data['name']) & (df['date'] <= data['date'])]

    line_title = data['name'] + "'s trend of COVID-19 until " + data['date']
    line_fig = px.line(
        data_frame=line_df,
        x='date',
        y='cases',
        hover_name='cases',
        animation_frame=line_df['date'],
        title=line_title
    )
    
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)