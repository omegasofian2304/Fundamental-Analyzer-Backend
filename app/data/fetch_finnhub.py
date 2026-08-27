import requests
from app.data.fundamental_metrique_fetcher import MetriqueFetcher, data_metrique_error
from app.config import FINNHUB_API_KEY
from datetime import datetime, timedelta



class Finnhub(MetriqueFetcher):
    def __init__(self, api_key=None, base_url="https://finnhub.io/api/v1/stock/metric"):
        self.api_key = api_key or FINNHUB_API_KEY
        self.base_url = base_url
    def fetch_metrique(self,ticker):
        '''
            fetch metrics data for a company

            :return:
            a dict of lists of tuples
        '''

        if not self.api_key:
            raise data_metrique_error("FINNHUB_API_KEY is missing")
        params = {
            "symbol": ticker,
            "metric": "all",
            "token": self.api_key
        }

        five_years = datetime.now() - timedelta(days=5 * 365)
        six_years = datetime.now() - timedelta(days=6 * 365)

        response = requests.get(self.base_url, params=params)
        if response.status_code != 200:
            raise data_metrique_error(f"Erreur API, status: {response.status_code}")

        data = response.json()

        try:
            quarterly = data["series"]["quarterly"]
        except KeyError:
            raise data_metrique_error(f"Format de réponse inattendu pour {ticker}")
        result={}
        metriques = {"netDebtToTotalEquity","netMargin","peTTM","salesPerShare"}

        for metrique in metriques:

            try:
                serie = quarterly[metrique]
            except KeyError:
                continue

            result[metrique] = []

            for point in serie:

                date = datetime.strptime(point["period"], "%Y-%m-%d")
                value = point["v"]

                if date >= six_years and metrique=="salesPerShare":
                    result[metrique].append((date,value))

                elif date >= five_years:

                    result[metrique].append((date, value))

        return result


