import unittest
from main import CurrencyChecker


class TestCurrencyCheckerSimple(unittest.TestCase):
    """7 основных тестов для CurrencyChecker"""

    def setUp(self):
        self.checker = CurrencyChecker()

    def test1_basic_currencies(self):
        """Базовые валюты"""
        text = "$100, 50 EUR, ₽1,500"
        results = self.checker.find_currency_amounts(text)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], ("USD", "100"))
        self.assertEqual(results[1], ("EUR", "50"))
        self.assertEqual(results[2], ("RUB", "1500"))

    def test2_decimal_amounts(self):
        """Дробные суммы"""
        text = "$99.99, 49.50 EUR"
        results = self.checker.find_currency_amounts(text)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ("USD", "99.99"))

    def test3_empty_cases(self):
        """Пустые случаи"""
        self.assertEqual(self.checker.find_currency_amounts(""), [])
        self.assertEqual(self.checker.find_currency_amounts("Просто текст"), [])

    def test5_supported_currencies(self):
        """Список валют"""
        currencies = self.checker.get_supported_currencies()
        self.assertIn('USD', currencies)
        self.assertIn('EUR', currencies)
        self.assertIn('RUB', currencies)

    def test6_parse_currency(self):
        """Парсинг валют"""
        amount, currency = self.checker._parse_currency_amount("$100")
        self.assertEqual(amount, "100")
        self.assertEqual(currency, "USD")

    def test7_valid_amount(self):
        """Валидность суммы"""
        self.assertTrue(self.checker._is_valid_amount("100"))
        self.assertTrue(self.checker._is_valid_amount("100.50"))
        self.assertFalse(self.checker._is_valid_amount("100.123"))


if __name__ == '__main__':
    unittest.main()