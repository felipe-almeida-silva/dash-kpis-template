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

dash.register_page(__name__, path='/sales')


### ETL ###
# reading the data from the csv file
df_sales = pd.read_csv('sales.csv', encoding='ISO-8859-1')
# df_sales.drop('Row ID', axis=1, inplace=True)

# drop the columns that are all NaN
df_sales.dropna(axis=1, how='all', inplace=True)

# Convert the column names to lower and replace ' ' to '_'
df_sales.columns = df_sales.columns.str.lower().str.replace(' ', '_').str.replace('-','_')

# Convert the 'order_date' column to datetime
df_sales['order_date'] = pd.to_datetime(df_sales['order_date'], dayfirst=True)
# df_sales['ship_date'] = pd.to_datetime(df_sales['ship_date'], dayfirst=True)

# Convert country, state, city, state, region, category, sub-category, ship_mode to categorical
# df_sales['country'] = df_sales['country'].astype('category')
# df_sales['state'] = df_sales['state'].astype('category')
# df_sales['city'] = df_sales['city'].astype('category')
# df_sales['region'] = df_sales['region'].astype('category')
df_sales['category'] = df_sales['category'].astype('category')
df_sales['sub_category'] = df_sales['sub_category'].astype('category')
# df_sales['ship_mode'] = df_sales['ship_mode'].astype('category')
df_sales['segment'] = df_sales['segment'].astype('category')

# Convert order_id, customer_id, customer_name, product_id, product_name to string
df_sales['order_id'] = df_sales['order_id'].astype('str')
df_sales['customer_id'] = df_sales['customer_id'].astype('str')
df_sales['customer_name'] = df_sales['customer_name'].astype('str')
df_sales['product_id'] = df_sales['product_id'].astype('str')
df_sales['product_name'] = df_sales['product_name'].astype('str')

# Convert sales and profit to numeric
df_sales['sales'] = df_sales['sales'].str.replace(',', '')
df_sales['sales'] = pd.to_numeric(df_sales['sales'], errors='coerce')
df_sales['profit'] = df_sales['profit'].str.replace(',', '')
df_sales['profit'] = pd.to_numeric(df_sales['profit'], errors='coerce')

# total sales
total_sales = df_sales['sales'].sum()

# Average Sales: This is the average sales value over a certain period.
average_sales = df_sales['sales'].mean()

# Number of Orders: The total number of orders can be a good KPI to track the overall activity. In this case, you can count the unique 'Order ID'
num_orders = df_sales['order_id'].nunique()

# Average Order Value: This is the average value of each order. It can be calculated as Total Sales divided by Number of Orders.
avg_order_value = total_sales / num_orders

# Sales by Category: This shows which categories of products are generating more sales.
sales_by_category = df_sales.groupby('category')['sales'].sum()

# Overall Profit Margin
overall_profit = df_sales['profit'].sum() /  df_sales['sales'].sum()

# sales by month/quarter: This gives a time-series breakdown of the sales, helping you understand the seasonal trends in sales. 
# To do this, first convert 'order_date' to datetime and then extract the month or quarter.
df_sales['year'] = df_sales['order_date'].dt.year
df_sales['month'] = df_sales['order_date'].dt.month
df_sales['quarter'] = df_sales['order_date'].dt.quarter

sales_by_month_year = df_sales.groupby(['year', 'month'])['sales'].sum()
sales_by_quarter_year = df_sales.groupby(['year', 'quarter'])['sales'].sum()

# Profitability
total_profit = df_sales['profit'].sum()

# Profit Margin
profit_margin = total_profit / total_sales

### Finish ETL ###

### filters ###
years = df_sales['order_date'].dt.year.unique()
years = np.sort(years)
# invert list
years = years[::-1]

categories = df_sales['category'].unique()

sub_categories = df_sales['sub_category'].unique()
### end filters ###

