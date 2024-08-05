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

st.markdown("The dashboard will help with the distribution problems Citi Bike currently faces")


############ IMPORT DATA ############

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)


############ TOP 20 STATIONS ############

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))


fig.update_layout(
    title = 'Top 20 bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)

st.plotly_chart(fig, use_container_width = True)
