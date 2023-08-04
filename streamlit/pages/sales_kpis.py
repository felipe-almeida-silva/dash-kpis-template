import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
# from streamlit_extras.dataframe_explorer import dataframe_explorer ## interesting
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from helper.database import MySQLDatabase

### connect to db and create df
with st.spinner('Getting your data...'):
    # db = MySQLDatabase(host='localhost', user='root', password='', database='kpis_database', port=3306)

    # df_sales = db.dataframe_from_query('select * from orders;')

    df_sales = pd.read_csv('old_sales.csv')


### etl df
# replace column names with lower case and replace space with underscore and - with  underscore
df_sales.columns = df_sales.columns.str.lower()
df_sales.columns = df_sales.columns.str.replace(' ', '_')
df_sales.columns = df_sales.columns.str.replace('-', '_')



# Convert the 'order_date' column to datetime
df_sales['order_date'] = pd.to_datetime(df_sales['order_date'])
# df_sales['ship_date'] = pd.to_datetime(df_sales['ship_date'])

# Convert country, state, city, state, region, category, sub-category, ship_mode to categorical
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
# df_sales['sales'] = df_sales['sales'].str.replace(',', '')
df_sales['sales'] = pd.to_numeric(df_sales['sales'], errors='coerce')
# df_sales['profit'] = df_sales['profit'].str.replace(',', '')
df_sales['profit'] = pd.to_numeric(df_sales['profit'], errors='coerce')


#####
# To do this, first convert 'order_date' to datetime and then extract the month or quarter.
df_sales['year'] = df_sales['order_date'].dt.year
df_sales['month'] = df_sales['order_date'].dt.month
df_sales['quarter'] = df_sales['order_date'].dt.quarter

sales_by_month_year = df_sales.groupby(['year', 'month'])['sales'].sum()
sales_by_month_year = sales_by_month_year.reset_index()
# sort by year then month
sales_by_month_year = sales_by_month_year.sort_values(['year', 'month'])

sales_by_quarter_year = df_sales.groupby(['year', 'quarter'])['sales'].sum()
sales_by_quarter_year = sales_by_quarter_year.reset_index()

# map the month number to month name
month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
                6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                11: 'Nov', 12: 'Dec'}

# create a new column with the month name
sales_by_month_year['month'] = sales_by_month_year['month'].map(month_map)