# # app.layout = html.Div([
layout = html.Div([
    dcc.Store(id='data-store', data=df_sales.to_dict('records')),
    # dbc.Row([html.H3("Year")], style={"margin-top": "10px"}),
    dbc.Row([
        dbc.Col([
            dbc.Row([html.H3("Year")]),  # nested row for header
            dbc.Row([  # nested row for content
                dcc.Dropdown(id='year-selector', 
                             options=[{'label': year, 'value': year} for year in years], 
                             value=years, 
                             multi=True)
            ]),
        ], width=4),
        dbc.Col([
            dbc.Row([html.H3("Category")]),  # nested row for header
            dbc.Row([ dcc.Dropdown(id='category-selector', 
                             options=[{'label': category, 'value': category} for category in categories], 
                             value=categories, 
                             multi=True)
            ]),
        ], width=4),
        dbc.Col([
            dbc.Row([html.H3("Sub Category")]),  # nested row for header
            dbc.Row([dcc.Dropdown(id='sub-category-selector', 
                             options=[{'label': sub_categor, 'value': sub_categor} for sub_categor in sub_categories], 
                             value=sub_categories, 
                             multi=True)
            ]),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col(id='card-total-sales', width=3),
        dbc.Col(id='card-average-sales', width=3),
        dbc.Col(id='card-num-orders', width=3),
        dbc.Col(id='card-avg-order-value', width=3),
    ]),
    dbc.Row([
        dbc.Col(id='card-profit', width=3),
        dbc.Col(id='card-profit-margin', width=3),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-by-category-graph'), width=6),
        dbc.Col(dcc.Graph(id='sales-by-quarter-year-graph'), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-by-month-year-graph'), width=12),
    ])
])

# @app.callback(
@callback(
    [Output('card-total-sales', 'children'),
     Output('card-average-sales', 'children'),
     Output('card-num-orders', 'children'),
     Output('card-avg-order-value', 'children'),
     Output('card-profit', 'children'),
     Output('card-profit-margin', 'children')],
    [Input('data-store', 'data'),
     Input('year-selector', 'value'),
     Input('category-selector', 'value'),
     Input('sub-category-selector','value')]
)

def update_metrics(data, value, c_value, sub_c_value):
    df = pd.DataFrame(data)
    df = df[df['year'].isin(value)]
    df = df[df['category'].isin(c_value)]
    df = df[df['sub_category'].isin(sub_c_value)]
    total_sales = df['sales'].sum()
    average_sales = df['sales'].mean()
    num_orders = df['order_id'].nunique()
    avg_order_value = total_sales / num_orders if num_orders > 0 else 0
    total_profit = df['profit'].sum()
    profit_margin = total_profit / total_sales

    return (create_card("Total Sales", total_sales), create_card("Average Sales", average_sales),
            create_card("Number of Orders", num_orders), create_card("Average Order Value", avg_order_value),
            create_card("Total Profit", total_profit), create_card("Profit Margin", profit_margin))

def create_card(title, value):
    # Check if the value is within the range [0,1] (i.e., a percentage)
    if 0 <= value <= 1:
        value = f"{value * 100:.2f}%"  # Display as a percentage
    else:
        value = f"$ {value:,.2f}"  # Display as a currency with commas as thousand separators

    card_content = [
        dbc.CardHeader(html.H5(title)),
        dbc.CardBody(
            [
                # html.H5(title, className="card-title"),
                html.P(value, className="card-text"),
            ],
            style={"text-align": "center"}  # text alignment in the card body
        ),
    ]

    return dbc.Card(card_content, style={"border": "2px solid #333",  # card border
                                         "background-color": "#e9ecef",  # card background color
                                         "margin-top": "10px",  # margin from top
                                         "margin-bottom": "10px", # margin from bottom
                                         "text-align": "center" 
                                         })


# @app.callback(
@callback(
    Output('sales-by-category-graph', 'figure'),
    [Input('data-store', 'data'),
     Input('year-selector', 'value'),
     Input('category-selector', 'value'),
     Input('sub-category-selector','value')]
)

def update_sales_by_category_graph(data, value, c_value, sub_c_value):
    df = pd.DataFrame(data)
    df = df[df['year'].isin(value)]
    df = df[df['category'].isin(c_value)]
    df = df[df['sub_category'].isin(sub_c_value)]
    sales_by_category = df.groupby('category')['sales'].sum()
    fig = px.bar(sales_by_category, x=sales_by_category.index, y=sales_by_category.values, labels={'x':'Category', 'y':'Sales'}, title='Sales by Category')
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#FFFFFF',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='#FFFFFF',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        plot_bgcolor='#161A22',
        paper_bgcolor='#161A22',
        font=dict(color='#FFFFFF')
    )
    return fig

# @app.callback(
@callback(
    Output('sales-by-month-year-graph', 'figure'),
    [Input('data-store', 'data'),
     Input('year-selector', 'value'),
     Input('category-selector', 'value'),
     Input('sub-category-selector','value')]
)
def update_sales_by_month_year_graph(data, value, c_value, sub_c_value):
    df = pd.DataFrame(data)
    df = df[df['year'].isin(value)]
    df = df[df['category'].isin(c_value)]
    df = df[df['sub_category'].isin(sub_c_value)]
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    sales_by_month_year = df.groupby(['year', 'month'])['sales'].sum().reset_index()
    # map the month number to month name
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
                    6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                    11: 'Nov', 12: 'Dec'}

    # create a new column with the month name
    sales_by_month_year['month'] = sales_by_month_year['month'].map(month_map)
    fig = px.line(sales_by_month_year, x='month', y='sales', labels={'x':'Year, Month', 'y':'Sales'}, color='year', title='Sales by Month/Year')
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#FFFFFF',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='#FFFFFF',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        plot_bgcolor='#161A22',
        paper_bgcolor='#161A22',
        font=dict(color='#FFFFFF')
    )
    return fig

# @app.callback(
@callback(
    Output('sales-by-quarter-year-graph', 'figure'),
    [Input('data-store', 'data'),
     Input('year-selector', 'value'),
     Input('category-selector', 'value'),
     Input('sub-category-selector','value')]
)
def update_sales_by_quarter_year_graph(data, value, c_value, sub_c_value):
    df = pd.DataFrame(data)
    df = df[df['year'].isin(value)]
    df = df[df['category'].isin(c_value)]
    df = df[df['sub_category'].isin(sub_c_value)]
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year'] = df['order_date'].dt.year
    df['quarter'] = df['order_date'].dt.quarter
    sales_by_quarter_year = df.groupby(['year', 'quarter'])['sales'].sum().reset_index()
    # map the quarter number to quarter name
    quarter_map = {1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'}

    # create a list of the quarters
    sales_by_quarter_year = sales_by_quarter_year.sort_values(['year', 'quarter'])
    sales_by_quarter_year['quarter'] = sales_by_quarter_year['quarter'].map(quarter_map)
    fig = px.line(sales_by_quarter_year.reset_index(), x='quarter', y='sales', labels={'x':'Year, Quarter', 'y':'Sales'}, color='year', title='Sales by Quarter/Year')
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='#FFFFFF',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='#FFFFFF',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        plot_bgcolor='#161A22',
        paper_bgcolor='#161A22',
        font=dict(color='#FFFFFF')
    )
    return fig
