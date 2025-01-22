from api import fetch_news, fetch_stock_data, fetch_market_holidays, fetch_rsi, fetch_sma, fetch_macd  # Import functions from api.py and fetch_rsi
from datetime import datetime, timedelta, time

def is_market_open(date):
    # Check if the date is a weekend (Saturday or Sunday)
    if date.weekday() >= 5:  # Saturday or Sunday
        return False

    # Fetch market holidays from the Polygon API
    market_holidays = fetch_market_holidays()

    if market_holidays:
        # Check if the date is in the market holidays response
        for holiday in market_holidays:
            if holiday['date'] == date.strftime('%Y-%m-%d') and holiday['status'] == 'closed':
                return False

    return True  # The market is open if it's not a weekend and not a holiday

def next_trading_day(start_date):
    # Increment the date until we find a weekday (Monday to Friday)
    next_day = start_date + timedelta(days=1)
    while not is_market_open(next_day):
        next_day += timedelta(days=1)
    return next_day

def get_sma_and_macd(pub_date):
    date = pub_date.strftime('%Y-%m-%d')

    macd = fetch_macd(date)
    sma = fetch_sma(date)

    return sma, macd

def get_price_before_and_after_news(pub_date, stock_data):
    market_open_time = time(9, 30)  # Market opens at 9:30 AM
    market_close_time = time(16, 0)  # Market closes at 4:00 PM

    # Extract relevant prices from the stock data
    pre_market_price = stock_data.get('preMarket', None)
    open_price = stock_data.get('open', None)
    close_price = stock_data.get('close', None)
    after_hours_price = stock_data.get('afterHours', None)

    # Initialize price_before and price_after
    price_before = None
    price_after = None

    # Determine price before the news and set before_timestamp
    if pub_date.time() < market_open_time:
        # Article published before market opens
        price_before = pre_market_price
        before_timestamp = int(pub_date.timestamp() * 1000)  # Convert to milliseconds
    elif market_open_time <= pub_date.time() <= market_close_time:
        # Article published during market hours
        price_before = open_price  # Use the open price of the current day
        before_timestamp = int(pub_date.timestamp() * 1000)  # Convert to milliseconds
    else:
        # Article published after market closes
        price_before = close_price
        before_timestamp = int(pub_date.timestamp() * 1000)  # Convert to milliseconds

    # Determine price after the news and set after_timestamp
    if pub_date.time() < market_close_time:
        # If published before market close, use the closing price of the current day as price_after
        price_after = close_price
        after_timestamp = int(pub_date.timestamp() * 1000)  # Use the same timestamp for after
    else:
        # If published after market close, use the opening price of the next trading day
        next_day = next_trading_day(pub_date.date())
        next_day_stock_data = fetch_stock_data(stock_data['symbol'], next_day.strftime('%Y-%m-%d'))  # Fetch next day's data
        price_after = next_day_stock_data.get('close', None) if next_day_stock_data else None
        after_timestamp = int(next_day.timestamp() * 1000)  # Convert to milliseconds for the next trading day

    # Fetch RSI values
    rsi_before, rsi_after = fetch_rsi(stock_data['symbol'], before_timestamp, after_timestamp)

    return price_before, price_after, rsi_before, rsi_after
