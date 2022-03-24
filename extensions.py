import requests
import json
from config import keys


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось конвертировать валюту {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось конвертировать валюту {quote}.")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}.")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        resp = json.loads(r.content)
        total_base = resp[quote_ticker] * amount
        total_base = round(total_base, 3)

        return total_base



