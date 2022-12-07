import streamlit as st
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network

#import plotly.graph_objects as go
from datetime import datetime, date, time, timedelta
import requests

token_dict = {"BTC": "bitcoin", "ETH": "ethereum"}

st.title('On-chain Data Visualizer')

st.header('Dashboard')
col1, col2, col3 = st.columns(3)
# Fear and Greed Index
with col1:
    st.image('https://alternative.me/crypto/fear-and-greed-index.png', caption='Fear and Greed Index', use_column_width=True)
# BTC Price
with col2:
    btc_url = f"https://api.coingecko.com/api/v3/coins/{token_dict['BTC']}/market_chart?vs_currency=usd&days=0&interval=daily"
    btc_data = requests.get(btc_url).json()
    btc_price = btc_data['prices'][0][1]
    st.metric("BTC Price", f"${btc_price:,.2f}")
    st.image('https://www.coingecko.com/coins/1/sparkline', caption='Last 7 days BTC Price Chart', use_column_width=True)
# Trending Coins
with col3:
    trending_url = "https://api.coingecko.com/api/v3/search/trending"
    trending_data = requests.get(trending_url).json()
    trending_coins = [x['item']['name'] for x in trending_data['coins']]
    st.write("Trending Coins")
    st.write(trending_coins)

st.header('Choose Token & Time range')

flag = False
with st.form("Choose Token & Date range"):
    # Select token
    st.write("Select token ticker")
    token = st.selectbox('Select token',
                options=('Select token','ETH','MATIC','SAND'),
                index=0, label_visibility='collapsed')
    # Select time range
    # disabled = True if token == 'Select token' else False
    st.write('Select date range (Time Zone: UTC)')
    min_date = date(2020, 1, 1) # modify here
    max_date = date(2021, 12, 31) # modify here
    user_start_date = st.date_input(f'Start date: from {min_date}', min_date, disabled=False)
    user_end_date = st.date_input(f'End date: to {max_date}', min_date + timedelta(days=2), disabled=False)
    date_submitted = st.form_submit_button("Continue")
    if date_submitted:
        if token == 'Select token':
            st.warning('Please select token.')
        elif user_end_date < user_start_date:
            st.warning('End date must fall after start date.')
        elif user_start_date < min_date:
            st.warning('Start date must be after 2020-01-01.')
        elif user_end_date > max_date:
            st.warning('End date must be before 2021-12-31.')
        else:
            flag = True

with st.form("Choose Time range"):
    # disabled = False if (date_submitted and token != 'Select token') else True
    disabled = False if flag else True
    user_start_time, user_end_time = st.slider('Select time range',
        min_value=datetime.combine(user_start_date, time(0, 0)),
        max_value=datetime.combine(user_end_date, time(23, 59)),
        value=(datetime.combine(user_start_date, time(0, 0)), datetime.combine(user_end_date, time(23, 59))),
        format="YYYY-MM-DD HH:mm",
        step=timedelta(minutes=1),
        disabled=disabled)
    time_submitted = st.form_submit_button("Submit")

if time_submitted:
    st.write(f"From: {user_start_date}")
    st.write(f"To: {user_end_date}")

    st.header(f'Real-time {token} Token Metrics')
    col1, col2, col3, col4 = st.columns(4)
    coin_url = f"https://api.coingecko.com/api/v3/coins/{token_dict[token]}/market_chart?vs_currency=usd&days=0&interval=daily"
    coin_data = requests.get(coin_url).json()
    
    token_price = coin_data['prices'][0][1] # if token != "Select token" else 0.00
    token_market_cap = coin_data['market_caps'][0][1] / 1000000 # if token != "Select token" else 0.0
    token_volume = coin_data['total_volumes'][0][1] / 1000000 # if token != "Select token" else 0.0
    col1.metric("Current price", f"${token_price:,.2f}")
    col2.metric("Market Cap", f"${token_market_cap:,.1f}M")
    col3.metric("Volume (24h)", f"${token_volume:,.1f}M")
    with col4:
        img_url = "https://www.coingecko.com/coins/279/sparkline" # this image is for ETH only. Need to change here for each token
        st.image(img_url, caption='Last 7 days Price Chart', use_column_width=True)
    

    st.header('On-chain Network Visualization')
    col1, _ = st.columns(2)
    with col1:
        user_min = st.slider('Adjust MIN value',min_value=0,max_value=100,value=40)
    st.write(user_min)
    # st.image('https://supplychainbeyond.com/wp-content/uploads/2019/08/supply-chain-network-applications-multi-party-networks-5.jpg', caption='On-chain Network', use_column_width=True)
    # # st.plotly_chart()
    df=pd.read_csv('test_data_semi.csv')
    # Save and read graph as HTML file (on Streamlit Sharing)
    form='%Y-%m-%d %H:%M'
    df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d %H:%M')
    user_start=user_start_time
    user_end=user_end_time
    print("STart: ",datetime.datetime64(user_start))
    print("End:",user_end)
    print(df['Date'])
    df_date= df.loc[df['Date'].isin(pd.date_range(user_start,user_end))]

    # df_date= df.loc[df['Date'].isin(pd.date_range(datetime.strftime(user_start,format=form), datetime.strftime(user_end,format=form)))]
    print(df_date)
    df_select = df_date.loc[df_date['Value']>user_min].reset_index(drop=True)
    
    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, source='From', target='To', edge_attr='Value', create_using=nx.MultiGraph())
    d=dict(G.degree)
    scale=10
    #Updating edge weighted degree dict
    d.update((x, scale*y) for x, y in d.items())
        
    #Setting up size attribute
    nx.set_node_attributes(G,d,'size')
        
    # Initiate PyVis network object
    coin_net = Network(height='465px', bgcolor='#222222', font_color='white')

    # Take Networkx graph and translate it to a PyVis graph format
    coin_net.from_nx(G)

    # Generate network with specific layout settings
    coin_net.repulsion(node_distance=420, central_gravity=0.33,
                        spring_length=110, spring_strength=0.10,
                        damping=0.95)

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        coin_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        coin_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)

