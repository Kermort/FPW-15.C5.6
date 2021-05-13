import requests
from config import keys

class APIException(Exception):
    pass

class Converter():
    @staticmethod
    def convert(cur: str, base: str, amount: str):
        if cur.lower() == base.lower():
            raise APIException(f"Введены две одинаковые валюты {cur.lower()}")
        if cur.lower() not in keys.keys():
            raise APIException(f"Невозможно обработать валюту {cur.lower()}")
        if base.lower() not in keys.keys():
            raise APIException(f"Невозможно обработать валюту {base.lower()}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Ошибка в количестве валюты")
        r = requests.get(f"https://api.coingate.com/v2/rates/merchant/{keys[cur.lower()]}/{keys[base.lower()]}")
        return r.content