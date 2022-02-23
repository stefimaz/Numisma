import CryptoDownloadData as coinData
import pandas as pd

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