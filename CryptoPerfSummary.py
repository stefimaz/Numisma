#Analyze performeace by Return Breakdown (xy), Annualized_std_dev, Average Annual Return, Sharpe_ratio, BTC_Beta (30d rolling average)
#Return Daily, Cumulative and Overall Summary Matrix 
#Author: Ken Lee 2022.02.22

# Import Modules
import pandas as pd
import os
import json
import requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import alpaca_trade_api as tradeapi
from pathlib import Path
import sqlalchemy as sql
import CryptoDownloadData as hist
from datetime import date
import logging
from dateutil.relativedelta import relativedelta
import numpy as np
from datetime import date
from datetime import datetime

crypto_data_connection_string = 'sqlite:///./Reference/crypto.db'

def get_price_matrix(p_portfolio_df, p_start_date, p_end_date):

    name_df = p_portfolio_df.copy()
    if 'symbol' in name_df:
        print('a')
        # do nothing
    elif 'name' in  name_df:
        name_df['symbol'] = name_df['name']
    else:
        name_df['symbol'] = name_df.index

    names = hist.get_where_condition(name_df, 'symbol')
    names
    sql_query = f"""
    SELECT DISTINCT date, symbol, close FROM CRYPTO_PX_HISTORY WHERE (date > '{p_start_date}' and date <= '{p_end_date}') and symbol in ({names})
    """
    portfolio_df = pd.read_sql_query(sql_query, crypto_data_connection_string)
    stock_hist_matrix = portfolio_df.pivot('date','symbol',values = 'close')  
    # Exclide any symbol having na (doesn't have full price history)
    stock_hist_matrix = stock_hist_matrix.dropna(axis='columns')
    stock_hist_matrix = stock_hist_matrix.dropna()
    #stock_hist_matrix = stock_hist_matrix.dropna()
    return stock_hist_matrix

def get_daily_return_matrix(p_stock_hist_matrix):
    navs_daily_returns = p_stock_hist_matrix.pct_change().dropna()
    return navs_daily_returns

def get_cumulative_return_matrix(p_stock_hist_matrix):
    navs_cumulative_returns = (1 +  p_stock_hist_matrix).cumprod() - 1
    navs_cumulative_returns = navs_cumulative_returns.dropna()
    return navs_cumulative_returns
  
def get_std_matrix(p_daily_return_matrix, p_year_trading_days, p_rolling_days):
    daily_std = p_daily_return_matrix.std() * (p_year_trading_days) ** (1 / 2)
    #daily_std = daily_std.sort_values()
    daily_std_df = pd.DataFrame(daily_std, columns = ['Annualized_std_dev'])
    daily_std_df['Average_annual_return'] = p_daily_return_matrix.mean() * (p_year_trading_days) 
    daily_std_df['Sharpe_ratio'] = (daily_std_df['Average_annual_return'] / daily_std_df['Annualized_std_dev'])
    btc_variance = p_daily_return_matrix['BTC'].rolling(window=p_rolling_days).var().dropna()
    btc_variance_df = pd.DataFrame(btc_variance)
    btc_variance_df = btc_variance_df.rename(columns={'BTC': 'BTC Var'})
    navs_covariance =  p_daily_return_matrix.rolling(window=p_rolling_days).cov(p_daily_return_matrix['BTC'].rolling(window=p_rolling_days)).dropna()
    navs_beta = navs_covariance.div(btc_variance_df['BTC Var'], axis = 0)
    navs_beta.dropna()
    beta_df = pd.DataFrame(navs_beta.mean(), columns = ['BTC_30d_roll_beta'])
    summary_matrix_df = pd.merge(daily_std_df, beta_df, left_index=True, right_index=True)
    return summary_matrix_df

def get_xy_daily_return_matrix(p_date, p_start_date, p_x_end_date, p_y_end_date):
    x_start_date = p_start_date
    x_end_date = p_x_end_date
    y_end_date = p_y_end_date
    historical_px_matrix = hist.get_price_history_by_period(p_date)
    historical_px_matrix['Start Date'] = x_start_date
    historical_px_matrix['Start Cost'] = historical_px_matrix['Y1']
    historical_px_matrix['X_End Date'] = x_end_date
    historical_px_matrix['X_End Close'] = historical_px_matrix['M6']
    historical_px_matrix['X_Return'] = historical_px_matrix['X_End Close'] / historical_px_matrix['Start Cost'] - 1  #pct_change
    historical_px_matrix['Y_End Date'] = y_end_date
    historical_px_matrix['Y_End Close'] = historical_px_matrix['D0']
    historical_px_matrix['Y_Return'] = historical_px_matrix['Y_End Close'] / historical_px_matrix['Start Cost'] - 1 #pct_change
    historical_px_matrix['XY_Return'] = historical_px_matrix['Y_End Close'] / historical_px_matrix['X_End Close'] - 1 #pct_change
    return historical_px_matrix

