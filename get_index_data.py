import CryptoDownloadData as coinData
import pandas as pd

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

coinbase = {'BTC' : {'CoinGeckID' : 'bitcoin'},
            'ETH' : {'CoinGeckID' : 'ethereum'}, 
            'BNB' : {'CoinGeckID' : 'binancecoin'}, 
            'USDC' : {'CoinGeckID' : 'usd-coin'}, 
            'XRP' : {'CoinGeckID' : 'ripple'}, 
            'ADA' : {'CoinGeckID' : 'cardano'}, 
            'SOL' : {'CoinGeckID' : 'solana'}, 
            'LUNA' : {'CoinGeckID' : 'terra-luna'}, 
            'AVAX' : {'CoinGeckID' : 'avalanche-2'}}

metaverse = {'MANA' : {'CoinGeckID' : 'decentraland'}, 
             'SAND' : {'CoinGeckID' : 'the-sandbox'}, 
             'AXS' : {'CoinGeckID' : 'axie-infinity'}, 
             'THETA' : {'CoinGeckID' : 'theta-token'}, 
             'ENJ' : {'CoinGeckID' : 'enjincoin'},
             'WEMIX' : {'CoinGeckID' : 'wemix-token'}, 
             'WAXP' : {'CoinGeckID' : 'wax'}, 
             'RNDR' : {'CoinGeckID' : 'render-token'}, 
             'SUSHI' : {'CoinGeckID' : 'sushi'}, 
             'ONT' : {'CoinGeckID' : 'ontology'}, 
             'UOS' : {'CoinGeckID' : 'ultra'}, 
             'PLA' : {'CoinGeckID' : 'playdapp'}, 
             'CEEK' : {'CoinGeckID' : 'ceek'}, 
             'CHR' : {'CoinGeckID' : 'chromaway'}}

yieldfarm = {'CAKE' : {'CoinGeckID' : 'pancakeswap-token'}, 
             'AAVE' : {'CoinGeckID' : 'aave'}, 
             'CRV' : {'CoinGeckID' : 'curve-dao-token'}, 
             'RLY' : {'CoinGeckID' : 'rally-2'}, 
             'SNX' : {'CoinGeckID' : 'havven'}, 
             'SUSHI' : {'CoinGeckID' : 'sushi'}, 
             'RGT' : {'CoinGeckID' : 'rari-governance-token'}, 
             'REEF' : {'CoinGeckID' : 'reef-finance'}}


allindex = {'CAKE' : {'CoinGeckID' : 'pancakeswap-token'}, 
            'AAVE' : {'CoinGeckID' : 'aave'}, 
            'CRV' : {'CoinGeckID' : 'curve-dao-token'}, 
            'RLY' : {'CoinGeckID' : 'rally-2'}, 
            'SNX' : {'CoinGeckID' : 'havven'}, 
            'SUSHI' : {'CoinGeckID' : 'sushi'}, 
            'RGT' : {'CoinGeckID' : 'rari-governance-token'}, 
            'REEF' : {'CoinGeckID' : 'reef-finance'},
            'BTC' : {'CoinGeckID' : 'bitcoin'},
            'ETH' : {'CoinGeckID' : 'ethereum'}, 
            'BNB' : {'CoinGeckID' : 'binancecoin'}, 
            'USDC' : {'CoinGeckID' : 'usd-coin'}, 
            'XRP' : {'CoinGeckID' : 'ripple'}, 
            'ADA' : {'CoinGeckID' : 'cardano'}, 
            'SOL' : {'CoinGeckID' : 'solana'}, 
            'LUNA' : {'CoinGeckID' : 'terra-luna'}, 
            'AVAX' : {'CoinGeckID' : 'avalanche-2'},
            'MANA' : {'CoinGeckID' : 'decentraland'}, 
            'SAND' : {'CoinGeckID' : 'the-sandbox'}, 
            'AXS' : {'CoinGeckID' : 'axie-infinity'}, 
            'THETA' : {'CoinGeckID' : 'theta-token'}, 
            'ENJ' : {'CoinGeckID' : 'enjincoin'},
            'WEMIX' : {'CoinGeckID' : 'wemix-token'}, 
            'WAXP' : {'CoinGeckID' : 'wax'}, 
            'RNDR' : {'CoinGeckID' : 'render-token'}, 
            'SUSHI' : {'CoinGeckID' : 'sushi'}, 
            'ONT' : {'CoinGeckID' : 'ontology'}, 
            'UOS' : {'CoinGeckID' : 'ultra'}, 
            'PLA' : {'CoinGeckID' : 'playdapp'}, 
            'CEEK' : {'CoinGeckID' : 'ceek'}, 
            'CHR' : {'CoinGeckID' : 'chromaway'}}




