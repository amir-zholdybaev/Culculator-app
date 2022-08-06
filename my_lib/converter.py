import os
import json
import datetime
import requests
from requests.exceptions import HTTPError


class Converter:
    months = [
        'января', 'февраля', 'марта', 'апреля',
        'мая', 'июня', 'июля', 'августа',
        'сентября', 'октября', 'ноября', 'декабря'
    ]

    def __init__(self, new_json_file_name=str):
        self.file_name = new_json_file_name

        if not (os.path.exists(self.file_name) and os.path.getsize(self.file_name) > 0):
            new_currency_data = {"currencies": [], "rates": {}, "date": ""}

            self.__save_to_file(new_currency_data, self.file_name)

    def __save_to_file(self, data=dict, file_name=str):
        currency_data_str = json.dumps(data, ensure_ascii=False)

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(currency_data_str)

    def __get_currency_data(self, file_name=str):
        try:
            if os.path.getsize(file_name) <= 0:
                raise FileNotFoundError('Файл пуст')

            with open(file_name, 'r', encoding='utf-8') as file:
                currency_data = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError) as error:
            raise FileNotFoundError(f'Проблемы с файлом {file_name}:', error)

        return currency_data

    def __save_currency_data(self, file_name=str, *, currencies: list = None, rates: dict = None, date: str = None):
        args = {'currencies': currencies, 'rates': rates, 'date': date}

        currency_data = self.__get_currency_data(file_name)

        for key in args.keys():
            if args[key] is not None:
                currency_data[key] = args[key]

        self.__save_to_file(currency_data, file_name)

    def get_currencies(self):
        return self.__get_currency_data(self.file_name)["currencies"]

    def add_currencies(self, *new_currencies):
        saved_currencies = self.get_currencies()

        for currency in new_currencies:
            if currency not in saved_currencies:
                saved_currencies.append(currency)

        self.__save_currency_data(self.file_name, currencies=saved_currencies)

    def remove_currencies(self, *currencies):
        saved_currencies = self.get_currencies()

        for currency in currencies:
            if currency in saved_currencies:
                saved_currencies.remove(currency)

        self.__save_currency_data(self.file_name, currencies=saved_currencies)

    def get_rates(self, url=str, params=dict):
        response = requests.get(url, params=params)

        if not response.ok:
            raise HTTPError(response.text)

        rates = response.json()

        return rates

    def get_old_rates(self):
        return self.__get_currency_data(self.file_name)["rates"]

    def save_rates(self, rates=dict):
        rates['BASE_CUR'] = 1.0
        self.__save_currency_data(self.file_name, rates=rates)

    def get_date(self):
        date = datetime.date.today()
        return f"{date.day} {Converter.months[date.month - 1]} {date.year} года"

    def get_old_date(self):
        return self.__get_currency_data(self.file_name)["date"]

    def save_date(self, date=str):
        self.__save_currency_data(self.file_name, date=date)

    def convert(self, rates=dict, currency=str, value=int):
        rates['BASE_CUR'] = 1.0

        base_currency_value = value / rates[currency]

        conversion_result = {}

        for key in rates.keys():
            conversion_result[key] = base_currency_value * rates[key]

        return conversion_result
