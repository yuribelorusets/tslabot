import unittest
import pandas as pd
from data import prepare_dataset

class TestDataFunctions(unittest.TestCase):

    def test_prepare_dataset(self):
        news_data = [
            {
                'published_utc': '2024-06-24T18:33:53Z',
                'insights': [{'sentiment': 'positive', 'sentiment_reasoning': 'Good news'}],
                'tickers': ['TSLA'],
                'title': 'Tesla Stock Rises',
                'description': 'Tesla stock is on the rise.',
                'keywords': ['Tesla', 'Stock', 'Market']
            }
        ]
        stock_data = {
            pd.to_datetime('2024-06-24').date(): {'open': 100, 'close': 105}
        }

        df = prepare_dataset(news_data, stock_data)

        self.assertEqual(len(df), 1)
        self.assertEqual(df['title'][0], 'Tesla Stock Rises')
        self.assertEqual(df['sentiment'][0], 'positive')
        self.assertEqual(df['open_price'][0], 100)
        self.assertEqual(df['close_price'][0], 105)
        self.assertEqual(df['price_change'][0], 5.0)  # ((105 - 100) / 100) * 100

if __name__ == '__main__':
    unittest.main()