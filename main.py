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
                options=('Select token','ETH','MATIC','SAND'),
                index=0)
    # print(token)
with col2:
    if token == 'Select token':
        start, end = st.slider('Select token first!', 
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2022, 12, 1),
            value=(datetime(2020, 6, 1), datetime(2021, 7, 1)),
            format="YYYY-MM-DD",
            disabled=True)
        st.write('Start date:', start)
        st.write('End date:', end)
    else:
        start, end = st.slider(
            'Select time range',
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2022, 12, 1),
            value=(datetime(2020, 6, 1), datetime(2021, 7, 1)),
            format="YYYY-MM-DD")
        st.write('Start date:', start)
        st.write('End date:', end)
st.header('Price Chart')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current price", "$1,281.66", "10%")
col2.metric("Market Cap", "$156,930,933,370", "9%")
col3.metric("Volume (24h)", "$8,189,875,958", "13%")
col4.metric("Last 7 Days", "picture")
st.image('https://images.theconversation.com/files/380042/original/file-20210121-23-1bblai1.png?ixlib=rb-1.1.0&q=30&auto=format&w=600&h=322&fit=crop&dpr=2', caption=f"{token} price chart", use_column_width=True)

st.header('On-chain Network Visualization')
col1, col2 = st.columns([3, 1])
with col1:
    st.image('https://supplychainbeyond.com/wp-content/uploads/2019/08/supply-chain-network-applications-multi-party-networks-5.jpg', caption='On-chain Network', use_column_width=True)
with col2:
    user_min = st.slider('Adjust MIN value',
                min_value=0,
                max_value=100,
                value=40)