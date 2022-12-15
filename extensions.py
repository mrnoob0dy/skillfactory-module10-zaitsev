import json
import requests


from config import *



class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base_key = currencies[base.lower()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")
        try:
            quote_key = currencies[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}!")
        

        try:
            amount_val = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Не удалось обработать количество валюты {amount}!")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_key}&from={base_key}&amount={amount_val}"
        resp = requests.request("GET", url, headers=headers, data=payload)
        result_json = json.loads(resp.content)
        return result_json['result']
