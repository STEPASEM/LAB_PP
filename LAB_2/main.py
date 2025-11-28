import re
import requests
from bs4 import BeautifulSoup


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

    def find_currency_amounts(self, text):
        """Находит все валютные суммы в тексте"""
        matches = []
        for match in self.currency_pattern.finditer(text):
            amount_str = match.group(0)
            # Извлекаем валюту и сумму
            currency, amount = self._parse_currency_amount(amount_str)
            if currency and amount:
                matches.append((amount, currency))
        return matches

    def _parse_currency_amount(self, amount_str):
        """Парсит строку с валютной суммой на составляющие"""
        # Удаляем лишние пробелы
        amount_str = amount_str.strip()

        # Определяем валюту
        currency = None

        # Сначала проверяем символьные обозначения
        for symbol, curr_code in self.currency_symbols.items():
            if symbol in amount_str:
                currency = curr_code
                amount_str = amount_str.replace(symbol, '').strip()
                break

        # Если не нашли символ, ищем текстовые обозначения
        if currency is None:
            for curr_code in self.supported_currencies:
                if curr_code.upper() in amount_str.upper():
                    currency = curr_code
                    amount_str = amount_str.upper().replace(curr_code.upper(), '').strip()
                    break

        # Очищаем сумму от запятых
        amount_clean = amount_str.replace(',', '').strip()

        # Проверяем, что после очистки у нас осталась валидная сумма
        if not self._is_valid_amount(amount_clean):
            return None, None

        return amount_clean, currency

    def _is_valid_amount(self, amount_str):
        """Проверяет, является ли строка валидной денежной суммой"""
        if not amount_str:
            return False

        # Проверяем формат: целое число или число с плавающей точкой
        amount_pattern = re.compile(r'^\d+(?:\.\d{1,2})?$')
        return amount_pattern.match(amount_str) is not None

    def get_supported_currencies(self):
        """Возвращает список поддерживаемых валют"""
        return self.supported_currencies

    def get_currency_from_url(self, url):
        """Загружает текст с веб-страницы и ищет валютные суммы"""

        print(f"🔄 Загружаю страницу: {url}")
        response = requests.get(url)
        response.raise_for_status()

        # Создаем BeautifulSoup объект
        soup = BeautifulSoup(response.content, 'html.parser')

        # Удаляем скрипты и стили чтобы получить чистый текст
        for script in soup(["script", "style"]):
            script.decompose()

        # Получаем чистый текст страницы
        page_text = soup.get_text()

        print(f"📄 Размер текста: {len(page_text)} символов")

        # Ищем валютные суммы в очищенном тексте
        return self.find_currency_amounts(page_text)

    def process_file(self, filename):
        """Читает файл и ищет валютные суммы"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            return self.find_currency_amounts(content)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

def main():
    checker = CurrencyChecker()

    print("=== Проверка и поиск валютных сумм ===")
    print("Поддерживаемые валюты:", ", ".join(checker.get_supported_currencies()))
    print("Символы валют: $ (USD), € (EUR), £ (GBP), ¥ (JPY), ₽ (RUB)")
    print("\nВыберите режим работы:")
    print("1 - Поиск в тексте")
    print("2 - Загрузить из файла")
    print("3 - Загрузить по URL")

    choice = input("Ваш выбор (1-3): ").strip()

    if choice == '1':
        # Поиск в тексте
        text = input("Введите текст для поиска: ")
        amounts = checker.find_currency_amounts(text)
        if amounts:
            print("Найденные валютные суммы:")
            for amount, currency in amounts:
                print(f"- {amount} {currency}")
        else:
            print("Валютные суммы не найдены")

    elif choice == '2':
        # Загрузка из файла
        filename = input("Введите имя файла: ")
        amounts = checker.process_file(filename)
        if amounts:
            print("Найденные валютные суммы:")
            for amount, currency in amounts:
                print(f"- {amount} {currency}")
        else:
            print("Валютные суммы не найдены")

    elif choice == '3':
        # Загрузка по URL
        url = input("Введите URL: ")
        amounts = checker.get_currency_from_url(url)
        if amounts:
            print("Найденные валютные суммы:")
            for amount, currency in amounts:
                print(f"- {amount} {currency}")
        else:
            print("Валютные суммы не найдены")
    else:
        print("Неверный выбор")

if __name__ == "__main__":
    main()