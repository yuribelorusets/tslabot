import pandas as pd
from datetime import datetime

def prepare_dataset(news_data, stock_data):
    dataset = []
    for article in news_data:
        # Extract sentiment data
        sentiment = article['insights'][0]['sentiment'] if article.get('insights') else 'neutral'
        sentiment_reasoning = article['insights'][0]['sentiment_reasoning'] if article.get('insights') else None

        # Extract article URL
        url = article.get('article_url', 'N/A')

        # Extract date and convert to datetime
        pub_date = datetime.fromisoformat(article['published_utc'].replace('Z', '+00:00'))

        # Get stock prices
        open_price = stock_data.get(pub_date.date(), {}).get('open', None)
        close_price = stock_data.get(pub_date.date(), {}).get('close', None)
        volume = stock_data.get(pub_date.date(), {}).get('volume', None)

        # Calculate price change
        price_change = ((close_price - open_price) / open_price) * 100 if open_price and close_price else None

        # Append the relevant data to the dataset
        dataset.append({
            'date': pub_date,
            'ticker': article['tickers'][0] if article.get('tickers') else None,
            'title': article['title'],
            'description': article['description'],
            'url': url,
            'sentiment': sentiment,
            'sentiment_reasoning': sentiment_reasoning,
            'keywords': ', '.join(article.get('keywords', [])),
            'open_price': open_price,
            'close_price': close_price,
            'price_change': price_change,
            'volume' : volume
        })

    return pd.DataFrame(dataset)

# Assuming you have the Polygon news data and stock price data
# news_data = polygon_news_response  # Your Polygon.io news API response
# stock_prices = get_stock_prices()  # Function to get stock prices for relevant dates

# Create the dataset
# training_data = prepare_dataset(news_data, stock_prices)
