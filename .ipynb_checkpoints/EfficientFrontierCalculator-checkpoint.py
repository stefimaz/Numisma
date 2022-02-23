import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
import pandas as pd

def calculate_efficient_frontier(asset_prices):
    
    # Calculate Log Returns
    log_returns = asset_prices.pct_change().apply(lambda x: np.log(1+x))
    
    # Calculate Covariance Matrix
    cov_matrix = log_returns.cov()

    #Calculate Correlation Matrix
    corr_matrix = log_returns.corr()
    
    # Calculate yearly returns
    y_returns = asset_prices.pct_change().sum()
    
    
    # Initialize the empty lists to store calculated returns 
    portfolio_returns = []
    portfolio_volatility = []
    portfolio_weights = []

    num_assets = len(asset_prices.columns)

    # Number of potential portfolios to calculate
    num_portfolios = 10000
    
    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        portfolio_weights.append(weights)
    
        returns = np.dot(weights, y_returns)                                   
        portfolio_returns.append(returns)
    
        var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
        sd = np.sqrt(var)
        ann_sd = sd*np.sqrt(250) 
        portfolio_volatility.append(ann_sd)
    
    portfolios_df = pd.DataFrame({'Returns' : portfolio_returns, 'Volatility' : portfolio_volatility, 'Weights': portfolio_weights})
    
    # Calculate and find the max Sharpe Ratio - The Optimal Portfolio
    risk_free_rate = .01

    optimal_portfolio = portfolios_df.iloc[((portfolios_df['Returns'] - risk_free_rate) /portfolios_df['Volatility']).idxmax()]
    
    
    return optimal_portfolio['Weights']