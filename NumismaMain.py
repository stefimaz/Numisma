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


##################### Run Inputs ##################
#ETF LIST:
#'Ventidex'
#'Farmdex'
#'Metadex'

run_date = date(2022, 3, 3) #date.today()
etf_name = 'Metadex'


##################### load Data ##################
curr_weight = coinData.get_etf_weight_by_date(etf_name, run_date)
orig_date = date(2021, 7, 15) # Intercept date -- do not change
orig_weight = coinData.get_etf_weight_by_date(etf_name, orig_date)
st.set_page_config(page_title="Numisma", layout="wide") 
st.title(etf_name + ' Portfolio')
px_strat = coinData.get_base_pxchanges_matrix(run_date)
selected_px_strat = pd.merge(px_strat, orig_weight, left_on='Name',right_on='symbol')
etf_return = coinData.get_etf_cum_return(etf_name, orig_weight, run_date, orig_date)


# Portfolio Returns % 
curr_return = etf_return.iloc[-1][etf_name]
d1_return = etf_return.iloc[-2][etf_name]
w1_return = etf_return.iloc[-7][etf_name]
m1_return = etf_return.iloc[-30][etf_name]
m3_return = etf_return.iloc[-90][etf_name]
m6_return = etf_return.iloc[-180][etf_name]


container0 = st.container()
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10  = st.columns(10)

with container0:
    with col1:
        st.caption("Current PX")
        st.metric(run_date.strftime('%m/%d/%Y'), f"${round(curr_return*1000,1)}", "")
    with col2:
        st.metric("1D","", f"{round((curr_return-d1_return)/d1_return*100,1)}%")
    with col3:
        st.metric("1W","", f"{round((curr_return-w1_return)/w1_return*100,1)}%")
    with col4:
        st.metric("1M", "", f"{round((curr_return-m1_return)/m1_return*100,1)}%")
    with col5:
        st.metric("3M", "",  f"{round((curr_return-m3_return)/m3_return*100,1)}%")
    with col10:
        st.caption("Since Intercept")
        st.metric(orig_date.strftime('%m/%d/%Y'), "$1000",  f"{round((curr_return-1.0)/1.0*100,1)}%")     
# Style Code
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

gridOptions = {
    # Master PX Table
    "masterDetail": True,
    "rowSelection": "single",
    "cellClass":"ag-right-aligned-cell",
    # the first Column is configured to use agGroupCellRenderer
    "columnDefs": [
        {"field": "Name","type":"leftAligned"},
        {"field": "Cur_PX", "headerName": 'Close PX',"valueFormatter": "(x*1).toFixed(2)","type":"numericColumn"},
        {"field": "weight", "headerName": 'Orig_Wt%',"valueFormatter": "(x*100).toFixed(2)","type":["numericColumn","numberColumnFilter"]},
        {"field": "1_Day", "headerName": '1 Day', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Week", "headerName": '1 Week', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Month", "headerName": '1 Month', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "3_Months", "headerName": '3 Months', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "1_Year", "headerName": '1 Year', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "Since_Intercept", "headerName": 'Since Intercept', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"}, 
        {"field": "Return", "headerName": 'Return', "valueFormatter": "(x*1).toFixed(2)","cellStyle":cellsytle_jscode,"type":"numericColumn"},
        {"field": "Start_PX", "headerName": 'Start PX',"valueFormatter": "(x*1).toFixed(2)","type":"numericColumn"},

       # {"field": "Start_Date", "headerName": 'Start Date',"type":"dateColumn"},
       # {"field": "A/O Date", "headerName": 'Close Date',"type":"rightAligned"},

    ],
    "defaultColDef": {
        "flex": 1,
    },
}

gridOptions_wt = {
    # enable Master / Detail
    "masterDetail": True,
    "rowSelection": "single",
    "cellClass":"ag-right-aligned-cell",
    # the first Column is configured to use agGroupCellRenderer
    "columnDefs": [
        {"field": "symbol", "headerName": 'Name',"type":"leftAligned"},
        {"field": "weight", "headerName": 'Curr_Wt%',"valueFormatter": "(x*100).toFixed(2)","type":"numericColumn"},
        {"field": "coin_px", "headerName": 'Coin Price$',"valueFormatter": "(x).toFixed(2)","type":"numericColumn"},
        {"field": "investment", "headerName": 'Investment$',"valueFormatter": "(x).toFixed(2)","type":"numericColumn"},
        {"field": "coin_cnt", "headerName": 'Coin Owned',"valueFormatter": "(x).toFixed(2)","type":"numericColumn"},

    ],
    "defaultColDef": {
        "flex": 1,
    },
}


AgGrid(selected_px_strat, gridOptions=gridOptions, allow_unsafe_jscode=True, enable_enterprise_modules=True, theme='dark')

pie_fig = curr_weight.iplot(kind="pie", labels="symbol", values="weight",
                         title=etf_name + " Coin Allocation",
                         asFigure=True,
                        hole=0.4)

#pie_fig
##################### Asset Detail Layout ##################
st.line_chart(etf_return)
container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        pie_fig
    with col2:
        invest_by_weight = gp.get_coin_values_by_weight_df(1000,curr_weight)
        st.caption('If investing $1000 USD on ' + run_date.strftime('%m/%d/%Y') + ":")
        AgGrid(invest_by_weight, gridOptions=gridOptions_wt, allow_unsafe_jscode=True, enable_enterprise_modules=True)


#container2 = st.container()
