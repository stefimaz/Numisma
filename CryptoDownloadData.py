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
    SELECT * FROM (SELECT 'D0' as period,date from CRYPTO_PX_HISTORY order by date desc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'D7_W1' as period,date from CRYPTO_PX_HISTORY where '{week_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'M1' as period,date from CRYPTO_PX_HISTORY where '{month_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'M3' as period,date from CRYPTO_PX_HISTORY where '{month_3}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'M6' as period,date from CRYPTO_PX_HISTORY where '{month_6}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'Y1' as period,date from CRYPTO_PX_HISTORY where '{year_1}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'Y2' as period,date from CRYPTO_PX_HISTORY where '{year_2}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'Y3' as period,date from CRYPTO_PX_HISTORY where '{year_3}' <= date order by date asc LIMIT 1)
    UNION
    SELECT * FROM (SELECT 'Y0_YTD' as period,date from CRYPTO_PX_HISTORY where '{ytd}' <= date order by date asc LIMIT 1)
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