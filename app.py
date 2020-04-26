import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Placeholder and constant TODO
TIME_PLACEHOLDER = [
    datetime(2019, 10, 12),
    datetime(2020, 4, 25),
]

# Initiate server
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content":"width=device-width, initial-scale=1.0"}
    ],
)

server = app.server

# Load Data

df = px.data.gapminder() # TODO: replace data
df2 = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))


# App Layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H1(
                    id="description",
                    children="Covid-19 Pandemic",
                ),
            ], style={"text-align":"center", "margin-top":"3%"}
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="top-section",
                    children=[
                        html.P(
                            id="slider-text",
                            children="Drag the slider to change the time"
                        ),
                        dcc.Slider(
                            id="time-slider",
                            min=0,
                            max=1,
                            value=0,
                            marks={
                                str(time.strftime("%m/%d/%Y")): {
                                    "label": str(time.strftime("%m/%d/%Y")),
                                    "style": {"color": "#7fafdf"},
                                }
                                for time in TIME_PLACEHOLDER
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="choropleth-container",
                    children=[
                        html.H5(
                            "Total confirmed COVID-19 cases across the world in {}".format(str(TIME_PLACEHOLDER[0].strftime("%m/%d/%Y"))),
                            id="choropleth-title",
                        ),
                        html.P(
                            "Click on a country to view detailed data on that country"
                        ),
                        dcc.Graph(
                            id="world-choropleth",
                            figure=px.scatter_geo(df, 
                                locations="iso_alpha",
                                size="pop",
                                color="continent",
                                hover_name="country",
                                animation_frame="year",
                                projection="natural earth"
                            ),
                        ),
                    ],
                ),
                html.Div(
                    id="bottom-section",
                    children=[
                        html.Div(
                            id="line-container",
                            children=[
                                html.H5(
                                    "World-wide increase in total cases",
                                    id="line-title",
                                ),
                                dcc.Graph(
                                    id="left-graph",
                                    figure=px.line(df2),
                                ),
                            ], className="six columns"
                        ),
                        html.Div(
                            id="bar-container",
                            children=[
                                html.H5(
                                    "Comparison of total cases between countries",
                                    id="bar-title",
                                ),
                                dcc.Graph(
                                    id="right-graph",
                                    figure=go.Figure(
                                        data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
                                        layout=go.Layout(
                                            title=go.layout.Title(text="A Figure Specified By A Graph Object")
                                        )
                                    ),
                                ),
                            ], className="six columns"
                        ),
                    ], style={"margin-top":"3%", "margin-bottom":"3%"}
                ),
                html.Div(
                    id="footer",
                    children=[
                        html.Div(
                            id="footer-message-1",
                            children=[
                                html.H2(
                                    "#StayHome"
                                ),
                            ], style={"text-align":"center", "margin-top":"3%", "margin-bottom":"3%"}, className="six columns"
                        ),
                        html.Div(
                            id="footer-message-2",
                            children=[
                                html.H2(
                                    "#StaySafe"
                                ),
                            ], style={"text-align":"center", "margin-top":"3%", "margin-bottom":"3%"}, className="six columns"
                        ),
                    ],
                ),
            ], style={"margin":"3% 5%"}
        ),
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True)