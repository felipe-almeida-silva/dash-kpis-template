import dash
from dash import dcc
from dash import html
from dash import callback
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], )

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H2('home')
])