def get_index_prices(selected_index):
    if selected_index == 'Coinbase100':
        index_coins = ['BTC', 'ETH', 'BNB', 'USDC', 'XRP', 'ADA', 'SOL', 'LUNA', 'AVAX']
    elif selected_index == 'TopMetaverseTokens':
        index_coins = ['MANA', 'SAND', 'AXS', 'THETA', 'ENJ','WEMIX', 'WAXP', 'RNDR', 'SUSHI', 'ONT', 'UOS', 'PLA', 'CEEK', 'CHR']
    elif selected_index == 'YieldFarmingTokens':
        index_coins = ['CAKE', 'AAVE', 'CRV', 'RLY', 'SNX', 'SUSHI', 'RGT', 'REEF']
    else:
        return ('ERROR: Invalid Index Entry.')
    
    index_prices = pd.DataFrame()
    
    for i in index_coins:
        prices_df = coinData.get_px_history(i)
        prices_list = prices_df['adjClose'].values.tolist()
        index_prices.insert(0, i, prices_list[0:365], True)
        
    return index_prices

def get_index_coins(selected_index):
    if selected_index == 'Coinbase100':
        index_coins = ['BTC', 'ETH', 'BNB', 'USDC', 'XRP', 'ADA', 'SOL', 'LUNA', 'AVAX']
    elif selected_index == 'TopMetaverseTokens':
        index_coins = ['MANA', 'SAND', 'AXS', 'THETA', 'ENJ','WEMIX', 'WAXP', 'RNDR', 'SUSHI', 'ONT', 'UOS', 'PLA', 'CEEK', 'CHR']
    elif selected_index == 'YieldFarmingTokens':
        index_coins = ['CAKE', 'AAVE', 'CRV', 'RLY', 'SNX', 'SUSHI', 'RGT', 'REEF']
    else:
        return ('ERROR: Invalid Index Entry.')
    
    return index_coins


def get_index_df(coins, weights):
    index_df = pd.DataFrame({'Coins' : coins, 'Weights' : weights})
    return index_df


def get_coin_values(investment, selected_index, index_df):
    
    if selected_index == 'Coinbase100':
        index_dict = coinbase
        index_coins = ['BTC', 'ETH', 'BNB', 'USDC', 'XRP', 'ADA', 'SOL', 'LUNA', 'AVAX']
    elif selected_index == 'TopMetaverseTokens':
        index_dict = metaverse
        index_coins = ['MANA', 'SAND', 'AXS', 'THETA', 'ENJ','WEMIX', 'WAXP', 'RNDR', 'SUSHI', 'ONT', 'UOS', 'PLA', 'CEEK', 'CHR']
    elif selected_index == 'YieldFarmingTokens':
        index_dict = yieldfarm
        index_coins = ['CAKE', 'AAVE', 'CRV', 'RLY', 'SNX', 'SUSHI', 'RGT', 'REEF']
    else:
        return ('ERROR: Invalid Index Entry.')
    
    index_df['Investment per Coin (USD)'] = investment * index_df['Weights']
    
    coin_prices = []
    
    for i in index_coins:
        coin = i
        cg_id = index_dict[coin]['CoinGeckID']
        price = cg.get_price(ids = cg_id, vs_currencies = 'usd')
        coin_prices.append(price[cg_id]['usd'])
        
    index_df['Coin Price (USD)'] = coin_prices
    
    index_df['Coins Owned'] = index_df['Investment per Coin (USD)'] / index_df['Coin Price (USD)']
    
    return index_df


def get_coin_values_by_weight_df(investment, weight_df):
    
    index_dict = allindex
    weight_df['weight'] = pd.to_numeric(weight_df['weight'])
    weight_df['investment'] = investment * weight_df['weight']
    
    coin_prices = []
    
    for symbol in weight_df['symbol']:
        cg_id = index_dict[symbol]['CoinGeckID']
        price = cg.get_price(ids = cg_id, vs_currencies = 'usd')
        coin_prices.append(price[cg_id]['usd'])
        
    weight_df['coin_px'] = coin_prices
    
    weight_df['coin_cnt'] = weight_df['investment'] / weight_df['coin_px']
    
    return weight_df