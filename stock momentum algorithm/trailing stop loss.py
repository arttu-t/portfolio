import pandas as pd
import yfinance as yf

# Load CSV with tickers per date
df = pd.read_csv('tickers_by_date.csv', parse_dates=['date'])

# Normalize dates to first of each month
df['date'] = df['date'].dt.to_period('M').dt.to_timestamp()
df = df.drop_duplicates(subset='date')

# Build monthly start dates from Jan 2018 to Jan 2025
start_date = pd.to_datetime('1995-01-01')
end_date   = pd.to_datetime('2025-01-01')
months = pd.date_range(start=start_date, end=end_date, freq='MS')

# Gather all tickers in that span (for bulk download)
tickers_set = set()
for d in months:
    row = df[df['date'] == d]
    if not row.empty:
        tickers_set.update(row.iloc[0]['tickers'].split(','))


tickers_all = sorted(tickers_set)

#removes tickers with wrong/missing data
tickers_all.remove('BDK')
tickers_all.remove('CBE')
tickers_all.remove('TIE')
tickers_all.remove('ACS')
tickers_all.remove('BSC')

# Download price data once (start 6 months earlier to compute momentum)
price_data = yf.download(
    tickers_all,
    start=(start_date - pd.DateOffset(months=6)).strftime('%Y-%m-%d'),
    end=(end_date + pd.DateOffset(months=1)).strftime('%Y-%m-%d'),
    auto_adjust=True
)['Close']



# Parameters
stop_loss_pct = 0.15
portfolio_value = 1.0
log = []

for ekadate in months:
    # Get tickers active on the 1st of this month
    row = df[df['date'] == ekadate]
    if row.empty:
        continue
    tickers = row.iloc[0]['tickers'].split(',')
    tickers = [t for t in tickers if t in price_data.columns]
    if not tickers:
        continue

    # Define the momentum window (t‑7 to t‑2 months)
    momentum_start = ekadate - pd.DateOffset(months=7)
    momentum_end = ekadate - pd.DateOffset(months=2)
    momentum_window = price_data[tickers].loc[momentum_start:momentum_end]

    if momentum_window.shape[0] < 2:
        continue

    momentum = momentum_window.iloc[-1] / momentum_window.iloc[0] - 1
    momentum = momentum.dropna()
    if momentum.empty:
        continue

    top_stocks = momentum.nlargest(10).index.tolist()

    # Price data for the current month
    month_end = ekadate + pd.offsets.MonthEnd(0)
    in_month = price_data[top_stocks].loc[ekadate:month_end]

    individual_returns = {}

    for stock in top_stocks:
        prices = in_month[stock].dropna()
        if len(prices) < 2:
            individual_returns[stock] = None
            continue

        start_price = prices.iloc[0]
        peak_price = start_price
        exit_price = prices.iloc[-1]

        # Trailing stop logic
        for price in prices[1:]:
            # update peak
            if price > peak_price:
                peak_price = price
            # check drawdown
            if 1 - (price / peak_price) > stop_loss_pct:
                # sell at the exact stop level
                exit_price = peak_price * (1 - stop_loss_pct)
                break

        individual_returns[stock] = (exit_price / start_price) - 1


    # Calculate portfolio return
    valid_returns = [r for r in individual_returns.values() if r is not None]
    if not valid_returns:
        continue
    portfolio_return = sum(valid_returns) / len(valid_returns)
    portfolio_value *= (1 + portfolio_return)

    # Log results
    log.append({
        'date': ekadate.strftime('%Y-%m-%d'),
        'top_momentum': top_stocks,
        'individual_returns_%': {s: round(r * 100, 2) if r is not None else None
                                 for s, r in individual_returns.items()},
        'portfolio_return_%': round(portfolio_return * 100, 2),
        'portfolio_value': round(portfolio_value, 4)
    })


results_df = pd.DataFrame(log)
results_df.to_csv('momentum_results_1995_2025_trailing015.csv', index=False)

print("Full results saved to specified csv")