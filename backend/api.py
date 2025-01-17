import requests
from datetime import datetime, timedelta

# Replace 'YOUR_API_KEY' with your actual Polygon.io API key
API_KEY = 'JKge37H5qEXX5o9eNWqjY5ZoipFTPTRr'
NEWS_BASE_URL = 'https://api.polygon.io/v2/reference/news'
STOCK_BASE_URL = 'https://api.polygon.io/v1/open-close/{ticker}/{date}'

# Define parameters for the news request
news_params = {
    'ticker': 'TSLA',  # Tesla's stock ticker
    'limit': 10,       # Limit to 10 articles
    'order': 'desc',   # Get the latest news first
    'sort': 'published_utc',  # Sort by publication date
    'apiKey': API_KEY  # Your API key
}

# Make the request to Polygon.io for news
news_response = requests.get(NEWS_BASE_URL, params=news_params)

# Check if the news request was successful
if news_response.status_code == 200:
    news_data = news_response.json()
    for article in news_data['results']:
        print(f"Title: {article['title']}")
        print(f"Published Date: {article['published_utc']}")
        print(f"Description: {article['description']}\n")
else:
    print(f"Error fetching news: {news_response.status_code}, {news_response.text}")

# Define parameters for the stock price request
ticker = 'TSLA'
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Use yesterday's date

# Make the request to Polygon.io for stock price
stock_response = requests.get(STOCK_BASE_URL.format(ticker=ticker, date=yesterday), params={'apiKey': API_KEY})

# Check if the stock price request was successful
if stock_response.status_code == 200:
    stock_data = stock_response.json()
    print(f"Stock Data for {ticker} on {yesterday}:")
    print(f"Open: {stock_data['open']}")
    print(f"Close: {stock_data['close']}")
    print(f"High: {stock_data['high']}")
    print(f"Low: {stock_data['low']}")

    # Print premarket and after-hours data if available
    if 'preMarket' in stock_data:
        print(f"Premarket Data: {stock_data['preMarket']}")
    if 'afterHours' in stock_data:
        print(f"Afterhours Data: {stock_data['afterHours']}\n")
else:
    print(f"Error fetching stock data: {stock_response.status_code}, {stock_response.text}")
