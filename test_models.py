import unittest
from app.future.models import *


class TestModels(unittest.TestCase):
    """
    Simple test cases for Futures and Prices models
    """

    def test_create_future(self):
        # self.assertEqual("a", "a")
        self.assertEqual(Future("test_future", "http://www.test.com").name,
                         "test_future")
        self.assertEqual(Future("test_future", "http://www.test.com").url,
                         "http://www.test.com")

    def test_create_price(self):
        self.assertEqual(Price(date='2019-10-10', price=123.45, future_id=99).date, '2019-10-10')
        self.assertEqual(Price(date='2019-10-10', price=123.45, future_id=99).price, 123.45)
        self.assertEqual(Price(date='2019-10-10', price=123.45, future_id=99).future_id, 99)




if __name__ == '__main__':
    unittest.main()
