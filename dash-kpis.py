import dash
from dash import dcc
from dash import html
from dash import State
from dash.dependencies import Input, Output
from dash_bootstrap_components._components.Container import Container
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages = True, external_stylesheets=[dbc.themes.SPACELAB])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(page['name'], href=page['path']))
        for page in dash.page_registry.values()
    ],
    brand="MOAT AI",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    dbc.Row([
        html.H1('KPIs Dashboard'),
    ],
    style={"text-align": "center"}  # text alignment in the card body
    ),
    dbc.Row([
        navbar
    ]),
    dash.page_container
],
style={"margin-left": "20px",
    "margin-right": "20px",
    })


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
