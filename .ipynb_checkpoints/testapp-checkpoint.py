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
    with open(Path('./contracts/compiled/artregistry_abi.json')) as f:
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


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

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


st.title("Art Registry Appraisal System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Choose the Thematic Portfolio
################################################################################
st.markdown("## Select the Theme")
artwork_name = st.text_input("Enter the name of the artwork")
artist_name = st.text_input("Enter the artist name")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
if st.button("Register Artwork"):
    artwork_ipfs_hash = pin_artwork(artwork_name, file)
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_name,
        artist_name,
        int(initial_appraisal_value),
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
st.markdown("---")


################################################################################
# Appraise Art
################################################################################
st.markdown("## Appraise Artwork")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
appraisal_report_content = st.text_area("Enter details for the Appraisal Report")
if st.button("Appraise Artwork"):

    # Use Pinata to pin an appraisal report for the report URI
    appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content)
    report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the appraisal report history")
art_token_id = st.number_input("Artwork ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.createFilter(
        fromBlock=0, argument_filters={"tokenId": art_token_id}
    )
    reports = appraisal_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Appraisal Event Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This artwork has no new appraisals")

        
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

import os
from pathlib import Path
import requests

import hvplot.pandas
import numpy as np
import matplotlib.pyplot as plt
from MCForecastTools_2Mod import MCSimulation
import plotly.express as px
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm
from sklearn.linear_model import LinearRegression

#i commented out line 95-96 in the MCForecast file to avoid printing out lines "Running simulation number"

# title of the project and introduction on what to do 

st.title('Dividends Reinvestment Dashboard')
st.write('Analysis of the **Power** of **Dividend Reinvestment**.')
st.write('Select from the list of stocks that pays dividends.')
st.write('You will then be able to select between three options.')
st.write('***Choose wisely***.')

# chosen stock and crypto tickers. choice of the 3 different options






################################################################################
# Choose the Thematic Portfolio
################################################################################
theme = ("MDX","FDX","VDX")

# box selection for the stock to invest in
dropdown_theme = st.selectbox('Pick your theme', theme)

@st.cache
# Calculating the value of the investment compare to the amount of share selected, giving the amount 
def amount(share_amount):
    value = close_price(dropdown_stocks) * share_amount
    price = value
    return round(value,2)

def regression(stock_df, forecast_years):
    
    stock = yf.Ticker(dropdown_stocks)
    stock_df =  stock.history(start = start, end = end)
    stock_df["Time"] = stock_df.index
    stock_df["Time"] = stock_df["Time"].dt.year
    
    
    dividends = stock_df.loc[stock_df["Dividends"] > 0]
    dividends = dividends.drop(columns = ["Open", "High", "Low", "Close", "Volume", "Stock Splits"])
    dividends = dividends.groupby(["Time"]).sum()
    dividends["Years"] = dividends.index
    
    index_col = []
    for i in range(len(dividends.index)):
        index_col.append(i)
    dividends["Count"] = index_col
    
    x_amount = dividends["Count"].values.reshape(-1,1)
    y_amount = dividends["Dividends"].values.reshape(-1,1)
    
    amount_regression = LinearRegression().fit(x_amount,y_amount)
    yfit_amount = amount_regression.predict(x_amount)
    
    amount_regression.coef_ = np.squeeze(amount_regression.coef_)
    amount_regression.intercept_ = np.squeeze(amount_regression.intercept_)
    

    fig = px.scatter(dividends, y = "Dividends", x = "Years", trendline = "ols")

    st.write(fig)
    
    amount_forecast = []
    forecasted_year = []
    for i in range(len(dividends.index) + forecast_years):
        value = (amount_regression.coef_ * (i) + amount_regression.intercept_ )
        amount_forecast.append(round(value,3))
        forecasted_year.append(i+dividends["Years"].min())
    
    forecasted_data = pd.DataFrame(columns = ["Year", "Forecasted Rates"])
    forecasted_data["Year"] = forecasted_year
    forecasted_data["Forecasted Rates"] = amount_forecast
    return forecasted_data
    
  
    
initial_investment = (amount(share_amount))
st.info('Your initial investment is ${}'.format(amount(share_amount)))

# Showing amount of yearly dividend in $  
st.text(f'Your current yearly dividend for the amount of shares you selected is $:')
 
