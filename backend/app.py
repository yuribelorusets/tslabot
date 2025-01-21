from api import fetch_news, fetch_stock_data, fetch_market_holidays  # Import functions from api.py
from analyze import analyze_sentiments  # Import the sentiment analysis function from analyze.py
from datetime import datetime, timedelta

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

def main():
    ticker = 'TSLA'

    # Fetch news data
    news_data = fetch_news(ticker)

    # Dictionary to store fetched stock data
    stock_data_cache = {}

    # Define market hours
    market_close_time = datetime.strptime("16:00", "%H:%M").time()

    # Analyze sentiment and check price impact for each news article
    for article in news_data:
        pub_date = datetime.fromisoformat(article['published_utc'].replace('Z', '+00:00'))

        # Determine the date for fetching stock data
        if pub_date.time() > market_close_time:
            # Article published after market close, fetch next day's opening price
            target_date = next_trading_day(pub_date.date() + timedelta(days=1))
        else:
            # Article published before market close, fetch today's closing price
            target_date = pub_date.date()

        # Check if stock data for the target date has already been fetched
        if target_date not in stock_data_cache:
            stock_data = fetch_stock_data(ticker, target_date.strftime('%Y-%m-%d'))  # Fetch stock data for the target date
            stock_data_cache[target_date] = stock_data  # Cache the fetched data
        else:
            stock_data = stock_data_cache[target_date]  # Use cached data

        # Get the price before the news
        if pub_date.time() > market_close_time:
            # Use the opening price of the next trading day
            price_before = stock_data.get('open', None)
        else:
            # Use the closing price of the current day
            price_before = stock_data.get('close', None)

        # Get the closing price for the day after the news for price change calculation
        if pub_date.time() > market_close_time:
            # If the article was published after market close, we need the next day's closing price
            next_day = target_date
            next_day_prices = stock_data_cache.get(next_day, {})
            close_price = next_day_prices.get('close', None)
        else:
            # If the article was published before market close, we can use the same day's closing price
            close_price = stock_data.get('close', None)

        # Calculate price change
        if price_before is not None and close_price is not None:
            price_change = ((close_price - price_before) / price_before) * 100
        else:
            price_change = None

        # Analyze sentiment
        sentiment = analyze_sentiments([article], price_before)  # Pass the article for sentiment analysis
        print(f"Headline: {article['title']}")
        print(f"Sentiment: {sentiment[0][1] if sentiment else 'N/A'}")
        print(f"Price Change: {price_change if price_change is not None else 'N/A'}%\n")

if __name__ == "__main__":
    main()