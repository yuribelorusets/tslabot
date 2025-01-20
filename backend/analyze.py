import requests
from api import API_KEY, NEWS_BASE_URL, STOCK_BASE_URL  # Import necessary constants and URLs from api.py

# GPT API configuration
GPT_API_URL = 'https://api.openai.com/v1/chat/completions'  # Replace with your GPT endpoint
GPT_API_KEY = 'YOUR_GPT_API_KEY'  # Replace with your actual GPT API key

# Function to analyze sentiment using GPT for multiple headlines
def analyze_sentiments(news_data, price_before):
    sentiments = []

    for article in news_data:
        headline = article['title']
        # Simulate price after news (you would need to fetch this data)
        price_after = price_before * 1.02  # Example: price increased by 2%

        # Prepare the request for sentiment analysis
        headers = {
            'Authorization': f'Bearer {GPT_API_KEY}',
            'Content-Type': 'application/json'
        }
        prompt = f"Analyze the sentiment of the following headline: '{headline}'. " \
                 f"Price before news: {price_before}, Price after news: {price_after}. " \
                 f"What is the sentiment and how does it relate to the price reaction?"

        data = {
            'model': 'gpt-3.5-turbo',  # Use the standard GPT model
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150
        }

        # Send the request to the GPT API
        response = requests.post(GPT_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            sentiment = response.json()['choices'][0]['message']['content']
            sentiments.append((headline, sentiment))
        else:
            print(f"Error analyzing sentiment: {response.status_code}, {response.text}")
            sentiments.append((headline, None))  # Append None for failed requests

    return sentiments