# Calculate the yearly $ after getting the value from yahoo finance    
string_summary2 = tickerData.info['dividendRate']
yearly_div_amount = (string_summary2) * (share_amount)
st.info(f'${yearly_div_amount}') 


#Predict stock using series of Monte Carlo simulation. Only works with one stock at a time.

def mc_stock_price(years):

    stock = yf.Ticker(dropdown_stocks)
    stock_hist =  stock.history(start = start, end = end)


    stock_hist.drop(columns = ["Dividends","Stock Splits"], inplace = True)
    stock_hist.rename(columns = {"Close":"close"}, inplace = True)
    stock_hist = pd.concat({dropdown_stocks: stock_hist}, axis = 1)
    
    #defining variables ahead of time in preparation for MC Simulation series
    Upper_Yields = []
    Lower_Yields = []
    Means = []
    Years = [currentYear]
    iteration = []
    
    for i in range(years+1):
        iteration.append(i)
        
        
    #beginning Simulation series and populating with outputs
    
    #for x in range(number of years)
    for x in range(years):
        MC_looped = MCSimulation(portfolio_data = stock_hist, 
                                        num_simulation= 100,
                                        num_trading_days= 252*x+1)
        MC_summary_stats = MC_looped.summarize_cumulative_return()
        Upper_Yields.append(MC_summary_stats["95% CI Upper"])
        Lower_Yields.append(MC_summary_stats["95% CI Lower"])
        Means.append(MC_summary_stats["mean"])
        Years.append(currentYear+(x+1))
    
    
    potential_upper_price = [element * stock_hist[dropdown_stocks]["close"][-1] for element in Upper_Yields]
    potential_lower_price = [element * stock_hist[dropdown_stocks]["close"][-1] for element in Lower_Yields]
    potential_mean_price = [element * stock_hist[dropdown_stocks]["close"][-1] for element in Means]

    prices_df = pd.DataFrame(columns = ["Lower Bound Price", "Upper Bound Price", "Forecasted Average Price"])
    prices_df["Lower Bound Price"] = potential_lower_price
    prices_df["Forecasted Average Price"] = potential_mean_price
    prices_df["Upper Bound Price"] = potential_upper_price

    fig = px.line(prices_df)
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = iteration,
            ticktext = Years
        )
    )
    
    st.write(fig)
    
    
    return prices_df

def cumsum_shift(s, shift = 1, init_values = [0]):
    s_cumsum = pd.Series(np.zeros(len(s)))
    for i in range(shift):
        s_cumsum.iloc[i] = init_values[i]
    for i in range(shift,len(s)):
        s_cumsum.iloc[i] = s_cumsum.iloc[i-shift] + s.iloc[i]
    return s_cumsum


def predict_crypto(crypto, forecast_period=0):
    forecast_days = forecast_period * 365
    
    btc_data = yf.download(crypto, start, end)
    btc_data["Date"] = btc_data.index
    btc_data["Date"] = pd.to_datetime(btc_data["Date"])
    btc_data["year"] = btc_data["Date"].dt.year
    
    years = btc_data["year"].max() - btc_data["year"].min()
    
    btc_data.reset_index(inplace = True, drop = True)
    btc_data.drop(columns = ["Open", "High", "Low", "Adj Close", "Volume"], inplace = True)
    
    btc_rolling = btc_data["Close"].rolling(window = round(len(btc_data.index)/100)).mean().dropna()
    btc_change = btc_rolling.pct_change().dropna()
    btc_cum = (1 + btc_change).cumprod()
    
    list = []
    for i in range(years):
        list.append(btc_cum[i*round(len(btc_cum)/years):(i+1)*round(len(btc_cum)/years)].mean())

    slope = (list[-1]-list[0])/len(list)

    list2 = []
    for i in range(years):
        list2.append((slope*i)+list[0])
    
    upper = []
    lower = []
    for i in range(years):
        lower.append((slope*i) + (list[0]-slope))
        upper.append((slope*i) + (list[0]+slope))
        
    counter = 0
    positions = []
    for i in range(1, years):
        if (list[i] >= lower[i]) & (list[i] <= upper[i]):
            positions.append(i*round(len(btc_cum)/years))
            positions.append((i+1)*round(len(btc_cum)/years))
            counter+=1
    
    if (counter < years/2):
        btc_rolling = btc_data["Close"][positions[-2]:].rolling(window = round(len(btc_data.index)/100)).mean().dropna()
    
    if forecast_period == 0:
        
        auto_model = pm.auto_arima(btc_rolling)

        model_str = str(auto_model.summary())

        model_str = model_str[model_str.find("Model:"):model_str.find("Model:")+100]

        start_find = model_str.find("(") + len("(")
        end_find = model_str.find(")")
        substring = model_str[start_find:end_find]

        arima_order = substring.split(",")

        for i in range(len(arima_order)):
            arima_order[i] = int(arima_order[i])
    
        arima_order = tuple(arima_order)
    
        train = btc_rolling[:int(0.8*len(btc_rolling))]
        test = btc_rolling[int(0.8*len(btc_rolling)):]
        
