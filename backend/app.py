from helper import get_price_before_and_after_news, get_sma_and_macd
from api import fetch_news, fetch_stock_data, fetch_market_holidays  # Import functions from api.py
from analyze import analyze_sentiments  # Import the sentiment analysis function from analyze.py
from data import prepare_dataset  # Import the updated prepare_dataset function
from datetime import datetime, timedelta
import pandas as pd

def main():
    ticker = 'TSLA'

    # Fetch news data
    news_data = fetch_news(ticker)

    # Dictionary to store fetched stock data
    stock_data_cache = {}

    # List to hold prepared dataset
    prepared_data = []

    # Analyze sentiment and check price impact for each news article
    for article in news_data:
        pub_date = datetime.fromisoformat(article['published_utc'].replace('Z', '+00:00'))

        # Check if stock data for the target date has already been fetched
        if pub_date not in stock_data_cache:
            stock_data = fetch_stock_data(ticker, pub_date.strftime('%Y-%m-%d'))  # Fetch stock data for the target date
            stock_data_cache[pub_date] = stock_data  # Cache the fetched data
        else:
            stock_data = stock_data_cache[pub_date]  # Use cached data

        price_before, price_after, rsi_before, rsi_after = get_price_before_and_after_news(pub_date, stock_data)

        sma, macd = get_sma_and_macd(pub_date)

        # Add features to stock_data
        stock_data['price_before'], stock_data['price_after'], stock_data['rsi_before'],
        stock_data['rsi_after'], stock_data['sma'], stock_data['macd']
        = price_before, price_after, rsi_before, rsi_after, sma, macd

        # Prepare the dataset for the current article
        article_data = prepare_dataset(article, stock_data)
        prepared_data.append(article_data)  # Append the prepared data


        # Analyze sentiment
        # sentiment = analyze_sentiments([article], price_before)  # Pass the article for sentiment analysis
        # print(f"Headline: {article['title']}")
        # print(f"Sentiment: {sentiment[0][1] if sentiment else 'N/A'}")
        # print(f"Price Change: {price_change if price_change is not None else 'N/A'}%\n")

    # Convert the list of dictionaries to a DataFrame
    training_data = pd.DataFrame(prepared_data)
if __name__ == "__main__":
    main()