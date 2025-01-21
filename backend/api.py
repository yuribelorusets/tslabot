import requests
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual Polygon.io API key
API_KEY = 'JKge37H5qEXX5o9eNWqjY5ZoipFTPTRr'
NEWS_BASE_URL = 'https://api.polygon.io/v2/reference/news'
STOCK_BASE_URL = 'https://api.polygon.io/v1/open-close/{ticker}/{date}'

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