#         test_length = 

        model = ARIMA(train.values, order=arima_order)
        model_fit = model.fit(disp=0)
    
    
    
#         if ( float(0.2*len(btc_rolling)) < int(0.2*len(btc_rolling))):
        fc, se, conf = model_fit.forecast(len(test.index), alpha=0.05)  # 95% conf
#         else:
#             fc, se, conf = model_fit.forecast((int(0.2*len(btc_rolling))), alpha=0.05)

        fc_series = pd.Series(fc, index=test.index)
        lower_series = pd.Series(conf[:, 0], index=test.index)
        upper_series = pd.Series(conf[:, 1], index=test.index)
    
        plt.rcParams.update({'font.size': 40})
        fig = plt.figure(figsize=(40,20), dpi=100)
        ax = fig.add_subplot(1,1,1)
        l1 = ax.plot(train, label = "Training")
        l2 = ax.plot(test, label = "Testing")
        l3 = ax.plot(fc_series, label = "Forecast")
        ax.fill_between(lower_series.index, upper_series, lower_series,
                         color='k', alpha=.15)
        ax.set_title('Forecast vs Actuals')
        fig.legend(loc='upper left', fontsize=40), (l1,l2,l3)
        plt.rc('grid', linestyle="-", color='black')
        plt.grid(True)
        st.write(fig)
    


    else:
        auto_model = pm.auto_arima(btc_rolling)

        model_str = str(auto_model.summary())

        model_str = model_str[model_str.find("Model:"):model_str.find("Model:")+100]

        start_find = model_str.find("(") + len("(")
        end_find = model_str.find(")")
        substring = model_str[start_find:end_find]

        arima_order = substring.split(",")

        for i in range(len(arima_order)):
            arima_order[i] = int(arima_order[i])

        arima_order = tuple(arima_order)
    
    
        train = btc_rolling[:int(0.8*len(btc_rolling))]
        test = btc_rolling[int(0.8*len(btc_rolling)):]
    
        model = ARIMA(train.values, order=arima_order)
        model_fit = model.fit(disp=0)

        fighting = np.arange(0, (test.index[-1] + forecast_days) - test.index[0])
        empty_df = pd.DataFrame(fighting)
        empty_df.index = np.arange(test.index[0], test.index[-1] + forecast_days)
    

        if ( float(0.2*len(btc_rolling)) > int(0.2*len(btc_rolling)) ):
            fc, se, conf = model_fit.forecast(len(empty_df.index), alpha=0.05)  # 95% conf
        else:
            fc, se, conf = model_fit.forecast(len(empty_df.index), alpha=0.05)

        fc_series = pd.Series(fc, index=empty_df.index)
        lower_series = pd.Series(conf[:, 0], index=empty_df.index)
        upper_series = pd.Series(conf[:, 1], index=empty_df.index)
    
        plt.rcParams.update({'font.size': 40})
        fig = plt.figure(figsize=(40,20), dpi=100)
        ax = fig.add_subplot(1,1,1)
        l1 = ax.plot(train, label = "Training")
        l2 = ax.plot(test, label = "Testing")
        l3 = ax.plot(fc_series, label = "Forecast")
        ax.fill_between(lower_series.index, upper_series, lower_series,
                         color='k', alpha=.15)
        ax.set_title('Forecast vs Actuals')
        fig.legend(loc='upper left', fontsize=40), (l1,l2,l3)
        plt.rc('grid', linestyle="-", color='black')
        plt.grid(True)
        st.write(fig)
        
