#Download Crypto PX History by using Alpha and YahooFinance API
#Ken Lee - 2021.02.21
#DB NAME: CYPTO_PX_HISTORY

import requests
import pandas as pd
import os
import json
from dotenv import load_dotenv
import sqlalchemy as sql
from pathlib import Path
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
import numpy as np
import CryptoPerfSummary as coinAnalytic
import EfficientFrontierCalculator as ef
import get_index_data as gp
load_dotenv()
alpha_api_key = os.getenv("ALPHA_API_KEY")


# Database connection string
crypto_data_connection_string = 'sqlite:///./Reference/crypto.db'
# Database engine
crypto_data_engine = sql.create_engine(crypto_data_connection_string, echo=True)


def drop_table(p_table_name):
    connection = crypto_data_engine.raw_connection()
    cursor = connection.cursor()
    command = "DROP TABLE IF EXISTS {};".format(p_table_name)
    cursor.execute(command)
    connection.commit()
    cursor.close()

def create_index_from_csv(p_path, p_db_name):
    #1.Load ETF List (Parents) from CSV
    coin_list_df = pd.read_csv(p_path, index_col='symbol', parse_dates=True, infer_datetime_format=True)
    coin_list_df.to_sql(p_db_name, crypto_data_engine, index_label='symbol', if_exists='replace')


def get_crypto_px(symbol, start_date = None, end_date = None):
    api_key = os.getenv("ALPHA_API_KEY")
    exchange = 'USD'
    api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={exchange}&apikey={api_key}'
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df['Time Series (Digital Currency Daily)']).T
    df = df.rename(columns = {'1a. open (USD)': 'Open', '2a. high (USD)': 'High', '3a. low (USD)': 'Low', '4a. close (USD)': 'Close', '5. volume': 'Volume'})
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1].drop(['1b. open (USD)', '2b. high (USD)', '3b. low (USD)', '4b. close (USD)', '6. market cap (USD)'], axis = 1)
    if start_date:
        df = df[df.index >= start_date]
    if end_date:
        df = df[df.index <= end_date]
    df['date'] = pd.to_datetime(df.index).date
    df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adjClose', 'Volume': 'volume'})
    df.index = pd.to_datetime(df.index).date
    df.insert(0, 'symbol', symbol)
    return df

def get_crypto_px_yf(symbol, start_date = None, end_date = None):
    df = yf.download(symbol+'-USD', start_date, end_date)
    df['date'] = pd.to_datetime(df.index).date
    df.index = pd.to_datetime(df.index).date
    df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adjClose', 'Volume': 'volume'})
    df.insert(0, 'symbol', symbol)
    return df


def download_px_data(df_symbols, symbol_colName, start_date = None, end_date = None):
    for symbol in df_symbols[symbol_colName]:
        df = get_crypto_px_yf(symbol, start_date, end_date)
        df.to_sql('CRYPTO_PX_HISTORY', crypto_data_engine, index=True, if_exists='append')
        display(df)

def create_coinlist100():
    #1. Create the Sample 100 coins
    file_path = Path('./Reference/Coinbase100.csv')
    create_index_from_csv(file_path, 'COINBASE_100')

def create_sampleETF():
    #2. Create Sample ETF List
    file_path = Path('./Reference/sampleETF.csv')
    create_index_from_csv(file_path, 'ETF_LIST')

def download_px_data_from_COINBASE_100(start_date, end_date):
    sql_query = """
    SELECT * 
    FROM COINBASE_100"""
    coin_symbols = pd.read_sql_query(sql_query, crypto_data_connection_string)
    coin_symbols
    download_px_data(coin_symbols, 'symbol', start_date, end_date)

