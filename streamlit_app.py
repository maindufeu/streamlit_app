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
#datastreams_id = [6,63,101,89,98,97,99]
datastreams_id = []
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
        payload = json.dumps(p)
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
######################################################################################################################################
if st.button('Raw data'):
    st.subheader('Raw data')
    st.write(data)

options = st.multiselect(
    'Which platforms do you want to fetch',
    ['Facebook', 'Google', 'Sizmek SAS - Colombia','Sizmek SAS - Mexico','Sizmek SAS - Miami','Sizmek SAS - Puerto Rico'],
    ['Facebook','Google', 'Sizmek SAS - Colombia','Sizmek SAS - Mexico','Sizmek SAS - Miami','Sizmek SAS - Puerto Rico'])

st.write('You selected:', options)

id_mapping = {'Facebook':6, 'Google':63, 'Sizmek SAS - Colombia':89, 'Sizmek SAS - Mexico':98,'Sizmek SAS - Miami':97,'Sizmek SAS - Puerto Rico':99}

datastreams_id = [id_mapping[x] for x in options]
st.write(datastreams_id)

st.subheader('Number of records  by day')

fetch_sd = st.date_input('Start Date input')

fetch_ed = st.date_input('End Date input')

sd = fetch_sd.strftime('%Y-%m-%dT%H:%M:%SZ')
ed = fetch_ed.strftime('%Y-%m-%dT%H:%M:%SZ')

st.write("start Date:", fetch_sd, 'End Date:', fetch_ed)

p = {}
p['start'] = sd
p['end'] = ed
payload = json.dumps(p)
st.write(str(payload))

if st.checkbox(f'Fetch {options} data from {sd} to {ed}'):
    response = fetch_ds(datastreams_id)
    st.write(response)
######################################################################################################################################
color = st.select_slider(
    'Select an initiative',
    options=['A lo grande', 'Chocodilema', 'Komplete', 'Despierta Mucho Mas', 'Freestamp', 'Red City', 'Promo Xbox'])
st.write('Values:', color)
######################################################################################################################################
hist_values = np.histogram(data[DATE_COLUMN].dt.day, bins=31, range=(1,31))[0]
st.bar_chart(hist_values)
      
#filtered_data = data[(data['daily'].dt.day).isin(days_range)]
#filtered_data = data[data['initiative' == color]]

#st.subheader('Campaigns at days %d' % day_to_filter)
#st.write(filtered_data)

st.subheader('Sentiment Analysis')
######################################################################################################################################
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
######################################################################################################################################
# Create distplot with custom bin_size
chart_data = data.groupby(['initiative', 'platform','daily'], as_index=False).mean()
data_sub1 = chart_data[['initiative','platform','daily','platform_cost']]
st.write(data_sub1)
#data_sub1 = data_sub1.groupby('platform', as_index=False).mean()
#data_sub1 = data_sub1[data_sub1['initiative'] == 'A lo grande']
#data_sub1['daily'] = data_sub1['daily'].dt.date
#st.write(data_sub1)

st.bar_chart(np.random.randn(50, 3))
##########################################################################################################################################
st.line_chart(data_sub1["platform_cost"])
#st.bar_chart(data_sub1)
#st.area_chart(chart_data)
#st.write(subprocess.call('date', shell=True))