#     forecast_crypto = pd.DataFrame(predict_crypto(dropdown_crypto, year_opt2))
#     forecast_crypto = forecast_crypto.T
        forecast_crypto = pd.DataFrame()
    
        f_diffed = round(len(btc_data.index)/100) * fc_series.diff()
        u_diffed = round(len(btc_data.index)/100) * upper_series.diff()
        l_diffed = round(len(btc_data.index)/100) * lower_series.diff()

        forecast_crypto["Forecasted Values"] = cumsum_shift(f_diffed, round(len(btc_data.index)/100), fc_series.values[:round(len(btc_data.index)/100)])
        forecast_crypto["Upper 95% Bound"] = cumsum_shift(u_diffed, round(len(btc_data.index)/100), upper_series.values[:round(len(btc_data.index)/100)])
        forecast_crypto["Lower 95% Bound"] = cumsum_shift(l_diffed, round(len(btc_data.index)/100), lower_series.values[:round(len(btc_data.index)/100)])
        
        date_list = [btc_data["Date"][test.index[0]] + datetime.timedelta(days=x) for x in range(len(empty_df.index))]
        forecast_crypto["Date"] = date_list
        forecast_crypto["Date"] = pd.to_datetime(forecast_crypto["Date"])
        forecast_crypto["Date"] = forecast_crypto["Date"].dt.date
        forecast_crypto.set_index("Date", inplace = True)
        return forecast_crypto
    

# This is where the user make the choice of where to reinvest the dividend paid. 

dropdown_option = st.selectbox('Where do you want to reinvest your dividends?', options)

# Create and empty DataFrame for closing prices of chosen stock
df_stock_prices = pd.DataFrame()

# Fetch the closing prices for all the stocks
df_stock_prices[dropdown_option] = close_price(dropdown_stocks)


    

# Calculating the cumulative returns after choosing the same stock option
if dropdown_option == "Keep the cash":
    
    # Slider 3 with option to select the amount of year to reinvest(10, 20 or 30)
    year_opt3 = st.slider('How many years of pocketing the cash?', min_value= 10, max_value= 30, value=10, step= 10)
    st.write(f'You will reinvest your dividends for {year_opt3} years')
    
    daily = yf.download(dropdown_stocks, start, end)['Adj Close']
    def average_annual (daily):
        rel = daily.pct_change()
        ave_rel= rel.mean()
        anual_ret = (ave_rel * 252) * 100
        return anual_ret
    st.subheader(f'Average yearly returns of {dropdown_stocks} is {average_annual(daily): .2f}%')
    
    yearly_returns = average_annual(daily)
    investment1 = initial_investment
    interest1 =  yearly_returns
    
    def sip_stock(investment, tenure, interest, amount= investment1, is_year=True, is_percent=True, show_amount_list=False):
        tenure = tenure*12 if is_year else tenure
        interest = interest/100 if is_percent else interest
        interest /= 12
        amount_every_month = {}
        for month in range(tenure):
            amount = (amount + investment)*(1+interest)
            amount_every_month[month+1] = amount
        return {f'A': amount,
                'Amount every month': amount_every_month} if show_amount_list else round(amount, 2) 
    # (monthly amount, years, percent returned)
    SIP_stock_maturity = sip_stock(0, year_opt3, interest1)
    
    st.subheader(f'The projected return for {dropdown_stocks} is:')
    st.success(f'${SIP_stock_maturity}')
#    st.subheader(f'Your total dividend return will be {SIP_maturity}')

         
    investment = yearly_div_amount / 12
    interest = 0
    # simulation of dividend investment over time. 
    # simple dividend reinvestment function
    @st.cache
    def sip(investment, tenure, interest, amount=0, is_year=True, is_percent=True, show_amount_list=False):
        tenure = tenure*12 if is_year else tenure
        interest = interest/100 if is_percent else interest
        interest /= 12
        amount_every_month = {}
        for month in range(tenure):
            amount = (amount + investment)*(1+interest)
            amount_every_month[month+1] = amount
        return {f'A': amount,
                'Amount every month': amount_every_month} if show_amount_list else round(amount, 2) 
    # (monthly amount, years, percent returned)
    SIP_maturity = sip(investment, year_opt3, interest)
    
    st.subheader(f'Your total dividend return will be')
    st.success(f'${SIP_maturity}')


