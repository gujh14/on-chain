import streamlit as st
import streamlit.components.v1 as components

import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network

import plotly.graph_objects as go
import datetime as dt
import requests
import time

from data import get_data, getDateRange, getWhaleData

import san
san.ApiConfig.api_key = "5eltgwflu5h23c3v_f2ky7f3nxsufx2m4"

ticker2name = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "UNI": "uniswap",
    "LINK": "chainlink",
    "AXS": "axie-infinity"
    }
ticker2imgurl = {
    "BTC": "https://www.coingecko.com/coins/1/sparkline", 
    "ETH": "https://www.coingecko.com/coins/279/sparkline", 
    "UNI": "https://www.coingecko.com/coins/12504/sparkline", 
    "LINK": "https://www.coingecko.com/coins/877/sparkline", 
    "AXS": "https://www.coingecko.com/coins/13029/sparkline",
    }
st.set_page_config(layout="wide", page_title="Real-time On-chain Data Visualizer", page_icon="📈")
st.title('📈 Real-time On-chain Data Visualizer')

@st.cache
def call_fear_greed_data():
    # api call
    fear_greed_url = "https://api.alternative.me/fng/"
    fear_greed_data = requests.get(fear_greed_url).json()
    return fear_greed_data

@st.cache
def call_btc_data():
    # api call
    btc_url = f"https://api.coingecko.com/api/v3/coins/{ticker2name['BTC']}/market_chart?vs_currency=usd&days=0&interval=daily"
    btc_data = requests.get(btc_url).json()
    return btc_data

@st.cache
def call_trending_data():
    # api call
    trending_url = "https://api.coingecko.com/api/v3/search/trending"
    trending_data = requests.get(trending_url).json()
    return trending_data

@st.cache
def call_coin_data(token):
    coin_url = f"https://api.coingecko.com/api/v3/coins/{ticker2name[token]}/market_chart?vs_currency=usd&days=0&interval=daily"
    coin_data = requests.get(coin_url).json()
    return coin_data

@st.cache
def call_ohlc_data(token, from_date, to_date, interval):
    ohlc_data = san.get(
        "ohlc", slug=f"{ticker2name[token]}", from_date=from_date, to_date=to_date, interval=interval
    )
    return ohlc_data

st.header('Dashboard')
col1, col2, col3 = st.columns(3)
# Fear and Greed Index
with col1:
    # st.image('https://alternative.me/crypto/fear-and-greed-index.png', caption='Fear and Greed Index', use_column_width=True)
    fg_data = call_fear_greed_data()
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        value=int(fg_data['data'][0]['value']),
        mode="gauge+number",
        title={'text': f"Now: {fg_data['data'][0]['value_classification']}"},
        # min = 0, max = 100 with color gradient
        gauge = {'axis': {'range': [0, 100]},
                    'bar': {'color': "black"},
                    'steps' : [
                        {'range': [0, 20], 'color': "red"},
                        {'range': [20, 40], 'color': "orange"},
                        {'range': [40, 60], 'color': "yellow"},
                        {'range': [60, 80], 'color': "lightgreen"},
                        {'range': [80, 100], 'color': "green"}],
        }
    ))
    # adjust size
    fig.update_layout(
        autosize=False, width=300, height=300
    )
    st.write('Fear and Greed Index')
    st.plotly_chart(fig, use_container_width=True)
# BTC Price
with col2:
    st.write("Bitcoin")
    btc_data = call_btc_data()
    btc_price = btc_data['prices'][0][1]
    st.metric("Current Price", f"${btc_price:,.2f}")
    st.image('https://www.coingecko.com/coins/1/sparkline', caption='Last 7 days BTC Price Chart', use_column_width=True)
# Trending Coins
with col3:
    trending_data = call_trending_data()
    trending_coins = [x['item']['name'] for x in trending_data['coins']]
    st.write("Trending Coins")
    st.write(trending_coins)
    

st.header('Choose Token')
token = st.selectbox('Select token ticker',
                options=('ETH','UNI','LINK','AXS'),
                index=0)
if token != st.session_state.get('token', None):
    if 'start_time' in st.session_state:
        del st.session_state['start_time']
    if 'end_time' in st.session_state:
        del st.session_state['end_time']
    st.session_state['token'] = token

st.header(f'Real-time {token} Token Metrics')
col1, col2, col3, col4 = st.columns(4)
coin_data = call_coin_data(token)

