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

# Import the layout functions
from pages.home import home_layout
from pages.sales import sales_layout


app = dash.Dash(__name__, use_pages = True, external_stylesheets=[dbc.themes.SPACELAB])


app.layout = html.Div([
    dbc.Row([
        html.H1("KPIs Dashboard"),
    ],
    style={"text-align": "center"}  # text alignment in the card body
    ),
    dbc.Tabs(
    [
        dbc.Tab(home_layout(), label="Home"),
        dbc.Tab(sales_layout(), label="Sales"),
        dbc.Tab("This tab's content is never seen", label="Tab 3"),
    ],
    style={
        # "height": "44px",
        # "borderBottom": "1px solid #d6d6d6",
        # "padding": "6px",
        # "fontWeight": "bold",
        # "font-color": "white",
        # "borderTop": "1px solid #d6d6d6",
        # "borderBottom": "1px solid #d6d6d6",
        # "backgroundColor": "#119DFF",
        "color": "white",
        # "padding": "6px",
        "margin-top": "20px",
        "margin-bottom": "20px",
    }
    )
],
style={"margin-left": "20px",
    "margin-right": "20px",
    })


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
