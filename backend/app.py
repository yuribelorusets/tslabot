from api import fetch_news, fetch_stock_data  # Import functions from api.py
from analyze import analyze_sentiment  # Import the sentiment analysis function from analyze.py
from datetime import datetime, timedelta

def main():
    ticker = 'TSLA'

    # Fetch news data
    news_data = fetch_news(ticker)

    # Fetch stock price data
    stock_data = fetch_stock_data(ticker)

    if stock_data:
        price_before = stock_data['close']  # Assuming this is the price before the news
    else:
        print("Stock data could not be fetched.")
        return

    # Analyze sentiment for each news article
    for article in news_data:
        headline = article['title']
        # Simulate price after news (you would need to fetch this data)
        price_after = price_before * 1.02  # Example: price increased by 2%

        # Analyze sentiment
        sentiment = analyze_sentiment(headline, price_before, price_after)
        print(f"Headline: {headline}")
        print(f"Sentiment: {sentiment}\n")

if __name__ == "__main__":
    main()