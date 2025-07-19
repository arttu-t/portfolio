#this is a simple tool for analysing individual stocks. Feel free to add more key figures or edit the code to your liking
#data might be limited, because yahoo finance has limited key figures for some companies
import yfinance as yf

while True:
    def get_data(ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            print("key figures for", info.get("longName", "N/A"))
            print("Sector:", info.get("sector", "N/A"))
            market_cap = info.get("marketCap", "N/A")
            rounded_market_cap = round(market_cap / 1e9)  # Convert to billions and round
            print("Market Cap:", f"${rounded_market_cap}B")
            #calculate and print other key figures
            trailing_pe = info.get("trailingPE", "N/A")
            print("trailing p/e:", trailing_pe)
            forward_pe = info.get("forwardPE", "N/A")
            print("forward p/e:", forward_pe)
            print("p/b:", info.get("priceToBook", "N/A"))
            print("trailing PEG:", info.get("trailingPegRatio", "N/A"))
            
            #calculate momentum from 12 months
            hist = stock.history(period="1y", interval="1d")["Close"]
            if len(hist) >= 2:
                first_price = hist.iloc[0]
                last_price = hist.iloc[-1]
                mom = (last_price / first_price - 1) * 100
                print(f"12-Month Momentum: {mom:.2f}% "
                    f"(from {hist.index[0].date()} → {hist.index[-1].date()})")
            else:
                print("\nNot enough historical data to compute 12-month momentum.")

            pass
            
        
        except:
            print("something went wrong, try again") #most likely a network error
            pass 
        
    if __name__ == "__main__":

        ticker = input("\nGive stock ticker (eg. AAPL for apple) ")
        get_data(ticker)

   
