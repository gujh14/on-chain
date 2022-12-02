import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

st.title('On-chain Data Visualizer')

st.header('Dashboard')
col1, col2, col3 = st.columns(3)
with col1:
    # st.subheader('Fear and Greed Index')
    st.image('https://alternative.me/crypto/fear-and-greed-index.png', caption='Fear and Greed Index', use_column_width=True)
# <img src="https://alternative.me/crypto/fear-and-greed-index.png" alt="Latest Crypto Fear & Greed Index" />
st.header('Choose Token & Time range')
col1, col2 = st.columns(2)
with col1:
    token = st.selectbox('Select token',
                ('ETH','Option2','Option3','Option4'))
    # print(token)
with col2:
    if token:
        start, end = st.slider(
            'Select time range',
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2022, 12, 1),
            value=(datetime(2021, 1, 1), datetime(2021, 2, 1)),
            format="YYYY-MM-DD")
        st.write('Start date:', start)
        st.write('End date:', end)
    else:
        st.slider('Select token first!', disabled=True)
st.header('Price Chart')

st.header('On-chain Network Visualization')