def get_market_datas_by_period(p_today):
    day_1 = p_today + relativedelta(days=-1)
    year_1 = day_1 + relativedelta(years=-1)
    year_2 = day_1 + relativedelta(years=-2)
    year_3 = day_1 + relativedelta(years=-3)
    day_2 = day_1 + relativedelta(days=-2)
    week_1 = day_1 + relativedelta(weeks=-1)
    month_1 = day_1 + relativedelta(months=-1)
    month_3 = day_1 + relativedelta(months=-3)
    month_6 = day_1 + relativedelta(months=-6)
    ytd = date(day_1.year, 1, 1)
    
    sql_query = f"""
    SELECT DISTINCT * FROM (SELECT DISTINCT 'D0' as period,date from CRYPTO_PX_HISTORY order by date desc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'D1' as period,date from CRYPTO_PX_HISTORY where '{day_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'W1' as period,date from CRYPTO_PX_HISTORY where '{week_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'M1' as period,date from CRYPTO_PX_HISTORY where '{month_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'M3' as period,date from CRYPTO_PX_HISTORY where '{month_3}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'M6' as period,date from CRYPTO_PX_HISTORY where '{month_6}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'Y1' as period,date from CRYPTO_PX_HISTORY where '{year_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'Y2' as period,date from CRYPTO_PX_HISTORY where '{year_2}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'Y3' as period,date from CRYPTO_PX_HISTORY where '{year_3}' <= date order by date asc LIMIT 1)
    UNION
    SELECT DISTINCT * FROM (SELECT DISTINCT 'Y0_YTD' as period,date from CRYPTO_PX_HISTORY where '{ytd}' <= date order by date asc LIMIT 1)
    """
    history_dates = pd.read_sql_query(sql_query, crypto_data_connection_string)
    history_dates = history_dates.sort_values(by=['date'], ascending=False)
    return history_dates
            

def get_where_condition(p_df, p_column_name):
    where_condition = "" 
    for index, row in p_df.iterrows():
        if where_condition == "":
            where_condition = f"'{row[p_column_name]}'"
        else:
            where_condition = f"{where_condition}, '{row[p_column_name]}'"
    return where_condition 
    
    
def get_market_dates_list_condition(p_history_dates):
    where_dates = "" 
    for index, row in p_history_dates.iterrows():
        if where_dates == "":
            where_dates = f"'{row['date']}'"
        else:
            where_dates = f"{where_dates}, '{row['date']}'"
    return where_dates
    
def get_price_history_by_period(p_today):
    history_dates = get_market_datas_by_period(p_today)
    where_dates = get_market_dates_list_condition(history_dates)
    sql_query = f"""
    SELECT DISTINCT * FROM CRYPTO_PX_HISTORY WHERE date in ({where_dates})
    """
    CRYPTO_PX_HISTORY = pd.read_sql_query(sql_query, crypto_data_connection_string)        
    #CRYPTO_PX_HISTORY        
    history_df = CRYPTO_PX_HISTORY.merge(history_dates, on="date", how='inner')
    price_hist_matrix = history_df.pivot('symbol','period',values = 'close')     
    
    return price_hist_matrix

def get_hist_record_breakdown_by_period(p_today):
    sql_query = f"""
    SELECT distinct date, count(date) FROM CRYPTO_PX_HISTORY group by date
    """

    available_data_dates = pd.read_sql_query(sql_query, crypto_data_connection_string)
    market_dates = get_market_datas_by_period(p_today)

    dates_list = pd.merge(available_data_dates, market_dates, how='outer', indicator=True)
    dates_list= dates_list.loc[dates_list._merge == 'both', ['date', 'count(date)', 'period']]
    return dates_list

def get_px_history(p_symbol):
    sql_query = f"""
    SELECT DISTINCT * FROM CRYPTO_PX_HISTORY WHERE symbol='{p_symbol}'
    """
    px_history_df = pd.read_sql_query(sql_query, crypto_data_connection_string)
    px_history_df = px_history_df.drop(['index'], axis = 1)
    px_history_df = px_history_df.set_index('date')
    
    return px_history_df 

#Our 3 ETF Sample - 
#file_path = Path('./Reference/sampleETF.csv')
#coinData.create_index_from_csv(file_path, 'ETF_LIST')
#coinData.create_sampleETF
#Coinbase100  -- Ventidex
#TopMetaverseTokens -- Metadex
#YieldFarmingCoins -- Farmdex
#coinData.create_sampleETF

def get_symbollist_by_index(etf_name = None):
    if etf_name is not None:
        sql_query = f"""
        SELECT DISTINCT symbol FROM ETF_LIST WHERE ETF = '{etf_name}' """
    else:
        sql_query = f"""
        SELECT DISTINCT symbol FROM ETF_LIST"""
    
    etf_list= pd.read_sql_query(sql_query, crypto_data_connection_string)
    symbol_list = get_where_condition(etf_list, 'symbol')
    return symbol_list

