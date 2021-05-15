import requests
from bs4 import BeautifulSoup


class Exchanger:
    def __init__(self):
        self.eth_price_usd = ""
        self.rvn_price_usd = ""
        self.usd_to_pln_ratio = ""
        self.eth_price_pln = ""
        self.rvn_price_pln = ""
        self.update()

    def update(self):
        self.eth_price_usd = requests.get('https://api.ethermine.org/poolStats').json()['data']['price']['usd']
        self.rvn_price_usd = requests.get("https://api-ravencoin.flypool.org/poolStats").json()['data']['price']['usd']

        self.usd_to_pln_ratio = float(BeautifulSoup(
            requests.get("https://www.walutomat.pl/kursy-walut/usd-pln/").text, "html.parser")
            .find_all("span", {'class': 'value', "data-pair-exchange-value": ""})[2].text.replace(
            ",", "."))
        self.eth_price_pln = round(self.eth_price_usd * self.usd_to_pln_ratio, 2)
        self.rvn_price_pln = round(self.rvn_price_usd * self.usd_to_pln_ratio, 2)

    def usd_to_pln(self, usd):
        return round(usd * self.usd_to_pln_ratio, 2)
