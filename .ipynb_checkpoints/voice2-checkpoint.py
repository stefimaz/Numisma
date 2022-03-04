import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
# import streamlit.components.v1 as components
# import requests
import tweepy
import config
from tweepy.auth import OAuthHandler

load_dotenv()
################################################################################
# Set keys
################################################################################

client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

################################################################################
# Display Options
################################################################################


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

# @cz_binance is the founder and CEO of Binance 
# @MMCrypto is one of the world's elite group of traders
# @aantonop is one of the world's foremost trusted educators of Bitcoin

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

   # tweets = client.get_users_tweets(id=id, tweet_fields=['context_annotations','created_at','geo'])
#@st.cache(allow_output_mutation=True)
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
    
#user = client.get_user(username='cz_binance')
#user = client.get_user(username='MMCrypto')
#user = client.get_user(username='aantonop')

# id = username_choice
# tweets = client.get_users_tweets(id=id, tweet_fields=['context_annotations','created_at','geo'])

# for tweet in tweets.data:
#     st.sidebar.write(tweet)

    
    
    
# @cz_binance is the founder and CEO of Binance 
# @MMCrypto is one of the world's elite group of traders
# @aantonop is one of the world's foremost trusted educators of Bitcoin




#cz_binance_tweet = client.get_users_tweets('902926941413453824')
#MMCryto_tweet = client.get_users_tweets('904700529988820992')
#Andreas_tweet = client.get_users_tweets('1469101279')




################################################################################
# Identify top twitter usernames on crytocurrency
################################################################################
# Replace user ID
# id = '902926941413453824'

# users = client.get_users_followers(id=id, user_fields=['profile_image_url'])

# for user in users.data:
#     st.write(user.id)




















# auth = tweepy.OAuthHandler(
#     config.TWITTER_CONSUMER_KEY,
#     config.TWITTER_CONSUMER_SECRET,
#     config.TWITTER_ACCESS_TOKEN,
#     access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET
# )

# api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# client = tweepy.Client(
#     consumer_key=config.TWITTER_CONSUMER_KEY,
#     consumer_secret=config.TWITTER_CONSUMER_SECRET,
#     access_token=config.TWITTER_ACCESS_TOKEN,
#     access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET
# )

# client = tweepy.Client(bearer_token=config.TWITTER_BEARER_TOKEN)

# option = st.sidebar.selectbox("Select Dashboard", ('TWITTER','STOCKTWITS'))
# st.header(option)  
# user = client.get_user(username='cz_binance')
# user

# cz_binance_tweet = client.get_users_tweets('902926941413453824')

# st.write(cz_binance_tweet)

# Replace with your own search query
# query = 'covid -is:retweet'

# tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
#                                      user_fields=['profile_image_url'], expansions='author_id', max_results=100)

# # Get users list from the includes object
# users = {u["id"]: u for u in tweets.includes['users']}

# for tweet in tweets.data:
#     if users[tweet.author_id]:
#         user = users[tweet.author_id]
#         print(user.profile_image_url)


# auth = tweepy.OAuthhandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
# autho.set_access_token(config.TWITER_ACCESS_TOKEN, config.TWITER_ACCESS_TOKEN_SECRET)


# api = tweepy.API(auth)


# if option == 'TWITTER':
#     for username in config.TWITTER_USERNAMES:
#         st.subheader("TWITTER DASHBOARD LOGIC")    
#         user = api.get_user(username)

#         tweets = api.user_timeline("username")

#         st.image(user.profile_image_url)

#         for tweet in tweets:
#             if '$' in tweet.text:
#                 words=tweet.text.split('')
#                 for words in words:
#                     if word.startswith('$') and word[1:].isalpha():  
#                         symbol = word[1:]
#                         st.write(symbol)
#                         st.write(tweet.text)
#                         st.image(f"https://finviz.com/chart.ashx?t={symbol}")

# if option == 'STOCKTWITS':
#     symbol = st.sidebar.text_input("Symbol", value='nvda', max_chars=5)
#     r = requests.get(f"https://api.stockwits.com/api/2/stream/{symbol}/nvda.json")
#     data = r.json()
                     
#     for message in data['messages']:
#         st.image(message['user']['avatar_url'])
#         st.write(message['user']['username'])
#         st.write(message['created_at'])                 
#         st.write(message['body'])                                    