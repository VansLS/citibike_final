############ IMPORT LIBRARIES ############

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

st.set_page_config(page_title = 'New York Bikes Strategy Dashboard', layout='wide')

st.header("The dashboard will help with the distribution problems Citi Bike currently faces")


############ IMPORT DATA ############

df = pd.read_csv('reduced_data_to_plot.csv')
top20 = pd.read_csv('top20.csv')
df_linechart = pd.read_csv('linechartdata.csv')

############ TOP 20 STATIONS ############

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))


fig.update_layout(
    title = 'Top 20 bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)

st.plotly_chart(fig, use_container_width = True)

############ LINE CHART ############

# Create a dual-axis line chart
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig1.add_trace(
    go.Scatter(x=df_linechart['date'], y=df_linechart['number_of_daily_trips'], name='Daily bike rides', line=dict(color='blue')),
    secondary_y=False
)

fig1.add_trace(
    go.Scatter(x=df_linechart['date'], y=df_linechart['TAVG'], name='Daily temperature', line=dict(color='red')),
    secondary_y=True
)

# Update layout to better distinguish the axes
fig1.update_layout(
    title='Daily bike rides and temperature, New York',
    xaxis_title='Date',
    yaxis=dict(
        title='Daily bike rides',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue')
    ),
    yaxis2=dict(
        title='Daily temperature (°F)',
        titlefont=dict(color='red'),
        tickfont=dict(color='red'),
        overlaying='y',
        side='right'
    ),
    width=1000,
    height=600,
    legend=dict(x=0.01, y=0.99),
)

# Set y-axis range for better visualization
fig1.update_yaxes(range=[0, df_linechart['number_of_daily_trips'].max()*1.1], secondary_y=False)
fig1.update_yaxes(range=[df_linechart['TAVG'].min()-5, df_linechart['TAVG'].max()+5], secondary_y=True)

st.plotly_chart(fig1, use_container_width=True)


############ MAP ############
path_to_html = "NewYorkBikeTrips.html"

# Read file and keep in variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()

## Show in web page 
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height = 500)