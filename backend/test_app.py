import unittest
from datetime import datetime, timedelta
from app import is_market_open, next_trading_day

class TestAppFunctions(unittest.TestCase):

    def test_is_market_open_weekday(self):
        self.assertTrue(is_market_open(datetime(2023, 6, 26)))  # Monday
        self.assertTrue(is_market_open(datetime(2023, 6, 27)))  # Tuesday
        self.assertTrue(is_market_open(datetime(2023, 6, 28)))  # Wednesday
        self.assertTrue(is_market_open(datetime(2023, 6, 29)))  # Thursday
        self.assertTrue(is_market_open(datetime(2023, 6, 30)))  # Friday

    def test_is_market_open_weekend(self):
        self.assertFalse(is_market_open(datetime(2023, 6, 24)))  # Saturday
        self.assertFalse(is_market_open(datetime(2023, 6, 25)))  # Sunday

    def test_next_trading_day(self):
        self.assertEqual(next_trading_day(datetime(2023, 6, 30)), datetime(2023, 7, 3))  # Friday to Monday
        self.assertEqual(next_trading_day(datetime(2023, 7, 1)), datetime(2023, 7, 3))  # Saturday to Monday
        self.assertEqual(next_trading_day(datetime(2023, 7, 2)), datetime(2023, 7, 3))  # Sunday to Monday

if __name__ == '__main__':
    unittest.main()