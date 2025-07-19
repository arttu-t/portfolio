This is a python program for backtesting different momentum-based investing strategies. In the current code, the program takes 10 stocks at the start of each month from the S&P500 that have grown the most in 
the last 6 months, excluding the most recent month. It then holds them for a month and sells them, unless the 15 percent trailing stoploss is triggered, in which case they're sold at the price the stop loss 
activated. You can backtest how different momentum investing strategies would have worked historically. The program requires pandas and yfinance to run, and the file 'tickers_by_date.csv' contains the sp500 
companies for each day, starting from the 1990s. With the settings now in place, the program has returned about 22 percent annually from 1990 to 2025, which is pretty consistent with other momentum-based 
algorithms, and beats the market by a large margin.
