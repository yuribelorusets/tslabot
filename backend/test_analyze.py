import unittest
from unittest.mock import patch
from analyze import analyze_sentiments

class TestAnalyzeSentiments(unittest.TestCase):

    @patch('analyze.requests.post')
    def test_analyze_sentiments_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'choices': [{'message': {'content': 'Positive sentiment'}}]
        }

        news_data = [{'title': 'Test headline'}]
        price_before = 100
        sentiments = analyze_sentiments(news_data, price_before)

        self.assertEqual(len(sentiments), 1)
        self.assertEqual(sentiments[0][0], 'Test headline')
        self.assertEqual(sentiments[0][1], 'Positive sentiment')

    @patch('analyze.requests.post')
    def test_analyze_sentiments_failure(self, mock_post):
        mock_post.return_value.status_code = 500

        news_data = [{'title': 'Test headline'}]
        price_before = 100
        sentiments = analyze_sentiments(news_data, price_before)

        self.assertEqual(len(sentiments), 1)
        self.assertEqual(sentiments[0][0], 'Test headline')
        self.assertIsNone(sentiments[0][1])

if __name__ == '__main__':
    unittest.main()