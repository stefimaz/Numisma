import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

st.set_page_config(page_title='Numisma: Diversify your crypto holdings', layout='wide')
#image = Image.open("./Images/Cryptos.jpeg")
#st.image(image, width=900)
st.title("Numisma. Crypto Index Portfolio Management")

portfolios = ['Metadex Portfolio', 'Ventidex Portfolio', 'Farmdex Portfolio']

st.write("Choose from the available indexes to start you journey into minimizing yout risk")

load_dotenv("api.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
#accounts = w3.eth.accounts
#address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

# Load the contract once using cache
# Connects to the contract using the contract address and ABI

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./Ventidex2_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS2")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi)
    
    return contract

# Load the contract
contract = load_contract()

portfolios = {'Metadex Portfolio': {'Logo':'Images/Ventidex_pie.jpg'}, 'Ventidex Portfolio':{'Logo':'Images/Ventidex_pie.jpg'}, 'Farmdex Portfolio':{'Logo':'Images/Ventidex_pie.jpg'}}

st.header('Ventidex: Composed of the top 10 crypto by market cap')
st.subheader('This particular index was calculated by our proprietary AI')
st.image(portfolios['Ventidex Portfolio']['Logo'], width = 500)

################################################################################
# Buying the portfolio
################################################################################
st.title("Buy This Portfolio")

accounts = w3.eth.accounts

# Use a streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select your wallet", accounts)

# Use a streamlit component to get the contract URI
# contract_uri = st.text_input("The URI to the artwork")

if st.button("Buy Now"):

    # Use the contract to send a transaction to the safeMint function
    tx_hash = contract.functions.safeMint(address).transact({
        "from": address, "gas": 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.success(dict(receipt))
st.markdown("---")