def get_pxhist_by_symbol_list(symbol_list, column_name = None, start_date = None, end_date = None):
    
    if column_name is not None:
        select = f"date, symbol, {column_name}"
    else:
        select = '*'
    
    
    if start_date is not None and end_date is not None:
        sql_query  = f"SELECT DISTINCT {select} FROM CRYPTO_PX_HISTORY WHERE symbol in ({symbol_list}) and (date >='{start_date}' and date <= '{end_date}')"
    elif start_date is not None:
        sql_query  = f"SELECT DISTINCT {select} FROM CRYPTO_PX_HISTORY WHERE symbol in ({symbol_list}) and date >='{start_date}'"
    elif end_date is not None:
        sql_query  = f"SELECT DISTINCT {select} FROM CRYPTO_PX_HISTORY WHERE symbol in ({symbol_list}) and date <='{end_date}'"
    else:
        sql_query  = f"SELECT DISTINCT {select} FROM CRYPTO_PX_HISTORY WHERE symbol in ({symbol_list})"
    
    px_history_df = pd.read_sql_query(sql_query, crypto_data_connection_string)
    if 'index' in px_history_df.columns:
        px_history_df = px_history_df.drop(['index'], axis = 1)
    px_history_df = px_history_df.set_index('date')
    
    return px_history_df


def get_base_pxhorizon_matrix(t_date = None):
    sql_query = """
    SELECT max(date) date FROM CRYPTO_PX_HISTORY order by date desc"""
    t_date_str= pd.read_sql_query(sql_query, crypto_data_connection_string)
    t_date_str.iat[0,0]
    #print(type(t_date))
    if t_date == None:
        t_date = datetime.strptime(t_date_str.iat[0,0], '%Y-%m-%d').date()
        t_date = t_date + relativedelta(days=-1)
    date_list = get_market_datas_by_period(t_date)
    x_start_date = datetime(2021, 7, 15)
    x_end_date = datetime(2021, 12, 1)
    y_end_date = t_date 
    daily_xy_horizon_return_matrix = coinAnalytic.get_xy_daily_return_matrix(t_date, x_start_date, x_end_date, y_end_date)
    return daily_xy_horizon_return_matrix


def get_base_pxchanges_matrix(t_date = None):
    
    if (t_date == None) or (t_date >= date(2022, 3, 2)):
        t_date = date(2022, 3, 2)
    
    sql_query = f"""
    SELECT * FROM PX_SUMMARY_CACHE where [A/O Date] = '{t_date}'"""# where date = '{t_date}' and ETF = '{etf_name}'"""
    summary_list= pd.read_sql_query(sql_query, crypto_data_connection_string)
    summary_list.set_index('symbol', inplace=True)
    return_matrix = summary_list
    
    if len(summary_list) == 0:
    
        daily_xy_horizon_return_matrix = get_base_pxhorizon_matrix(t_date)
        return_matrix = pd.DataFrame()
        return_matrix['A/O Date'] = daily_xy_horizon_return_matrix['Y_End Date']
        return_matrix['Name'] = daily_xy_horizon_return_matrix.index
        return_matrix['Cur_PX'] = daily_xy_horizon_return_matrix['D0']
        return_matrix['1_Day'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['D1'])/daily_xy_horizon_return_matrix['D1']
        return_matrix['1_Week'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['W1'])/daily_xy_horizon_return_matrix['W1']
        return_matrix['1_Month'] =100 *  (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['M1'])/daily_xy_horizon_return_matrix['M1']
        return_matrix['3_Months'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['M3'])/daily_xy_horizon_return_matrix['M3']
        return_matrix['YTD'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['Y0_YTD'])/daily_xy_horizon_return_matrix['Y0_YTD']
        return_matrix['1_Year'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['Y1'])/daily_xy_horizon_return_matrix['Y1']
        return_matrix['2_Years'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['Y2'])/daily_xy_horizon_return_matrix['Y2']
        return_matrix['3_Years'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['Y3'])/daily_xy_horizon_return_matrix['Y3']
        return_matrix['Start_Date'] = daily_xy_horizon_return_matrix['Start Date']
        return_matrix['Since_Intercept'] = 100 * (daily_xy_horizon_return_matrix['D0']-daily_xy_horizon_return_matrix['Start Cost'])/daily_xy_horizon_return_matrix['Start Cost']
        return_matrix['Start_PX'] = daily_xy_horizon_return_matrix['Start Cost']
        return_matrix['Return'] = 100 * daily_xy_horizon_return_matrix['XY_Return']
        return_matrix = return_matrix.fillna('--')
        return_matrix = return_matrix.round({'1_Day': 2})
        return_matrix.to_sql('PX_SUMMARY_CACHE', crypto_data_engine, index=True, if_exists='append') #Cache the data for fast loading
    return return_matrix

