import re

class CurrencyChecker:
    def __init__(self):
        # Расширенное регулярное выражение для поиска валютных сумм
        self.currency_pattern = re.compile(
            r'''
            (?:                         # Незахватывающая группа для вариантов
                (?:USD|EUR|RUB|GBP|JPY|CNY|CHF|CAD|AUD|UAH|KZT|BYN|₽|$|€|£|¥)\s* # Валюта перед суммой
                \d{1,3}(?:,\d{3})*     # Целая часть с разделителями тысяч
                (?:\.\d{1,2})?         # Дробная часть 
            |
                \d{1,3}(?:,\d{3})*     # Целая часть с разделителями тысяч
                (?:\.\d{1,2})?         # Дробная часть 
                \s*(?:USD|EUR|RUB|GBP|JPY|CNY|CHF|CAD|AUD|UAH|KZT|BYN|₽|$|€|£|¥) # Валюта после суммы
            )
            ''',
            re.VERBOSE | re.IGNORECASE
        )

        # Словарь символов валют и их кодов
        self.currency_symbols = {
            '$': 'USD',
            '€': 'EUR',
            '£': 'GBP',
            '¥': 'JPY',
            '₽': 'RUB'
        }

        # Полный список поддерживаемых валют
        self.supported_currencies = [
            'USD', 'EUR', 'RUB', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD',
            'AUD', 'UAH', 'KZT', 'BYN'
        ]

def main():
    pass

if __name__ == "__main__":
    main()