def get_benchmark_performance(p_etf_targetbenchmark_df, p_performance_summary_matrix):
    p_etf_targetbenchmark_df["symbol"] = p_etf_targetbenchmark_df.index
    p_etf_targetbenchmark_df["grp"] = p_etf_targetbenchmark_df["type"].str[:3]
    p_etf_targetbenchmark_df["grp"] = p_etf_targetbenchmark_df["grp"].str.upper()
    p_performance_benchmark = pd.merge(p_etf_targetbenchmark_df, p_performance_summary_matrix, on = ["symbol"])   
    return p_performance_benchmark

def get_our_portfolio(p_etf_list_df, p_etf_constituents_df, p_performance_benchmark, p_performance_summary_matrix, p_abs_beta_max, p_sharpe_ratio_min):
    #etf_list_df["etf"] = etf_list_df.index
    benchmark_statistics = p_performance_benchmark.describe()
    p_etf_list_df["grp"] = p_etf_list_df["type"].str[:3]
    p_etf_list_df["grp"] = p_etf_list_df["grp"].str.upper()
    
    p_performance_summary_matrix = p_performance_summary_matrix.dropna()
    etf_holings_matrix_df = pd.merge(p_etf_constituents_df, p_etf_list_df, how = "inner", on = ["etf"])
    etf_exposure_w_cnt = etf_holings_matrix_df.pivot_table(index = 'symbol', columns = 'grp', values = 'pct_holding', aggfunc=pd.Series.nunique)
    
    etf_exposure_w_cnt = etf_exposure_w_cnt.fillna(0)
    performance_symbols = pd.merge(etf_exposure_w_cnt, p_performance_summary_matrix, on = ["symbol"])
    #1. Pick Better performer than benchmark ETFs (Cumulative Return, Past 1 year Horizon Return X 6M, Y 1Y)
    # Hair Cutting 
    #2. Limit Beta Exposure vs. SP 500 based on given abs_beta_max
    #3. Expected performance vs. Excess risk taken by the investor by sharpe_ratio_min
    picked_symbols = performance_symbols[(performance_symbols['X_Return'] > benchmark_statistics.at['max','X_Return'] ) & (performance_symbols['Y_Return'] > benchmark_statistics.at['max','Y_Return']) & (performance_symbols['Average_annual_return'] > benchmark_statistics.at['max','Average_annual_return'])  & (performance_symbols['Sharpe_ratio'] > p_sharpe_ratio_min) & (abs(performance_symbols['BTC_30d_roll_beta']) < p_abs_beta_max)]
    picked_symbols = picked_symbols.sort_values(['X_Return', 'Y_Return'], ascending =[0, 0])
    return picked_symbols


def get_crypto_hist_martix_summary(t_date):
    dates_list_df = hist.get_hist_record_breakdown_by_period(t_date)
    historical_px_matrix = hist.get_price_history_by_period(t_date)
    historical_px_matrix 
    # 1. Analyze all names performance for comparison
    x_start_date = dates_list_df.loc[dates_list_df['period'] == 'Y1', 'date'].iloc[0]
    x_end_date = dates_list_df.loc[dates_list_df['period'] == 'M6', 'date'].iloc[0]
    y_end_date = t_date 
        
    daily_xy_horizon_return_matrix = get_xy_daily_return_matrix(t_date, x_start_date, x_end_date, y_end_date)
    daily_price_matrix = get_price_matrix(daily_xy_horizon_return_matrix, x_start_date, y_end_date)
    daily_return_matrix = get_daily_return_matrix(daily_price_matrix)
    cumulative_returns_matrix =  get_cumulative_return_matrix(daily_price_matrix)
    year_trading_days = 252
    rolling_days = 30
    analysis_matrix = get_std_matrix(daily_return_matrix, year_trading_days, rolling_days)
    performance_summary_matrix = daily_xy_horizon_return_matrix.merge(analysis_matrix, on = 'symbol', how = 'left')
    return performance_summary_matrix

