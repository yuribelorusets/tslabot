import unittest
from unittest.mock import patch
from api import fetch_news, fetch_stock_data, fetch_market_holidays

class TestApiFunctions(unittest.TestCase):

    @patch('api.requests.get')
    def test_fetch_news_success(self, mock_get):
        # Mock the response for fetch_news
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [
                {
                    "title": "Test News",
                    "published_utc": "2024-06-24T18:33:53Z",
                    "insights": [{"sentiment": "positive", "sentiment_reasoning": "Good news"}],
                    "tickers": ["TSLA"],
                    "article_url": "https://example.com/test-news"
                }
            ]
        }

        news = fetch_news('TSLA')
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]['title'], 'Test News')

    @patch('api.requests.get')
    def test_fetch_stock_data_success(self, mock_get):
        # Mock the response for fetch_stock_data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "open": 100,
            "close": 105,
            "volume": 1000
        }

        stock_data = fetch_stock_data('TSLA', '2024-06-24')
        self.assertEqual(stock_data['open'], 100)
        self.assertEqual(stock_data['close'], 105)

    @patch('api.requests.get')
    def test_fetch_market_holidays_success(self, mock_get):
        # Mock the response for fetch_market_holidays
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "date": "2024-06-24",
                "exchange": "NYSE",
                "name": "Market Holiday",
                "status": "closed"
            }
        ]

        market_holidays = fetch_market_holidays()
        self.assertEqual(len(market_holidays), 1)
        self.assertEqual(market_holidays[0]['name'], "Market Holiday")

if __name__ == '__main__':
    unittest.main()