token_price = coin_data['prices'][0][1] ## if token != "Select token" else 0.00
token_market_cap = coin_data['market_caps'][0][1] / 1000000 ## if token != "Select token" else 0.0
token_volume = coin_data['total_volumes'][0][1] / 1000000 ## if token != "Select token" else 0.0
col1.metric("Current Price", f"${token_price:,.2f}")
col2.metric("Market Cap", f"${token_market_cap:,.1f}M")
col3.metric("Volume (24h)", f"${token_volume:,.1f}M")
with col4:
    img_url = ticker2imgurl[token]
    st.image(img_url, caption='Last 7 days Price Chart', use_column_width=True)

min_date, max_date = getDateRange(token)

ohlc_data = call_ohlc_data(token, str(min_date), str(max_date + dt.timedelta(days=1)), "1d")
ohlc_fig = go.Figure(data=[go.Candlestick(x=ohlc_data.index, open=ohlc_data['openPriceUsd'], high=ohlc_data['highPriceUsd'], low=ohlc_data['lowPriceUsd'], close=ohlc_data['closePriceUsd'])])
ohlc_fig.update_layout(xaxis_rangeslider_visible=True, title=f'{token} Price Chart from {min_date} to {max_date}')
st.plotly_chart(ohlc_fig, use_container_width=True)

# modify here ?
threshold = 1000
if token == "ETH":
    threshold = 10000
elif token == "LINK":
    threshold = 100
else:
    threshold = 10000

whale_data = getWhaleData(token, from_date=min_date, to_date=max_date + dt.timedelta(days=1), interval=dt.timedelta(days=1), threshold=threshold)
# whale_data = ohlc_data
whale_fig = go.Figure(data=[go.Scatter(x=whale_data.index, y=whale_data['count'], mode='lines')])
whale_fig.update_layout(xaxis_rangeslider_visible=True, title=f'{token} Whale Transactions from {min_date} to {max_date}')
st.plotly_chart(whale_fig, use_container_width=True)

st.header('Choose Datetime range')
with st.form("Choose Date range"):
    # Select date range
    st.write('Select date range (Time Zone: UTC)')
    
    user_start_date = st.date_input(f'Start date: available from {min_date}', min_date, disabled=False)
    user_end_date = st.date_input(f'End date: available until {max_date}', min_date + dt.timedelta(days=2), disabled=False)
    date_submitted = st.form_submit_button("Continue")
    if date_submitted:
        if user_end_date < user_start_date:
            st.warning('End date must fall after start date.')
        elif user_start_date < min_date:
            st.warning(f'Start date must be after {min_date}.')
        elif user_end_date > max_date:
            st.warning(f'End date must be before {max_date}.')

with st.form("Choose Time range"):
    # Select time range
    st.write('Select time range')
    disabled = False if date_submitted else True
    user_start_time, user_end_time = st.slider('Select time range',
        min_value=dt.datetime.combine(user_start_date, dt.time(0, 0)),
        max_value=dt.datetime.combine(user_end_date, dt.time(23, 59)),
        value=(dt.datetime.combine(user_start_date, dt.time(0, 0)), dt.datetime.combine(user_end_date, dt.time(23, 59))),
        format="YYYY-MM-DD HH:mm",
        step=dt.timedelta(minutes=1),
        disabled=disabled)
    time_submitted = st.form_submit_button("Submit")

    if time_submitted:
        st.session_state['start_time'] = user_start_time
        st.session_state['end_time'] = user_end_time

# if 'config' in st.session_state and st.session_state['config'] != None:
#     st.success("Done!")
# with st.spinner("Analyzing data..."):
#     time.sleep(1)

st.header('On-chain Network Visualization')

