import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd


dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

st.title('Testing export')

DATE_COLUMN = 'daily'
DATA_URL = ('https://testingmidktbo.s3.amazonaws.com/adverity-export.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Fetch raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of  by day')

#hist_values = np.histogram(data[DATE_COLUMN].dt.day, bins=24, range=(0,24))[0]
#st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
