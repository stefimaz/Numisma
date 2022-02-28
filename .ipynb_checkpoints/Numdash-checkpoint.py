iimport os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Any, List
import streamlit as st
from PIL import Image

from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Account
from web3 import middleware

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
load_dotenv("api.env")

st.set_page_config(page_title='Numisma: Diversify your crypto holdings', layout='wide')

accounts = w3.eth.accounts 

def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether

# The contracts have to be loaded separately for eack Token index
# Load the contract once using cache
# Connects to the contract using the contract address and ABI
# loading contract fot --------- token index
@st.cache(allow_output_mutation=True)

def load_contract():

    # Load the contract ABI
    with open(Path('./Token_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi)
    
    return contract

# Load the contract
contract = load_contract()

share_detail_m = "BTC, ETH"

portfolio_database = {
    "Metadex": ["Metadex","MTX", contract, "1ETH/Share", 1, "Images/Metadex_pie.jpeg"],
    "Ventidex": ["Ventidex","VTX", contract, "1ETH/Share", 1, "Images/Ventidex_pie.jpeg"],
    "Farmdex": ["Farmdex","FMX", "0x8fD00f170FDf3772C5ebdCD90bF257316c69BA45","1ETH/Share", 1, "Images/Farmdex_pie.jpeg"]
}
portfolio = ["Metadex", "Ventidex", "Farmdex"]

st.title("Numisma. Crypto Index Portfolio Management")

st.sidebar.header('Portfolio selection')

portfolio_choice = st.sidebar.selectbox('Select an Index', portfolio)


##################################################################################

portfolios_dict = {'Metadex Portfolio': {'Logo':'Images/Metadex_pie.jpg', 'Description':'The Metaverse Index is designed to capture the trend of entertainment, sports and business shifting to a virtual environment.', 'Creation':'For this Index Weight Calculation, we uses a combination of root market cap and liquidity weighting to arrive at the final index weights. We believe that liquidity is an important consideration in this space and should be considered when determining portfolio allocation.'}, 'Ventidex Portfolio':{'Logo':'Images/Ventidex_pie.jpg', 'Description':'', 'Creation':''}, 'Farmdex Portfolio':{'Logo':'Images/Farmdex_pie.jpg', 'Description':'', 'Creation':''}}

sorted_portfolio = ['Metadex Portfolio', 'Ventidex Portfolio', 'Farmdex Portfolio']

selected_portfolio = st.sidebar.selectbox("Available Portfolio", sorted_portfolio)

st.subheader('Current Portfolio Selection: ' + selected_portfolio)
st.image(portfolios_dict[selected_portfolio]['Logo'], width = 500)

st.subheader(" ")
st.header(f"{selected_portfolio}' Porfolio Description")
st.write(portfolios_dict[selected_portfolio]['Description'])

st.header(f"{selected_portfolio}' Creation strategy")
st.write(portfolios_dict[selected_portfolio]['Creation'])

st.markdown("---")


################################################################################
# Buying the portfolio
################################################################################
st.title("Buy This Portfolio")

# accounts = w3.eth.accounts 

# Use a streamlit component to get the address of the user
address = st.selectbox("Select your wallet", accounts)

balance = get_balance(w3, address)
st.subheader(f'You have ETH: {balance:.3f} in this wallet')

amount = st.number_input("How many shares do you want to buy?", min_value=1, value=1, step=1)
st.subheader(f"You have selected {amount} shares")

st.markdown(f" You will get Total {share_detail_m} for each share")

share_price = portfolio_database[portfolio_choice][4]
cost = share_price * amount
st.write(f'Your total is {cost} ETH')

if st.button("Buy Now"):
    # Use the contract to send a transaction to the purchase function
    tx_hash = contract.functions.purchase(address, cost).transact({
        "from": address, "gas": 1000000})

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.success(dict(receipt))
st.markdown("---")


################################################################################
# Helper functions to pin files and json to Pinata
################################################################################
def pin_artwork(index_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file)

    # Build a token metadata file for the artwork
    token_json = {
        "name": index_name,
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

###############################################################################
# Contract for NFT to register the Shares
###############################################################################
# The contracts have to be loaded separately for eack Token index
# loading contract fot --------- token index
def load_contract_art():

    # Load the contract ABI
    with open(Path('./Register.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS_ART")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi)
    
    return contract

# Load the contract
contract_art = load_contract_art()

################################################################################
# Register New Porfolio
################################################################################
st.markdown("## Register Your Portfolio")
index_name = st.text_input("Enter the name of your portfolio")
holder_name = st.text_input("Enter your full name")
initial_appraisal_value = st.text_input("Enter the initial investment amount")
#file = portfolios_dict[selected_portfolio]['Logo']
#file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"]) ## have to have the getvalue() function in pin_artwork
file = st.camera_input("Picture recording")

if st.button("Register Index Portfolio"):
    # Use the `pin_artwork` helper function to pin the file to IPFS
    artwork_ipfs_hash =  pin_artwork(index_name, file)
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    tx_hash = contract_art.functions.registerArtwork(
        address,
        index_name,
        holder_name,
        int(initial_appraisal_value),
        artwork_uri 
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.success(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display my Token")

#selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(address).call()

# st.write(f"This address owns {tokens} tokens")

# token_id = st.selectbox("Index Portfolio Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner =  contract_art.functions.ownerOf(tokens).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    
    token_uri =  contract.functions.tokenURI(tokens).call()

   # st.write(f"The tokenURI is {token_uri}")
   # st.image(token_uri)