def get_crypto_px_strat(t_date):
    dates_list_df = hist.get_hist_record_breakdown_by_period(t_date)
    historical_px_matrix = hist.get_price_history_by_period(t_date)
    historical_px_matrix 
    # 1. Analyze all names performance for comparison
    x_start_date = dates_list_df.loc[dates_list_df['period'] == 'Y1', 'date'].iloc[0]
    x_end_date = dates_list_df.loc[dates_list_df['period'] == 'M6', 'date'].iloc[0]
    y_end_date = t_date 
        
    daily_xy_horizon_return_matrix = get_xy_daily_return_matrix(t_date, x_start_date, x_end_date, y_end_date)
    daily_price_matrix = get_price_matrix(daily_xy_horizon_return_matrix, x_start_date, y_end_date)
    daily_return_matrix = get_daily_return_matrix(daily_price_matrix)
    cumulative_returns_matrix =  get_cumulative_return_matrix(daily_price_matrix)
    year_trading_days = 252
    rolling_days = 30
    analysis_matrix = get_std_matrix(daily_return_matrix, year_trading_days, rolling_days)
    performance_summary_matrix = daily_xy_horizon_return_matrix.merge(analysis_matrix, on = 'symbol', how = 'left')
    
    # 1. Analyze all names performance for comparison
    x_start_date = dates_list_df.loc[dates_list_df['period'] == 'Y1', 'date'].iloc[0]
    x_end_date = dates_list_df.loc[dates_list_df['period'] == 'M6', 'date'].iloc[0]
    y_end_date = t_date 
        
    daily_xy_horizon_return_matrix = get_xy_daily_return_matrix(t_date, x_start_date, x_end_date, y_end_date)
    daily_price_matrix = get_price_matrix(daily_xy_horizon_return_matrix, x_start_date, y_end_date)
    # 1) Simple Moving Average and 52 Weeks Low and High
    perf_screen_df = pd.DataFrame(daily_price_matrix.iloc[-1])
    perf_screen_df.columns[0]
    perf_screen_df.rename(columns={perf_screen_df.columns[0]:'CUR_PX'}, inplace = True)
    perf_screen_df['SMA_50'] = pd.DataFrame(round(daily_price_matrix.rolling(window=50).mean(),2).iloc[-1])
    perf_screen_df['SMA_150'] = pd.DataFrame(round(daily_price_matrix.rolling(window=150).mean(),2).iloc[-1])
    perf_screen_df['SMA_200'] = pd.DataFrame(round(daily_price_matrix.rolling(window=200).mean(),2).iloc[-1])
    perf_screen_df['SMA_200_20'] = pd.DataFrame(round(daily_price_matrix.rolling(window=200).mean(),2).iloc[-20])
    perf_screen_df['HIGH_52WK'] = pd.DataFrame(round(daily_price_matrix.rolling(window=52).max(),2).iloc[-1])
    perf_screen_df['LOW_52WK'] = pd.DataFrame(round(daily_price_matrix.rolling(window=52).min(),2).iloc[-1])
    # 2) Return Multiple
    return_multiple = performance_summary_matrix[['X_Return','XY_Return','Y_Return']].copy()
    return_multiple.rename(columns={'X_Return':'H1_Return','XY_Return':'H2_Return','Y_Return':'1Y_Return'}, inplace = True)
    return_multiple['H1_Multiple'] = round (( return_multiple['H1_Return'] /  return_multiple.at['BTC','H1_Return'] ), 2)
    return_multiple['H2_Multiple'] = round (( return_multiple['H1_Return'] /  return_multiple.at['BTC','H1_Return'] ), 2)
    return_multiple['1Y_Multiple'] = round (( return_multiple['1Y_Return'] /  return_multiple.at['BTC','1Y_Return'] ), 2)
    #display(return_multiple.head())

    # 3) RS Rating Relavtive Strong Rating 
    # BTC Benchmark
   # display(pd.DataFrame(perf_screen_df.loc['BTC']).transpose())
    rs_rating_df = return_multiple[['H1_Multiple','H2_Multiple','1Y_Multiple']].copy()
    rs_rating_df.rename(columns={'H1_Multiple':'H1_Rank','H2_Multiple':'H2_Rank','1Y_Multiple':'Y1_Rank'}, inplace = True)
    rs_rating_df = round((rs_rating_df.rank(pct=True) * 100), 2)
    perf_screen_df['RS_RATING'] = rs_rating_df['Y1_Rank'].copy()
    #display(perf_screen_df.head())
    return perf_screen_df

