import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
#import plotly.figure_factory as ff

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

st.title('Testing export')

DATE_COLUMN = 'daily'
DATA_URL = ('https://testingmidktbo.s3.amazonaws.com/stagging.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Fetch raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of  by day')

hist_values = np.histogram(data[DATE_COLUMN].dt.day, bins=31, range=(0,31))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
day_to_filter = st.slider('day', 0, 31, 17)
filtered_data = data[data[DATE_COLUMN].dt.day == day_to_filter]

st.subheader('Campaigns at days %d' % day_to_filter)
st.write(filtered_data)

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

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
