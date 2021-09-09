import streamlit as st
import requests
import json
import subprocess
from datetime import date
import numpy as np
import pandas as pd
#import plotly.figure_factory as ff
#import graphviz as graphviz
######################################################################################################################################
DATE_COLUMN = 'daily'
DATA_URL = ('https://testingmidktbo.s3.amazonaws.com/stagging.csv')
datastreams_id = [6]

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
######################################################################################################################################
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def fetch_ds(datastreams_id):
    for i in datastreams_id:
        url = f'https://KTBO.datatap.adverity.com/api/datastreams/{i}/fetch_fixed/'
        payload = json.dumps({
        "start": "2020-08-01T00:00:00Z",
        "end": "2021-08-06T00:00:00Z"
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token c49e653ffa8a0c80768bbf1af0887905a56fff9b'
        }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    return(response)
######################################################################################################################################

st.title('Adverity usual tasks')

st.dataframe(dataframe.style.highlight_max(axis=0))

st.write('última actualización de kwin')
data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done! (using st.cache)")

if st.button('Raw data'):
    st.subheader('Raw data')
    st.write(data)

options = st.multiselect(
    'What are your platforms do you want to fetch',
    ['Facebook', 'Google', 'Sizmek'],
    ['Facebook'])

st.write('You selected:', options)

st.subheader('Number of records  by day')

st.date_input('Date input')

color = st.select_slider(
    'Select a color of the rainbow',
    options=['A lo grande', 'Chocodilema', 'Komplete', 'Despierta Mucho Mas', 'Freestamp', 'Red City', 'Promo Xbox'])
st.write('Values:', color)

hist_values = np.histogram(data[DATE_COLUMN].dt.day, bins=31, range=(1,31))[0]
st.bar_chart(hist_values)

if st.checkbox(f'Fetch {options} data'):
    response = fetch_ds(datastreams_id)
      
#filtered_data = data[(data['daily'].dt.day).isin(days_range)]
#filtered_data = data[data['initiative' == color]]

#st.subheader('Campaigns at days %d' % day_to_filter)
#st.write(filtered_data)

st.subheader('Sentiment Analysis')

txt = st.text_area('Text to analyze', '''
     It was the best of times, it was the worst of times, it was
     the age of wisdom, it was the age of foolishness, it was
     the epoch of belief, it was the epoch of incredulity, it
     was the season of Light, it was the season of Darkness, it
     was the spring of hope, it was the winter of despair, (...)
     ''')

#st.write('Sentiment:', run_sentiment_analysis(txt))

st.subheader('graph')

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
chart_data = data.groupby(['initiative', 'platform','daily'], as_index=False).mean()
data_sub1 = chart_data[['initiative','platform','daily','platform_cost']]
st.write(data_sub1)
#data_sub1 = data_sub1.groupby('platform', as_index=False).mean()
#data_sub1 = data_sub1[data_sub1['initiative'] == 'A lo grande']
#data_sub1['daily'] = data_sub1['daily'].dt.date
#st.write(data_sub1)

st.bar_chart(np.random.randn(50, 3))

st.line_chart(data_sub1["platform_cost"])
#st.bar_chart(data_sub1)
#st.area_chart(chart_data)
#st.write(subprocess.call('date', shell=True))

