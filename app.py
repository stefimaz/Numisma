import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/Compiled/numisma_abi.json')) as f:
        contract_abi = json.load(f)
        
        
    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################

def pin_investment(investor_name, investor_picture):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(investor_name)

    # Build a token metadata file for the image
    token_json = {
        "name": investor_name,
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
st.write("Choose one of the following investment options to learn more")
col1, col2, col3 = st.columns(3)
with col1:
    st.header("FarmDex")
    st.image('./images/farmyield.jpg')
    with st.expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
with col2:
    st.header("MetaDex")
    st.image('./images/metaverse.jpg')
    with st.expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
with col3:
    st.header("VentiDex")
    st.image('./images/venti.jpg')
    with st.expander("See explanation"):
     st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)


    
################################################################################
# Select your Investment
################################################################################
st.markdown("## Let's get started!")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")    

investor_name = st.text_input("Enter the your name")
thematic_portfolio = st.selectbox(
     'Which thematic portfolio would you want more information on?',
     ('FarmDex','MetaDex', 'VentiDex')),
initial_investment = st.text_input("What is your initial investment?")
#picture = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
picture = st.camera_input("Take a picture")

if st.button("Register Investment"):
    investment_ipfs_hash = pin_investment(investor_name, picture)
    investment_uri = f"ipfs://{investment_ipfs_hash}"
    tx_hash = contract.functions.registerInvestment(
        address,
        investor_name,
        str(thematic_portfolio),
        int(initial_investment),
        investment_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{investment_ipfs_hash})")
st.markdown("---")
st.caption('Balloons. Hundreds of them...')


