import yfinance as yf

# беремо ціну з yfinance

def fetch_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")
        if not history.empty:
            return history.iloc[-1]['Close']
    except Exception as e:
        print(f"Error fetching stock price for {symbol}: {e}")
    return None