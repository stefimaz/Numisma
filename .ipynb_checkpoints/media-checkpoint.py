import os
import requests
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Any, List
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
from datetime import datetime
from datetime import date
#Library - Project3 
import CryptoDownloadData as coinData
import CryptoPerfSummary as coinAnalytic
import EfficientFrontierCalculator as ef
import get_index_data as gp

import cufflinks as cf
import sqlalchemy as sql
from pathlib import Path
from st_aggrid.shared import JsCode

import tweepy
import config
from tweepy.auth import OAuthHandler

load_dotenv()

################################################################################
# Set keys
################################################################################

client = tweepy.Client(
#     consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
#     consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
#     access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
#     access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
)

st.title("Numisma Investment System")
st.write("Learn about your options")
col1, col2, col3 = st.columns(3)
with col1:
    st.header("FarmDex")
    st.image('./images/farmyield.jpg')
    with st.expander("See explanation"):
     st.write("""
         Yield farming is an investment strategy in decentralised finance or DeFi. It involves lending or staking your cryptocurrency coins or tokens to get rewards in the form of transaction fees or interest.
     """)
with col2:
    st.header("MetaDex")
    st.image('./images/metaverse.jpg')
    with st.expander("See explanation"):
     st.write("""
         Metaverse is the technology behind a virtual universe where people can shop, game, buy and trade currencies and objects and more. Think of it as a combination of augmented reality, virtual reality, social media, gaming and cryptocurrencies.
     """)
with col3:
    st.header("VentiDex")
    st.image('./images/venti.jpg')
    with st.expander("See explanation"):
     st.write("""
         Market cap allows you to compare the total value of one cryptocurrency with another so you can make more informed investment decisions. Cryptocurrencies are classified by their market cap into three categories: Large-cap cryptocurrencies, including Bitcoin and Ethereum, have a market cap of more than $10 billion.
     """)

st.markdown("---")

################################################################################
# Identify top twitter usernames on crytocurrency
################################################################################

popular_twitter_usernames = ("metaversenoir","cz_binance", "mmcrypto", "aantonop")

username_choice = st.sidebar.selectbox("SELECT POPULAR TWITTER USERNAMES", (popular_twitter_usernames))



metaversenoir = '1450997150477815808'
cz_binance = '902926941413453824'
mmcrypto = '904700529988820992'
aantonop = '1469101279'       

if username_choice == 'metaversenoir':
    id = metaversenoir
    summary = '@metaversenoir is the Genius Behind the Best Metaverse Twitter Thread'
if username_choice == 'cz_binance':
    id = cz_binance
    summary = '@cz_binance is the founder and CEO of Binance'
if username_choice == 'mmcrypto':
    id = mmcrypto
    summary = '@MMCrypto is one of the elite group of traders in the world'
if username_choice == 'aantonop':
    id = aantonop
    summary = '@aantonop is one of the foremost trusted educators of Bitcoin in the world'

# for tweet in tweets.data:
st.sidebar.write(summary)

    
st.title(f'@{username_choice}')    
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Top Twitter")
    st.image('./images/twitter.jpg')
    tweets = client.get_users_tweets(id=id, tweet_fields=['context_annotations','created_at','geo'])
    with st.expander("See Tweets"):
     for tweet in tweets.data:
        st.write(tweet)
with col2:
    st.header("Likes")
    st.image('./images/like.jpg')
    tweets = client.get_liked_tweets(id=id, tweet_fields=['context_annotations','created_at','geo'])
    with st.expander("See Liked Tweets"):
     for tweet in tweets.data:
        st.write(tweet)
with col3:
    st.header("Followers")
    st.image('./images/followers.jpg')
    users = client.get_users_followers(id=id, user_fields=['profile_image_url'])
    with st.expander("See List of Potential Clients"):
     for user in users.data:
        st.write(user.name)

        st.markdown("---")