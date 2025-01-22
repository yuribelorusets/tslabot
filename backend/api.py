import requests
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual Polygon.io API key
API_KEY = 'JKge37H5qEXX5o9eNWqjY5ZoipFTPTRr'
NEWS_BASE_URL = 'https://api.polygon.io/v2/reference/news'
STOCK_BASE_URL = 'https://api.polygon.io/v1/open-close/{ticker}/{date}'
MARKET_HOLIDAYS_URL = 'https://api.polygon.io/v1/marketstatus/upcoming'
RSI_URL = 'https://api.polygon.io/v2/aggs/ticker/{ticker}/rsi'
MACD_URL = 'https://api.polygon.io/v2/aggs/ticker/{ticker}/macd'
SMA_URL = 'https://api.polygon.io/v2/aggs/ticker/{ticker}/sma'

def fetch_news(ticker='TSLA', limit=10):
    news_params = {
        'ticker': ticker,
        'limit': limit,
        'order': 'desc',
        'sort': 'published_utc',
        'apiKey': API_KEY
    }
    news_response = requests.get(NEWS_BASE_URL, params=news_params)

    if news_response.status_code == 200:
        return news_response.json()['results']
    else:
        print(f"Error fetching news: {news_response.status_code}, {news_response.text}")
        return None

def fetch_stock_data(ticker='TSLA', date=None):
    if date is None:
        # Default to yesterday if no date is provided
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        # Ensure the date is in the correct format (YYYY-MM-DD)
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')

    stock_response = requests.get(STOCK_BASE_URL.format(ticker=ticker, date=date), params={'apiKey': API_KEY})

    if stock_response.status_code == 200:
        return stock_response.json()
    else:
        print(f"Error fetching stock data: {stock_response.status_code}, {stock_response.text}")
        return None

def fetch_market_holidays():
    """Fetch the upcoming market closures from the Polygon API."""
    response = requests.get(MARKET_HOLIDAYS_URL, params={'apiKey': API_KEY})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching market holidays: {response.status_code}, {response.text}")
        return None

def fetch_rsi(ticker, before_timestamp, after_timestamp, period=14):
    """Fetch the Relative Strength Index (RSI) for a given ticker at two timestamps."""

    # Fetch RSI for the "before" timestamp
    params_before = {
        'apiKey': API_KEY,
        'period': period,
        'timestamp': before_timestamp
    }
    rsi_response_before = requests.get(RSI_URL.format(ticker=ticker), params=params_before)
    rsi_value_before = None
    if rsi_response_before.status_code == 200:
        data_before = rsi_response_before.json()
        if data_before.get("status") == "OK" and "results" in data_before:
            rsi_values_before = data_before["results"].get("values", [])
            if rsi_values_before:
                rsi_value_before = rsi_values_before[0]["value"]

    # Fetch RSI for the "after" timestamp
    params_after = {
        'apiKey': API_KEY,
        'period': period,
        'timestamp': after_timestamp
    }
    rsi_response_after = requests.get(RSI_URL.format(ticker=ticker), params=params_after)
    rsi_value_after = None
    if rsi_response_after.status_code == 200:
        data_after = rsi_response_after.json()
        if data_after.get("status") == "OK" and "results" in data_after:
            rsi_values_after = data_after["results"].get("values", [])
            if rsi_values_after:
                rsi_value_after = rsi_values_after[0]["value"]

    return rsi_value_before, rsi_value_after

def fetch_macd(date, short_period=12, long_period=26, signal_period=9):
    """Fetch the Moving Average Convergence Divergence (MACD) for TSLA at a given date."""
    # Convert date to timestamp in milliseconds
    timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000)

    params = {
        'apiKey': API_KEY,
        'short': short_period,
        'long': long_period,
        'signal': signal_period,
        'timestamp': timestamp  # Pass the timestamp as a parameter
    }
    macd_response = requests.get(MACD_URL.format(ticker='TSLA'), params=params)

    if macd_response.status_code == 200:
        data = macd_response.json()
        if data.get("status") == "OK" and "results" in data:
            # Extract the MACD values
            macd_values = data["results"].get("values", [])
            if macd_values:
                # Return the most recent MACD value, signal, and histogram
                latest_macd = macd_values[0]  # Get the latest entry
                return {
                    "macd": latest_macd["value"],
                    "signal": latest_macd["signal"],
                    "histogram": latest_macd["histogram"],
                    "timestamp": latest_macd["timestamp"]
                }
        else:
            print("No results found in MACD response.")
            return None
    else:
        print(f"Error fetching MACD: {macd_response.status_code}, {macd_response.text}")
        return None

def fetch_sma(date, period=14):
    """Fetch the Simple Moving Average (SMA) for TSLA at a given date."""
    # Convert date to timestamp in milliseconds
    timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000)

    params = {
        'apiKey': API_KEY,
        'period': period,
        'timestamp': timestamp  # Pass the timestamp as a parameter
    }
    sma_response = requests.get(SMA_URL.format(ticker='TSLA'), params=params)

    if sma_response.status_code == 200:
        data = sma_response.json()
        if data.get("status") == "OK" and "results" in data:
            sma_values = data["results"].get("values", [])
            if sma_values:
                # Return the most recent SMA value
                return sma_values[0]["value"]
        else:
            print("No results found in SMA response.")
            return None
    else:
        print(f"Error fetching SMA: {sma_response.status_code}, {sma_response.text}")
        return None