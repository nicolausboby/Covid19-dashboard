import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from urllib.request import urlopen
import json

from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Placeholder and constant
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

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')




# App Layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.P(
                    id="description",
                    children="Covid-19 dashboard",
                ),
            ],
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
                            min=min(TIME_PLACEHOLDER),
                            max=max(TIME_PLACEHOLDER),
                            value=min(TIME_PLACEHOLDER),
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
                    
                )
            ],
        ),
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True)