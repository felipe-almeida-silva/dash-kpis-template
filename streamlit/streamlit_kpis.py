import streamlit as st

# Add a title and description
st.title('Sales Dashboard App')
st.write('Welcome to the Sales Dashboard App! This dashboard provides key sales metrics and insights for your business.')

# Add images or GIFs
st.image('https://cdn.pixabay.com/photo/2018/05/18/16/25/statistics-3411473_1280.jpg', use_column_width=True, caption='Image 1')
st.image('https://cdn.pixabay.com/photo/2021/05/11/17/21/charts-6246450_1280.png', use_column_width=True, caption='Image 2')

# Add a brief explanation
st.write('This app allows you to explore and visualize your sales data. Use the filters on the left sidebar to select the years you want to analyze. The dashboard will display key performance indicators (KPIs) such as total sales, average sales, number of orders, and average order value. You can also view sales trends by month/year and quarter/year, as well as sales breakdown by product categories.')

# Add some highlights or important points
st.markdown('### Key Features:')
st.write('1. Interactive Dashboard: Easily explore and visualize your sales data.')
st.write('2. Performance Comparison: Compare metrics with the previous period to track progress.')
st.write('3. Sales Insights: Analyze sales trends, categories, and customer behavior.')

# Add a call-to-action
# st.markdown('### Get Started:')
# st.write('1. Upload your sales data in CSV format.')
# st.write('2. Open the sidebar and select the years you want to analyze.')
# st.write('3. Explore the dashboard and gain valuable insights into your sales performance!')

# Add a footer
st.markdown('---')
st.write('Created by MOAT AI')
