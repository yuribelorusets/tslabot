import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from app import is_market_open, next_trading_day

class TestAppFunctions(unittest.TestCase):

    @patch('app.fetch_market_holidays')  # Mock the fetch_market_holidays function as imported in app.py
    def test_is_market_open_weekday(self, mock_fetch_market_holidays):
        mock_fetch_market_holidays.return_value = []  # Simulate no holidays
        self.assertTrue(is_market_open(datetime(2023, 6, 26)))  # Monday
        self.assertTrue(is_market_open(datetime(2023, 6, 27)))  # Tuesday
        self.assertTrue(is_market_open(datetime(2023, 6, 28)))  # Wednesday
        self.assertTrue(is_market_open(datetime(2023, 6, 29)))  # Thursday
        self.assertTrue(is_market_open(datetime(2023, 6, 30)))  # Friday

    @patch('app.fetch_market_holidays')  # Mock the fetch_market_holidays function
    def test_is_market_open_weekend(self, mock_fetch_market_holidays):
        mock_fetch_market_holidays.return_value = []  # Simulate no holidays
        self.assertFalse(is_market_open(datetime(2023, 6, 24)))  # Saturday
        self.assertFalse(is_market_open(datetime(2023, 6, 25)))  # Sunday

    @patch('app.fetch_market_holidays')  # Mock the fetch_market_holidays function
    def test_is_market_open_holiday(self, mock_fetch_market_holidays):
        # Simulate a holiday on June 26, 2023
        mock_fetch_market_holidays.return_value = [
            {"date": "2023-06-26", "exchange": "NYSE", "name": "Market Holiday", "status": "closed"}
        ]
        self.assertFalse(is_market_open(datetime(2023, 6, 26)))  # Holiday

    @patch('app.fetch_market_holidays')  # Mock the fetch_market_holidays function
    def test_next_trading_day(self, mock_fetch_market_holidays):
        mock_fetch_market_holidays.return_value = []  # Simulate no holidays
        self.assertEqual(next_trading_day(datetime(2023, 6, 30)), datetime(2023, 7, 3))  # Friday to Monday
        self.assertEqual(next_trading_day(datetime(2023, 7, 1)), datetime(2023, 7, 3))  # Saturday to Monday
        self.assertEqual(next_trading_day(datetime(2023, 7, 2)), datetime(2023, 7, 3))  # Sunday to Monday

if __name__ == '__main__':
    unittest.main()