import unittest
from unittest.mock import patch
from api import fetch_news, fetch_stock_data

class TestApiFunctions(unittest.TestCase):

    @patch('api.requests.get')
    def test_fetch_news_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 1,
            "next_url": "https://api.polygon.io:443/v2/reference/news?cursor=eyJsaW1pdCI6MSwic29ydCI6InB1Ymxpc2hlZF91dGMiLCJvcmRlciI6ImFzY2VuZGluZyIsInRpY2tlciI6e30sInB1Ymxpc2hlZF91dGMiOnsiZ3RlIjoiMjAyMS0wNC0yNiJ9LCJzZWFyY2hfYWZ0ZXIiOlsxNjE5NDA0Mzk3MDAwLG51bGxdfQ",
            "request_id": "831afdb0b8078549fed053476984947a",
            "results": [
                {
                    "amp_url": "https://m.uk.investing.com/news/stock-market-news/markets-are-underestimating-fed-cuts-ubs-3559968?ampMode=1",
                    "article_url": "https://uk.investing.com/news/stock-market-news/markets-are-underestimating-fed-cuts-ubs-3559968",
                    "author": "Sam Boughedda",
                    "description": "UBS analysts warn that markets are underestimating the extent of future interest rate cuts by the Federal Reserve, as the weakening economy is likely to justify more cuts than currently anticipated.",
                    "id": "8ec638777ca03b553ae516761c2a22ba2fdd2f37befae3ab6fdab74e9e5193eb",
                    "image_url": "https://i-invdn-com.investing.com/news/LYNXNPEC4I0AL_L.jpg",
                    "insights": [
                        {
                            "sentiment": "positive",
                            "sentiment_reasoning": "UBS analysts are providing a bullish outlook on the extent of future Federal Reserve rate cuts, suggesting that markets are underestimating the number of cuts that will occur.",
                            "ticker": "UBS"
                        }
                    ],
                    "keywords": [
                        "Federal Reserve",
                        "interest rates",
                        "economic data"
                    ],
                    "published_utc": "2024-06-24T18:33:53Z",
                    "publisher": {
                        "favicon_url": "https://s3.polygon.io/public/assets/news/favicons/investing.ico",
                        "homepage_url": "https://www.investing.com/",
                        "logo_url": "https://s3.polygon.io/public/assets/news/logos/investing.png",
                        "name": "Investing.com"
                    },
                    "tickers": [
                        "UBS"
                    ],
                    "title": "Markets are underestimating Fed cuts: UBS By Investing.com - Investing.com UK"
                }
            ],
            "status": "OK"
        }

        news = fetch_news('TSLA')
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]['title'], 'Markets are underestimating Fed cuts: UBS By Investing.com - Investing.com UK')
        self.assertEqual(news[0]['insights'][0]['sentiment'], 'positive')

    @patch('api.requests.get')
    def test_fetch_news_failure(self, mock_get):
        mock_get.return_value.status_code = 500

        news = fetch_news('TSLA')
        self.assertIsNone(news)

    @patch('api.requests.get')
    def test_fetch_stock_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'open': 100,
            'close': 105
        }

        stock_data = fetch_stock_data('TSLA', '2023-06-24')
        self.assertEqual(stock_data['open'], 100)
        self.assertEqual(stock_data['close'], 105)

    @patch('api.requests.get')
    def test_fetch_stock_data_failure(self, mock_get):
        mock_get.return_value.status_code = 500

        stock_data = fetch_stock_data('TSLA', '2023-06-24')
        self.assertIsNone(stock_data)

if __name__ == '__main__':
    unittest.main()