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
from api.api_covid import CovidApi

external_stylesheets = [dbc.themes.BOOTSTRAP]

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
app.title = "COVID-19 Tracker"

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

latest_date = api.dfs[api.CONFIRMED]['date'].unique()[-1]
df_confirmed_init = api.dfs[api.CONFIRMED].groupby('date').sum().reset_index()
df_deaths_init = api.dfs[api.DEATHS].groupby('date').sum().reset_index()
df_recovered_init = api.dfs[api.RECOVERED].groupby('date').sum().reset_index()
data_pie = api.dfs[api.CONFIRMED].loc[api.dfs[api.CONFIRMED]['date'] == latest_date].groupby('continent').sum().reset_index()


#
# LAYOUTS
# 
line_layout = go.Layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title="World's COVID-19 case trend until " + latest_date,
    font=dict(
        color="#a3a7b0"
    )
)
def update_line_layout(data):
    new_line_layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=data['name'] + "'s COVID-19 trend until " + data['date'],
        font=dict(
            color="#a3a7b0"
        )
    )
    return new_line_layout 

pie_layout = go.Layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title="World's COVID-19 case percentages on " + latest_date,
    font=dict(
        color="#a3a7b0"
    )
)
def update_pie_layout(data):
    new_pie_layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title="Percentage of " + data['name'] + "'s confirmed cases compared to the world on " + data['date'],
        font=dict(
            color="#a3a7b0"
        )
    )
    return new_pie_layout



#
# FIGURES
#

# Initial line figures (world's trend)
line_fig_init = go.Figure(layout=line_layout)


line_fig_init.update_layout(plot_bgcolor='#23272c', )

line_fig_init.add_trace(go.Scatter(
    x=df_confirmed_init['date'],
    y=df_confirmed_init['confirmed'],
    mode='lines+markers',
    name='Confirmed'
))
line_fig_init.add_trace(go.Scatter(
    x=df_deaths_init['date'],
    y=df_deaths_init['deaths'],
    mode='lines+markers',
    name='Deaths'
))
line_fig_init.add_trace(go.Scatter(
    x=df_recovered_init['date'],
    y=df_recovered_init['recovered'],
    mode='lines+markers',
    name='Recovered'
))


# Initial pie figures (percentage per continent)
pie_fig_init = go.Figure(
    data=[
        go.Pie(
            labels=data_pie['continent'],
            values=data_pie['confirmed']
        )
    ],
    layout=pie_layout,
)

# Scatter geo figure
geo_figure=px.scatter_geo(
    api.get_data_df(type_data=api.CONFIRMED), 
    animation_frame="date",
    animation_group="country",
    hover_name="country",
    color="continent",
    custom_data=["date"],
    locations="iso_alpha3",
    projection="natural earth",
    size="confirmed",
)
geo_figure.update_geos(
    resolution=50,
    showcoastlines=True,
    showland=True, landcolor='rgb(217,217,217)',
    showocean=True, oceancolor="rgb(35,39,44)",
    showlakes=False,
    showrivers=False,
    showcountries=True, countrycolor="Black",
    projection_type='equirectangular',
)

geo_figure.update_layout(
    margin={
        "r":0,"t":0,"l":0,"b":0
    },
    plot_bgcolor='rgb(35,39,44)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(
        color="#a3a7b0",
    )
)


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
                            className="graph-container",
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
                                    figure=geo_figure,
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
                    className="col-12 col-sm-12",
                    children=[
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id="line-graph",
                                    figure=line_fig_init
                                )
                            ])
                        ),

                    ]
                ),
                html.Div(
                    className="col-12 col-sm-12",
                    children=[
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(
                                    id="pie-graph",
                                    figure=pie_fig_init,
                                )
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
                    className="col-6 col-sm-6 dark-mode",
                    children=[
                        html.H2("#StayHome", className="text-center")
                    ]
                ),
                html.Div(
                    className="col-6 col-sm-6 dark-mode",
                    children=[
                        html.H2("#StaySafe", className="text-center")
                    ]
                )
            ]
        )
    ]
)

#
# Functions
#
def filter_by_country_date(df, click_data):
    return df.loc[(df['country'] == click_data['name']) & (df['date'] <= click_data['date'])]


#
# CALLBACKS
#
@app.callback(
    [
        Output('line-graph', 'figure'),
        Output('pie-graph', 'figure')
    ],
    [
        Input('choropleth-graph', 'clickData')
    ]
)
def handle_choropleth_click(clickData):
    # Get clickData
    if clickData is None:
        return [line_fig_init,pie_fig_init]

    data = {
        "name": clickData['points'][0]['hovertext'],
        "code": clickData['points'][0]['location'],
        "confirmed": clickData['points'][0]['marker.size'],
        "date": clickData['points'][0]['customdata'][0]
    }

    # Process DF
    df_confirmed_all = api.get_data_df(type_data=api.CONFIRMED)
    df_confirmed_filtered = filter_by_country_date(df_confirmed_all, data)
    df_deaths_all = api.get_data_df(type_data=api.DEATHS)
    df_deaths_filtered = filter_by_country_date(df_deaths_all, data)
    df_recovered_all = api.get_data_df(type_data=api.RECOVERED)
    df_recovered_filtered = filter_by_country_date(df_recovered_all, data)

    # Update line chart
    new_line_layout = update_line_layout(data)
    line_fig = go.Figure(layout=new_line_layout)
    line_fig.add_trace(go.Scatter(
        x=df_confirmed_filtered['date'],
        y=df_confirmed_filtered['confirmed'],
        mode='lines+markers',
        name='Confirmed'
    ))
    line_fig.add_trace(go.Scatter(
        x=df_deaths_filtered['date'],
        y=df_deaths_filtered['deaths'],
        mode='lines+markers',
        name='Deaths'
    ))
    line_fig.add_trace(go.Scatter(
        x=df_recovered_filtered['date'],
        y=df_recovered_filtered['recovered'],
        mode='lines+markers',
        name='Recovered'
    ))

    # Update pie chart
    country_confirmed_cases = df_confirmed_filtered.loc[df_confirmed_filtered['date'] == data['date'], 'confirmed'].tolist()[0]
    total_confirmed_cases = df_confirmed_all.loc[df_confirmed_all['date'] == data['date']]['confirmed'].sum()
    pie_df = pd.DataFrame([
        {
            "Country": data['name'],
            "Confirmed": country_confirmed_cases
        },
        {
            "Country": "Others",
            "Confirmed": total_confirmed_cases
        }
    ])
    pie_title = "Percentage of " + data['name'] + "'s confirmed cases compared to the world on " + data['date']
    new_pie_layout = update_pie_layout(data)
    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=pie_df['Country'],
                values=pie_df['Confirmed']
            ),
        ],
        layout=new_pie_layout
        # data_frame=pie_df,
        # names="Country",
        # values="Confirmed",
        # title=pie_title
    )

    return [line_fig, pie_fig]


if __name__ == '__main__':
    app.run_server(debug=True)