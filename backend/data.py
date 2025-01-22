import pandas as pd
from datetime import datetime

def prepare_dataset(article, stock_data):
    # Extract sentiment data
    sentiment = article['insights'][0]['sentiment'] if article.get('insights') else 'neutral'
    sentiment_reasoning = article['insights'][0]['sentiment_reasoning'] if article.get('insights') else None

    # Extract article URL
    url = article.get('article_url', 'N/A')

    # Extract date and convert to datetime
    pub_date = datetime.fromisoformat(article['published_utc'].replace('Z', '+00:00'))

    # Get stock prices
    price_before = stock_data.get('price_before', None)
    price_after = stock_data.get('price_after', None)
    open_price = stock_data.get('open', None)
    close_price = stock_data.get('close', None)
    volume = stock_data.get('volume', None)
    rsi_before = stock_data.get('rsi_before', None)
    rsi_after = stock_data.get('rsi_after', None)
    sma = stock_data.get('sma', None)
    macd = stock_data.get('macd', None)

    # Calculate price change
    price_change = ((close_price - open_price) / open_price) * 100 if open_price and close_price else None

    # Create a dictionary for the dataset
    data = {
        'date': pub_date,
        'price_before': price_before,
        'price_after' : price_after,
        'rsi_before' : rsi_before,
        'rsi_after' : rsi_after,
        'macd' : macd,
        'sma' : sma,
        'title': article['title'],
        'description': article['description'],
        'url': url,
        'sentiment': sentiment,
        'sentiment_reasoning': sentiment_reasoning,
        'keywords': ', '.join(article.get('keywords', [])),
        'open_price': open_price,
        'close_price': close_price,
        'price_change': price_change,
        'volume': volume
    }

    return data  # Return the single article's data as a dictionary

def normalize_dataframe(df):
    """Normalize specified numerical features in the DataFrame."""
    # List of features to normalize
    features_to_normalize = ['price_before', 'price_after', 'open_price', 'close_price', 'price_change', 'volume']

    # Normalize using min-max normalization
    for feature in features_to_normalize:
        if feature in df.columns:
            min_value = df[feature].min()
            max_value = df[feature].max()
            df[feature] = (df[feature] - min_value) / (max_value - min_value) if max_value > min_value else 0

    return df

