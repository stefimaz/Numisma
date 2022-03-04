import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import streamlit.components.v1 as components
import requests
import tweepy


from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/Compiled/voice_abi.json')) as f:
        contract_abi = json.load(f)
        
        
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS_VOICE")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Sidebar functions to pin files and json to Pinata
################################################################################


#auth = tweepy.OAuthhandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
#autho.set_access_token(config.TWITER_ACCESS_TOKEN)

#api = tweepy.API(auth)

option = st.sidebar.selectbox("Select Dashboard", ('STOCKTWITS', 'TWITTER'))
st.header(option)
if option == 'STOCKTWITS':
    symbol = st.sidebar.text_input("Symbol", value='nvda', max_chars=5)
    r = requests.get(f"https://api.stockwits.com/api/2/stream/{symbol}/nvda.json")
    data = r.json()
                     
    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])                 
        st.write(message['body'])                    
   
  

if option == 'TWITTER':
    st.subheader("TWITTER DASHBOARD LOGIC")    
    tweets = api.user_timeline("")
st.markdown("---")

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################
def pin_voter(voter_name, voter_pic):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(voter_name)

    # Build a token metadata file for the image
    token_json = {
        "name": voter_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash

def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


st.title("Numisma Investment System")
st.write("Learn about your options")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)

col1, col2, col3 = st.columns(3)
with col1:
    st.header("FarmDex[0]")
    st.image('./images/farmyield.jpg')
    with st.expander("See explanation"):
     st.write("""
         Yield farming is an investment strategy in decentralised finance or DeFi. It involves lending or staking your cryptocurrency coins or tokens to get rewards in the form of transaction fees or interest.
     """)
with col2:
    st.header("MetaDex[1]")
    st.image('./images/metaverse.jpg')
    with st.expander("See explanation"):
     st.write("""
         Metaverse is the technology behind a virtual universe where people can shop, game, buy and trade currencies and objects and more. Think of it as a combination of augmented reality, virtual reality, social media, gaming and cryptocurrencies.
     """)
with col3:
    st.header("VentiDex[2]")
    st.image('./images/venti.jpg')
    with st.expander("See explanation"):
     st.write("""
         Market cap allows you to compare the total value of one cryptocurrency with another so you can make more informed investment decisions. Cryptocurrencies are classified by their market cap into three categories: Large-cap cryptocurrencies, including Bitcoin and Ethereum, have a market cap of more than $10 billion.
     """)

st.markdown("---")
################################################################################
# Your Voice Matters
################################################################################
option = st.sidebar.selectbox("Select Dashboard", ('FarmDex','MetaDex', 'VentiDex'))

if option == 'FarmDex':
    st.subheader("FarmDex Dashboiard Logic")
if option == 'MetaDex':
    st.subheader("MetaDex Dashboiard Logic")    
if option == 'VentiDex':
    st.subheader("VentiDex Dashboiard Logic")    
 
voter = st.text_input("Enter your name")

proposal = st.selectbox(
     'Which thematic appealed to you the most',
     ('FarmDex','MetaDex', 'VentiDex')),

#voter_pic = st.camera_input("Take a picture")

if st.button("Vote"):
    voter_ipfs_hash = pin_voter(voter, voter_pic)
    voter_uri = f"ipfs://{voter_ipfs_hash}"
    tx_hash = contract.functions.vote(
        unit(proposal),
        voter_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{voter_ipfs_hash})")
st.markdown("---")

#########