if 'start_time' in st.session_state and st.session_state['start_time'] != None:
    token = st.session_state['token']
    user_start_time = st.session_state['start_time']
    user_end_time = st.session_state['end_time']

    st.text(f"On-chain Network of {token} from {user_start_time} to {user_end_time} (UTC)")

    min_value = 0
    max_value = 0
    if token == 'ETH':
        min_value = 10000
        max_value = 30000
    elif token == 'LINK':
        min_value = 100
        max_value = 1000
    else:
        min_value = 1000
        max_value = 10000

    user_min = st.slider('Adjust MIN value',min_value=min_value,max_value=max_value,value=min_value) # need to modify

    # if token != "Select token":

    df = get_data(token, str(user_start_time), str(user_end_time), user_min, 50)

    G = nx.from_pandas_edgelist(df, source='From', target='To', edge_attr='Value', create_using=nx.MultiGraph())
    edge_info=nx.get_edge_attributes(G,'Value')
    nx.set_node_attributes(G, 0, 'size')
    nx.set_node_attributes(G, 0, 'color')
    volume={}
    title={}
    for i in (G.nodes().keys()):
        volume[i]={}
        volume[i]['neighbor']=[]
        volume[i]['amount']=[]
        #|In value|-|Out Value| 담는 부분
        volume[i]['adj']=[]

        title[i]=''

    edge_data=[]
    for edge in G.edges():
        e=list(edge)
        e.append(0)
        e=tuple(e)
        # To set node size corresponding to weights
        G.nodes[edge[0]]['size']+=edge_info[e]
        G.nodes[edge[1]]['size']+=edge_info[e]
        #각 노드의 이웃에 대한 정보
        if(edge[1] not in volume[edge[0]]['neighbor']):
            volume[edge[0]]['neighbor'].append(edge[1])
            volume[edge[0]]['amount'].append(edge_info[e])
            volume[edge[0]]['adj']=-edge_info[e]
        else:
            idx=volume[edge[0]]['neighbor'].index(edge[1])
            volume[edge[0]]['amount'][idx]+=edge_info[e]
            volume[edge[0]]['adj']=edge_info[e]
        if(edge[0] not in volume[edge[1]]['neighbor']):
            volume[edge[1]]['neighbor'].append(edge[0])
            volume[edge[1]]['amount'].append(edge_info[e])
            volume[edge[1]]['adj']=edge_info[e]
        else:
            idx=volume[edge[1]]['neighbor'].index(edge[0])
            volume[edge[1]]['amount'][idx]+=edge_info[e]
            volume[edge[1]]['adj']+=edge_info[e]
        edge_data.append(edge_info[e])


    #Normlization for node size
    node_size=nx.get_node_attributes(G,'size')

    data=list(nx.get_node_attributes(G,'size').values())
    norm_size= [(float(i)-min(data))/(max(data)-min(data)) for i in data]

    #Normalize for edge width
    width={}
    norm_edge= [(float(i)-min(edge_data))/(max(edge_data)-min(edge_data)) for i in edge_data]


    #Normalization for node color
    color={}
    adj_data=[]
    for i in volume.keys():
        adj_data.append(volume[i]['adj'])
    norm_adj=[(float(i)-min(adj_data))/(max(adj_data)-min(adj_data)) for i in adj_data]

    #Code RGB to 16hex
    def base10Tobase16(i):
        base16 = "%02X" % int(i)
        return base16
    def rgb2hex(r, g, b):
        hex_color = "#" + base10Tobase16(r) + base10Tobase16(g) + base10Tobase16(b)
        return hex_color

    #node size, color, width dictionary generation
    for i in range(len(list(volume.keys()))):
        node_size[list(volume.keys())[i]]=norm_size[i]*100
        #들어온 값이 많을수록 초록 # check here!
        color[list(volume.keys())[i]]=rgb2hex(255-norm_adj[i]*255,norm_adj[i]*255,80)

    for k in (list(edge_info.keys())):
        e_idx=list(edge_info.keys()).index(k)
        width[k]=norm_edge[e_idx]*50

    for i in (G.nodes().keys()):
        argsort = np.argsort(volume[i]['amount'])[::-1]
        volume[i]['amount'] = list(np.array(volume[i]['amount'])[argsort])
        volume[i]['neighbor'] = list(np.array(volume[i]['neighbor'])[argsort])

    for i in volume.keys():
        tops="Tops Transaction Neighbors"
        amount_s="Amount"
        title[i]+="{:-<90}".format("-")+"\n"+" .   |"+'{0:=^42}'.format(tops)+"|"f"{amount_s:=^16}\n"+"{:-<90}".format("-")+"\n"
        for j in range(len(volume[i]['neighbor'])):
            if(j<5):
                title[i]+=str(j+1)+" |  "+f"{volume[i]['neighbor'][j]:<50}"+'  |   '
                title[i]+=f"{str(volume[i]['amount'][j]):^30}"+"\n"
        
    #Setting up size attribute
    nx.set_node_attributes(G,node_size,'size')
    nx.set_node_attributes(G,title,'title')
    nx.set_edge_attributes(G,width,'weight')
    nx.set_node_attributes(G,color,'color')
    nx.set_edge_attributes(G,'gray','color')

    # Initiate PyVis network object
    coin_net = Network(height='1000px', bgcolor='#111111', font_color='white')

    # Take Networkx graph and translate it to a PyVis graph format
    coin_net.from_nx(G)

    # Generate network with specific layout settings
    coin_net.repulsion(node_distance=500, central_gravity=0.5,
                            spring_length=300, spring_strength=0.10,
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
    components.html(HtmlFile.read(), height=700)

