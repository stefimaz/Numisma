import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
#from st_aggrid import AgGrid
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
from datetime import datetime
#Library - Project3 
import CryptoDownloadData as coinData
import CryptoPerfSummary as coinAnalytic
import EfficientFrontierCalculator as ef

import sqlalchemy as sql
from pathlib import Path
from st_aggrid.shared import JsCode

# ... 

cellsytle_jscode = JsCode(
    """
function(params) {
    if (params.value < 0) {
        return {
            'color': 'white',
            'backgroundColor': 'darkred'
        }
    } else if (isNaN(params.value)){
        return {
            'color': 'black',
            'backgroundColor': 'dark'
        }
    } else {
        return {
            'color': 'white',
            'backgroundColor': 'green'
        }
    }
};
"""
)

celltwodecimal = JsCode(
    """
function(params) { return {((params).toFixed(2))}}; 
"""

)

st.set_page_config(page_title="Numisma", layout="wide") 
st.title('Numisma: Diversify your crypto holdings')
px_strat = coinData.get_base_pxchanges_matrix()
gb = GridOptionsBuilder.from_dataframe(px_strat)
gb.configure_pagination()
gb.configure_side_bar()
#gb.configure_column("1 Day", cellStyle=cellsytle_jscode, type=["numericColumn","numberColumnFilter"], valueFormatter=(px_strat. .percentage_column_b*100).toFixed(1)+'%'))
#gb.configure_column("Cur_PX", header_name='Cur Px', valueFormatter="(x).toFixed(2)", type=["numericColumn","numberColumnFilter"])
#gb.configure_column("1_Day", cellStyle=cellsytle_jscode, header_name='1 Day', valueFormatter="(x).toFixed(2)", type=["numericColumn","numberColumnFilter"])

#gb.configure_column("1_Day", cellStyle=cellsytle_jscode, #header_name='1 Day', valueFormatter=celltwodecimal, type=#["numericColumn","numberColumnFilter"])





#, valueFormatter="(px_strat.1_Day*100).toFixed(1)+'%'), aggFunc='sum')

#"
#valueFormatter="px_strat.1_Day.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})"

gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
#gridOptions = gb.build()
gridOptions = {
    # enable Master / Detail
    "masterDetail": True,
    "rowSelection": "single",
    "cellClass":"ag-right-aligned-cell",
    # the first Column is configured to use agGroupCellRenderer
    "columnDefs": [
        {
            "field": "name",
            "cellRenderer": "agGroupCellRenderer",
            "checkboxSelection": True,
        },
        {"field": "Name","type":"leftAligned"},
        {"field": "Cur_PX", "headerName": 'Close PX',"valueFormatter": "(x*1).toFixed(2)","type":"numericColumn"},
        {"field": "1_Day", "headerName": '1 Day', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Week", "headerName": '1 Week', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Month", "headerName": '1 Month', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "3_Months", "headerName": '3 Month', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Year", "headerName": '1 Year', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Year", "headerName": '2 Year', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "Since_Intercept", "headerName": 'Since Intercept', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},    
        {"field": "Start_PX", "headerName": 'Start PX',"valueFormatter": "(x*1).toFixed(2)","type":"numericColumn"},
        {"field": "Return", "headerName": 'Return', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "Start_Date", "headerName": 'Start Date',"type":"dateColumn"},
        {"field": "A/O Date", "headerName": 'Close Date',"type":"rightAligned"},

    ],
    "defaultColDef": {
        "flex": 1,
    },
}

AgGrid(px_strat, gridOptions=gridOptions, allow_unsafe_jscode=True, enable_enterprise_modules=True, theme='dark')