def get_pxhist_by_etfname(etf_name = None, column_name = None, start_date = None, end_date = None):
    symbol_list = get_symbollist_by_index(etf_name)
    px_history_df = get_pxhist_by_symbol_list(symbol_list, column_name, start_date, end_date)
    return px_history_df

def get_etf_list(etf_name):
    #if eft_name is None:
    #    etf_name = "farmdex','Metadex','Ventidex"
    #
    sql_query = f"""
    SELECT * FROM ETF_LIST where ETF = '{etf_name}'"""
    etf_list= pd.read_sql_query(sql_query, crypto_data_connection_string)
    return etf_list


def calculate_save_etf_weight(etf_name, start_date, end_date):
    etf_list = get_etf_list(etf_name)
    t_date = start_date + relativedelta(days=365)
    symbol_list = pd.DataFrame(etf_list['symbol'].loc[etf_list['ETF']==etf_name])
    symbol_list = symbol_list.reset_index(drop=True)
    #display(symbol_list)
    daily_price_matrix = coinAnalytic.get_price_matrix(symbol_list, start_date, end_date)
    daily_price_matrix.index = pd.to_datetime(daily_price_matrix.index)
    daily_price_dates = daily_price_matrix.loc[daily_price_matrix.index>=t_date]

    
    
    for date in daily_price_dates.index:
        price = daily_price_matrix.loc[daily_price_matrix.index<=date].tail(365)
        weights = ef.calculate_efficient_frontier(price)
        weight_df = pd.DataFrame(columns=['date','ETF', 'symbol', 'weight'])
        index_no = 0
        for weight in weights:
            #print(index_no)
            symbol =  (symbol_list.loc[index_no, 'symbol'])
            print(date)
            if date is not None:
                weight_df = weight_df.append(pd.DataFrame({'date':[date], 'ETF': [etf_name], 'symbol':[symbol], 'weight':[weight]}))
            index_no = index_no + 1
            
            #weight_df = weight_df.dropna
        display(weight_df)
        weight_df.set_index('date', inplace=True)
        weight_df = weight_df.dropna()
        weight_df.to_sql('CRYPTO_ETF_WEIGHT', crypto_data_engine, index=True, if_exists='append')


def get_etf_weight_by_date(etf_name, run_date):
    if run_date == date(2022, 3, 2):
        run_date = date(2022, 3, 3)
    sql_query = f"""
    SELECT distinct symbol, weight FROM CRYPTO_ETF_WEIGHT where ETF = '{etf_name}' and date like '{run_date}%'"""
    weight_list= pd.read_sql_query(sql_query, crypto_data_connection_string)
    return weight_list


def get_etf_cum_return(etf_name, orig_weight, run_date, orig_date):
    etf_list_array = orig_weight['symbol'].to_numpy()
    daily_price_matrix = coinAnalytic.get_price_matrix(orig_weight, (orig_date+ relativedelta(days=-1)), run_date)
    daily_return_matrix = coinAnalytic.get_daily_return_matrix(daily_price_matrix)
    cumulative_returns_matrix =  coinAnalytic.get_cumulative_return_matrix(daily_price_matrix)
    portfolio = daily_price_matrix[etf_list_array]
    return_stocks = portfolio.pct_change()
#return_stocks.head(10)
    initial_weight = orig_weight['weight'].to_numpy()
    daily_returns_portfolio_mean = return_stocks.mean()
    allocated_daily_returns = (initial_weight * daily_returns_portfolio_mean)
    portfolio_return = np.sum(allocated_daily_returns)
#print(portfolio_return)
    return_stocks[etf_name] = return_stocks.dot(initial_weight)
    Cumulative_returns_daily = (1+return_stocks).cumprod()
    Cumulative_returns_daily = Cumulative_returns_daily.dropna()
    our_etf_df = pd.DataFrame(Cumulative_returns_daily[etf_name].copy())
    our_etf_df.index = pd.to_datetime(our_etf_df.index)
   # orig_df = pd.DataFrame({etf_name: '1.0'}, index = '2021-07-15')   
    #our_etf_df = our_etf_df.append(orig_df)
    #our_etf_df = our_etf_df.sort_index()
    return our_etf_df