# map the quarter number to quarter name
quarter_map = {1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'}

# create a list of the quarters
sales_by_quarter_year = sales_by_quarter_year.sort_values(['year', 'quarter'])
sales_by_quarter_year['quarter'] = sales_by_quarter_year['quarter'].map(quarter_map)


# Sidebar
st.sidebar.title('Dashboard Filters')
years = df_sales['year'].unique().tolist()
years.sort()
year_select = st.sidebar.selectbox('Select Year', ['All'] + years, index=len(years))

compare_to_year_select = None
if year_select != 'All':
    years_to_compare = [year for year in years if year != year_select]
    compare_to_year_select = st.sidebar.selectbox('Compare To Year', ['Compare to Itself'] + years_to_compare, index=0)

quarters = df_sales['quarter'].unique().tolist()
quarters.sort()
quarter_select = st.sidebar.multiselect('Select Quarter(s)', quarters, quarters)

categories = df_sales['category'].unique().tolist()
categories.sort()
category_select = st.sidebar.multiselect('Select Category(s)', categories, categories)

# Apply filters
with st.spinner('Applying filters...'):
    if year_select == 'All':
        df_sales_filtered = df_sales
    else:
        print([year_select])
        df_sales_filtered = df_sales[df_sales['year'].isin([year_select])]
        df_sales_filtered = df_sales_filtered[df_sales_filtered['quarter'].isin(quarter_select)]
        df_sales_filtered = df_sales_filtered[df_sales_filtered['category'].isin(category_select)]

# Function to calculate comparison
def calculate_comparison(df, column, year_select, compare_to_year_select, quarter_select, category_select):
    if compare_to_year_select == 'Compare to Itself':
        df_year_select = df[(df['year'] == year_select) & (df['quarter'].isin(quarter_select)) & (df['category'].isin(category_select))]
        df_compare_to_year_select = df_year_select
    else:
        df_year_select = df[(df['year'] == year_select) & (df['quarter'].isin(quarter_select)) & (df['category'].isin(category_select))]
        df_compare_to_year_select = df[(df['year'] == compare_to_year_select) & (df['quarter'].isin(quarter_select)) & (df['category'].isin(category_select))]

    return df_year_select, df_compare_to_year_select


# Main Dashboard
st.title('Sales Dashboard')

# Calculate KPI values and comparisons
total_sales_year_select, total_sales_compare_to_year_select = calculate_comparison(df_sales_filtered, 'sales', year_select, compare_to_year_select, quarter_select, category_select)
total_sales_current = total_sales_year_select['sales'].sum()
total_sales_previous = total_sales_compare_to_year_select['sales'].sum()
total_sales_comparison = total_sales_current - total_sales_previous

average_sales_year_select, average_sales_compare_to_year_select = calculate_comparison(df_sales_filtered, 'sales', year_select, compare_to_year_select, quarter_select, category_select)
average_sales_current = average_sales_year_select['sales'].mean()
average_sales_previous = average_sales_compare_to_year_select['sales'].mean()
average_sales_comparison = average_sales_current - average_sales_previous

num_orders_year_select, num_orders_compare_to_year_select = calculate_comparison(df_sales_filtered, 'sales', year_select, compare_to_year_select, quarter_select, category_select)
num_orders_current = num_orders_year_select['order_id'].nunique()
num_orders_previous = num_orders_compare_to_year_select['order_id'].nunique()
num_orders_comparison = num_orders_current - num_orders_previous

avg_order_year_select, avg_order_compare_to_year_select = calculate_comparison(df_sales_filtered, 'sales', year_select, compare_to_year_select, quarter_select, category_select)
avg_order_value_current = total_sales_current / num_orders_current
avg_order_value_previous = total_sales_previous / num_orders_previous
avg_order_value_comparison = avg_order_value_current - avg_order_value_previous

# # KPIs
st.subheader(f'Key Performance Indicators {str(year_select).replace("[","").replace("]","")}')
col1, col2 = st.columns([4,4])
col1.metric('Total Sales', '$ {:,.2f}'.format(total_sales_year_select['sales'].sum()), '{:,.2f}'.format(total_sales_comparison))
col2.metric('Average Sales', '$ {:,.2f}'.format(average_sales_year_select['sales'].mean()), '{:,.2f}'.format(average_sales_comparison))

col3, col4 = st.columns([4,4])
col3.metric('Average Order Value','$ {:,.2f}'.format(df_sales['sales'].sum() / df_sales['order_id'].nunique()), '{:,.2f}'.format(avg_order_value_comparison))
col4.metric('Number of Orders', num_orders_year_select['order_id'].nunique(), num_orders_comparison)
style_metric_cards(background_color='#2B2B2B')


# Sales by Category
st.subheader('Sales by Category')
fig_category = px.bar(df_sales_filtered.groupby('category')['sales'].sum().reset_index(), x='category', y='sales', labels={'sales': 'Sales ($)'}, title='Sales by Category')
st.plotly_chart(fig_category)

# Sales by Month/Year
st.subheader('Sales by Month/Year')
fig_month = px.line(df_sales_filtered.groupby(['year', 'month'])['sales'].sum().reset_index(), x='month', y='sales', labels={'x': 'Month', 'y': 'Sales ($)'}, color='year', title='Sales by Month/Year')
st.plotly_chart(fig_month)

# Sales by Quarter/Year
st.subheader('Sales by Quarter/Year')
fig_quarter = px.line(df_sales_filtered.groupby(['year', 'quarter'])['sales'].sum().reset_index(), x='quarter', y='sales', labels={'x': 'Quarter', 'y': 'Sales ($)'}, color='year', title='Sales by Quarter/Year')
st.plotly_chart(fig_quarter)

# Add Descriptions
st.markdown("""
This dashboard presents key sales metrics and insights for the selected year(s). Use the filters on the left sidebar to explore the data based on your preferences.
""")
