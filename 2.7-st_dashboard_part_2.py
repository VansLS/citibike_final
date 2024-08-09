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
from PIL import Image
from numerize.numerize import numerize


############ Initial settings for the dashboard ############

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')
st.title ('Citi Bike Strategy Dashboard')

############ Define the sidebar ############
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather conditions and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Summary and recommendations"])


############ IMPORT DATA ############

df = pd.read_csv('reduced_data_to_plot.csv')
top20 = pd.read_csv('top20.csv')
df_linechart = pd.read_csv('linechartdata.csv')


############ DEFINE THE PAGES ############

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the distribution problems Citi Bike currently faces.")
    st.markdown("Since the Covid–19 pandemic, New York residents have found even more merit in bike sharing, creating higher demand. This has led to distribution problems—such as fewer bikes at popular bike stations or stations full of docked bikes, making it difficult to return a hired bike—and customer complaints. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather conditions and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Summary and recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("Kiosk_of_rental_bikes.jpg") #source: https://commons.wikimedia.org/wiki/File:Kiosk_of_rental_bikes.jpg
    st.image(myImage)


############ DUAL AXIS LINE CHART ############

elif page == 'Weather conditions and bike usage':

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    #add traces
    fig1.add_trace(go.Scatter(x=df_linechart['date'], y=df_linechart['number_of_daily_trips'], name='Daily bike rides', line=dict(color='blue')),
    secondary_y=False)
    fig1.add_trace(
    go.Scatter(x=df_linechart['date'], y=df_linechart['TAVG'], name='Daily temperature', line=dict(color='red')),
    secondary_y=True)

    #update the layout
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
    legend=dict(x=0.01, y=0.99),)

    # Set y-axis range for better visualization
    fig1.update_yaxes(range=[0, df_linechart['number_of_daily_trips'].max()*1.1], secondary_y=False)
    fig1.update_yaxes(range=[df_linechart['TAVG'].min()-5, df_linechart['TAVG'].max()+5], secondary_y=True)

    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")



############ TOP 20 STATIONS ############

elif page == 'Most popular stations':

    #create filter on side bard

    with st.sidebar:
        season_filter=st.multiselect(label='Select the season', options = df['season'].unique(),
        default=df['season'].unique())

    df1=df.query('season==@season_filter')

   # Define the total rides
    total_rides = float(df1['start_station_name'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
   
   # Bar chart

    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20filtered = df_groupby_bar.nlargest(20, 'value')
    

    fig = go.Figure(go.Bar(x = top20filtered['start_station_name'], y = top20filtered['value'], marker={'color': top20filtered['value'],'colorscale': 'Blues'}))

    fig.update_layout(
    title = 'Top 20 bike stations in New York filtered by the season. You can change the season selected using the sidebar.',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600)

    st.plotly_chart(fig, use_container_width = True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St. There is a significant difference between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")

############ MAP ############

elif page == 'Interactive map with aggregated bike trips':
    path_to_html = "NewYorkBikeTrips.html"

    st.write("#### Interactive map showing aggregated bike trips in New York")


# Read file and keep in variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()

## Show in web page 
    st.write("#### Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height = 500)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.") 
    st.markdown('The most popular start stations are W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St.')
    st.markdown('When we add the aggregated trips filter as well as the starting stations, we can see that the top 3 most popular stations also account for the routes with more trips.')
    st.markdown("""
    The most common routes (>5,000) are between:
    - W 21 St & 6 Ave and 9 Ave & W 22 St
    - 1 Ave & E 62 St and 1 Ave & E 68 St
    - Central Park North & Adam Clayton Powell Blvd and Central Park & Adam Clayton Powell Blvd
    """)
    st.markdown("These stations appear to be in the vicinity of tourist destinations such as the iconic Flatiron Building, and central park, which might explain greater demand.")

############ SUMMARY AND RECOMMENDATIONS ############

else:
    st.header("Summary and recommendations")
    bikes = Image.open("citibike2.jpg")  #source: https://www.flickr.com/photos/nycstreets/20296919256
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citi Bike should focus on the following objectives moving forward:")
    st.markdown('From May - October, add more bikes to the most popular stations and routes:')
    st.markdown('''
    - W 21 St & 6 Ave 
    - West St & Chambers St 
    - Broadway & W 58 St
    - 1 Ave & E 62 St and 1 Ave & E 68 St
    - Central Park area
    ''')
    st.markdown('This is due to the fact that demand surges during the warmer months, and the top 3 stations also coincide with some of the most popular routes.')
    st.markdown('To further ease the demand within the vicinity of tourist destinations, more bike stations could also be introduced within the area.')
    st.markdown("While more bikes should be added to the popular stations during the warmer months, they should be reduced during the colder months to reduce logistics costs.")