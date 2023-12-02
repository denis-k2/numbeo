import requests
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook


class CurrencyScoopHook(BaseHook):
    def __init__(self, currency_conn_id: str):
        super().__init__()
        self.conn_id = currency_conn_id

    def get_rate(self, date, base_currency: str):
        url = "https://api.currencyscoop.com/v1/historical"
        params = {
            "base": "USD",
            # "symbols": currency.upper(),
            "api_key": self._get_api_key(),
            "date": str(date),
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        byn = response.json()["response"]["rates"]["BYN"]
        eur = response.json()["response"]["rates"]["EUR"]
        rub = response.json()["response"]["rates"]["RUB"]
        uah = response.json()["response"]["rates"]["UAH"]
        return (byn, eur, rub, uah)

    def _get_api_key(self):
        conn = self.get_connection(self.conn_id)
        if not conn.password:
            raise AirflowException("Missing API key (password) in connection settings")
        return conn.password
