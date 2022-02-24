import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

st.set_page_config(page_title='Numisma: Diversify your crypto holdings', layout='wide')
st.image("./Images/Cryptos.jpeg")
st.title("Numisma. Crypto Index Portfolio Management")

st.markdown("""
Numisma is a bll bla bla.....
""")

st.sidebar.header('Portfolio selection')

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

load_dotenv("api.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
#accounts = w3.eth.accounts
#address = st.selectbox("Select Account", options=accounts)

# The contracts have to be loaded separately for eack Token index
# Load the contract once using cache
# Connects to the contract using the contract address and ABI
# loading contract fot --------- token index
@st.cache(allow_output_mutation=True)
def load_contract1():

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
contract1 = load_contract1()

# The contracts have to be loaded separately for eack Token index
# loading contract fot --------- token index
def load_contract2():

    # Load the contract ABI
    with open(Path('./Register.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESSArt")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi)
    
    return contract

# Load the contract
contract2 = load_contract2()

# The contracts have to be loaded separately for eack Token index
# loading contract fot --------- token index
def load_contract3():

    # Load the contract ABI
    with open(Path('./VdexAbi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESSVdex")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi)
    
    return contract

# Load the contract
contract3 = load_contract3()


#st.header('Ventidex: Composed of the top 10 crypto by market cap')
#st.subheader('This particular index was calculated by our proprietary AI')


################################################################################
# Buying the portfolio
################################################################################
st.title("Buy This Portfolio")

accounts = w3.eth.accounts

# Use a streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select your wallet", accounts)
amount = st.number_input("How many shares do you want to buy?", min_value=1, value=1, step=1)
# Use a streamlit component to get the contract URI
# contract_uri = st.text_input("The URI to the artwork")

if st.button("Buy Now"):

    # Use the contract to send a transaction to the safeMint function
    tx_hash = contract3.functions.purchase().transact({
        "from": address, "gas": 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write("Congratulation on your purchase, Hereis your Blockchain receipt")
    st.success(dict(receipt))
st.markdown("---")

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################
def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file)

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
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

################################################################################
# Register New Porfolio
################################################################################
st.markdown("## Register Your Portfolio")
artwork_name = st.text_input("Enter the name of your portfolio")
artist_name = st.text_input("Enter your full name")
initial_appraisal_value = st.text_input("Enter the initial investment amount")
#file = portfolios_dict[selected_portfolio]['Logo']
#file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
file = st.camera_input("Picture recording")

if st.button("Register Artwork"):
    # Use the `pin_artwork` helper function to pin the file to IPFS
    artwork_ipfs_hash =  pin_artwork(artwork_name, file)
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    tx_hash = contract2.functions.registerArtwork(
        address,
        artwork_name,
        artist_name,
        int(initial_appraisal_value),
        artwork_uri 
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.success(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
st.markdown("---")


