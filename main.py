import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from datetime import datetime, date, time, timedelta
import requests

token_dict = {"BTC": "bitcoin", "ETH": "ethereum"}

st.title('On-chain Data Visualizer')

st.header('Dashboard')
col1, col2, col3 = st.columns(3)
with col1:
    st.image('https://alternative.me/crypto/fear-and-greed-index.png', caption='Fear and Greed Index', use_column_width=True)

with col2:
    btc_url = f"https://api.coingecko.com/api/v3/coins/{token_dict['BTC']}/market_chart?vs_currency=usd&days=0&interval=daily"
    btc_data = requests.get(btc_url).json()
    btc_price = btc_data['prices'][0][1]
    st.metric("BTC Price", f"${btc_price:,.2f}")
    st.image('https://www.coingecko.com/coins/1/sparkline', caption='Last 7 days BTC Price Chart', use_column_width=True)
with col3:
    trending_url = "https://api.coingecko.com/api/v3/search/trending"
    trending_data = requests.get(trending_url).json()
    trending_coins = [x['item']['name'] for x in trending_data['coins']]
    st.write("Trending Coins")
    st.write(trending_coins)

st.header('Choose Token & Time range')
col1, col2 = st.columns(2)
with col1:
    token = st.selectbox('Select token',
                options=('Select token','ETH','MATIC','SAND'),
                index=0)
    # print(token)
with col2:
    disabled = True if token == 'Select token' else False
    st.write('Time Zone: UTC')
    st.write('Select date range')
    min_date = datetime(2020, 1, 1) # modify here
    max_date = datetime(2021, 1, 1) # modify here
    user_start = st.date_input('Start date', min_date, disabled=disabled)
    user_end = st.date_input('End date', min_date + timedelta(days=2), disabled=disabled)
    # warning if user_end < user_start
    if user_end < user_start:
        st.warning('End date must fall after start date.')
        flag = False
    else:
        flag = True
    user_start, user_end = st.slider('Select time range',
        min_value=datetime.combine(user_start, time(0, 0)),
        max_value=datetime.combine(user_end, time(23, 59)),
        value=(datetime.combine(user_start, time(0, 0)), datetime.combine(user_end, time(23, 59))),
        format="YYYY-MM-DD HH:mm",
        disabled=not (not disabled and flag))
    
    st.write('From:', user_start)
    st.write('To:', user_end)

if token == "Select token":
    st.header('Token Price Info')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current price", f"${0.00}")
    col2.metric("Market Cap", f"${0.0}M")
    col3.metric("Volume (24h)", f"${0.0}M")
    with col4:
        st.image('https://www.coingecko.com/coins/1/sparkline', caption='Last 7 days Price Chart', use_column_width=True)
else:
    st.header(f'{token} Price Info')
    col1, col2, col3, col4 = st.columns(4)
    coin_url = f"https://api.coingecko.com/api/v3/coins/{token_dict[token]}/market_chart?vs_currency=usd&days=0&interval=daily"
    coin_data = requests.get(coin_url).json()

    price = coin_data['prices'][0][1]
    market_cap = coin_data['market_caps'][0][1] / 1000000
    volume = coin_data['total_volumes'][0][1] / 1000000

    col1.metric("Current price", f"${price:,.2f}")
    col2.metric("Market Cap", f"${market_cap:,.1f}M")
    col3.metric("Volume (24h)", f"${volume:,.1f}M")
    with col4:
        st.image("https://www.coingecko.com/coins/279/sparkline", caption='Last 7 days Price Chart', use_column_width=True)

st.header('On-chain Network Visualization')
col1, _ = st.columns(2)
with col1:
    user_min = st.slider('Adjust MIN value',
                min_value=0,
                max_value=100,
                value=40)
st.image('https://supplychainbeyond.com/wp-content/uploads/2019/08/supply-chain-network-applications-multi-party-networks-5.jpg', caption='On-chain Network', use_column_width=True)
# st.plotly_chart()
st.write(user_min)