elif dropdown_option == "Same Stock":
    @st.cache
    def relativeret(df):
        rel = df.pct_change()
        cumret = (1 + rel).cumprod() - 1
        cumret = cumret.fillna(0)
        return cumret
    
    # Showing the plot of the cumulative returns
    if len(dropdown_stocks) > 0:
        df = relativeret(yf.download(dropdown_stocks, start, end)['Adj Close'])
        st.header('Cumulative returns of {}'.format(dropdown_stocks))
        st.line_chart(df)
     
    # Calculate the annual average return data for the stocks
    # Use 252 as the number of trading days in the year    
    stock = yf.download(dropdown_stocks, start, end)['Adj Close'] 
    
    def average_annual (daily):
        rel = stock.pct_change()
        ave_rel= rel.mean()
        anual_ret = (ave_rel * 252) * 100
        return anual_ret
    yearly_returns = average_annual(stock)
    
    
    st.subheader(f'Average yearly returns of {dropdown_stocks} is {average_annual(stock): .2f}%')
    
    
    
    # Slider 1 with option to select the amount of year to reinvest(10, 20 or 30)
    year_opt1 = st.slider('How many years of investment projections?', min_value= 10, max_value= 30, value=10, step= 10) 
    
    dividend_regression = regression(dropdown_stocks, year_opt1)
    st.dataframe(dividend_regression)
    
    mc_stock = mc_stock_price(year_opt1)
    st.subheader(f'This is the simulated price for {dropdown_stocks} ({stock_name}).')
    st.dataframe(mc_stock)

    zero = round(mc_stock["Forecasted Average Price"][0],2)
    last = round(mc_stock["Forecasted Average Price"][year_opt1-1],2)
    pct_gain  =  ( ( (last- zero) / zero ) )
    
    same_amount_div = yearly_div_amount / 12
    same_interest = yearly_returns
    investment3 = initial_investment
    @st.cache
    def same_stock(investment, tenure, interest, amount=investment3, is_year=True, is_percent=True, show_amount_list=False):
        tenure = tenure*12 if is_year else tenure
        interest = interest/100 if is_percent else interest
        interest /= 12
        amount_every_month = {}
        for month in range(tenure):
            amount = (amount + investment)*(1+interest)
            amount_every_month[month+1] = amount
        return {f'A': amount,
                'Amount every month': amount_every_month} if show_amount_list else round(amount, 2) 
    # (monthly amount, years, percent returned)
    Same_maturity = same_stock(same_amount_div, year_opt1, same_interest)
        
    st.info(f"The percent gain of the simulated forecasts is {round(float(pct_gain*100), 2)}%")
    
    st.subheader(f'Your stock average value after {year_opt1} years of reinvesting the dividends will be:')
    st.success(f'${Same_maturity}')
    
    st.text(f"Your reinvested dividend of ${yearly_div_amount} every years, would be worth:")
    st.success(f'${round(yearly_div_amount*pct_gain,2)}')
    
    
    # Calculating the projected return for crypto opyion chosen here
elif dropdown_option == "Crypto":
    
    # selection of the crypto to reinvest in
    dropdown_crypto = st.selectbox('What crypto would you like to reinvest in?', crypto)
    
    # Getting the data for selected crypto from yahoo finance and ploting it as a line chart
    if len(dropdown_crypto) > 0:
        df = yf.download(dropdown_crypto, start, end)
        st.header('Historical value of {}'.format(dropdown_crypto))
        st.dataframe(df)
        st.line_chart(df["Adj Close"])
        st.text("Using regression analysis, this is a model created to forecast the moving average of crypto-currency.")
        predict_crypto(dropdown_crypto)
    
        # Slider 2 with option to select the amount of year to reinvest(10, 20 or 30)
    year_opt2 = st.slider('Using the same regression model, how many years of investment projections?', min_value= 5, max_value= 15, value=5, step= 5)
    crypto_forecast = predict_crypto(dropdown_crypto, year_opt2)
    st.dataframe(crypto_forecast)
    
    
    crypto_gain = round( ((float(crypto_forecast["Forecasted Values"][-1:]) - float(crypto_forecast["Forecasted Values"][0])) / crypto_forecast["Forecasted Values"][0]) * 100 , 2)
    st.info(f"The percent gain from the forecasted values is {crypto_gain}%")
    st.text(f"Using the total yearly dividend of ${yearly_div_amount} reinvested in {dropdown_crypto} could get you:") 
    st.success(f"Future value of ${round(yearly_div_amount*crypto_gain,2)}")
    
    
    
    # simulation of chosen crypto using invested dividends to be added here
     
# Calculating the projected return for reinvestment into the same stock chosen here

