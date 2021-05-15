import requests
import datetime
from collections import OrderedDict

from Exchanger import Exchanger
from CsvSaver import CsvSaver


class EthWalletStats:
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
        self.wallet_stats = OrderedDict()
        self.update()

    def update(self):
        exchanger = Exchanger()
        miner_stats = requests.get(
            f"https://api.ethermine.org/miner/{self.wallet_address}/currentStats").json()
        self.wallet_stats["eth_price_usd"] = requests.get('https://api.ethermine.org/poolStats').json()['data']['price']['usd']
        self.wallet_stats["eth_price_pln"] = round(exchanger.usd_to_pln(self.wallet_stats["eth_price_usd"]), 2)
        self.wallet_stats["daily_estimate_eth"] = round(miner_stats['data']['coinsPerMin'] * 60 * 24, 4)
        self.wallet_stats["daily_estimate_usd"] = round(miner_stats['data']['usdPerMin'] * 60 * 24, 2)
        self.wallet_stats["daily_estimate_pln"] = round(60 * 24 *
                                                        exchanger.usd_to_pln(miner_stats['data']['usdPerMin']), 2)
        self.wallet_stats["monthly_estimate_eth"] = round(self.wallet_stats["daily_estimate_eth"] * 30, 3)
        self.wallet_stats["monthly_estimate_usd"] = round(self.wallet_stats["daily_estimate_usd"] * 30, 2)
        self.wallet_stats["monthly_estimate_pln"] = round(self.wallet_stats["daily_estimate_pln"] * 30, 2)
        self.wallet_stats["yearly_estimate_eth"] = round(self.wallet_stats["daily_estimate_eth"] * 365, 3)
        self.wallet_stats["yearly_estimate_usd"] = round(self.wallet_stats["daily_estimate_usd"] * 365, 2)
        self.wallet_stats["yearly_estimate_pln"] = round(self.wallet_stats["daily_estimate_pln"] * 365, 2)
        self.wallet_stats["before_year_ends_eth"] = round(self.wallet_stats["daily_estimate_eth"] *
                                                          (datetime.date(2022, 1, 1) - datetime.date.today()).days, 3)
        self.wallet_stats["before_year_ends_usd"] = round(self.wallet_stats["daily_estimate_usd"] *
                                                          (datetime.date(2022, 1, 1) - datetime.date.today()).days, 2)
        self.wallet_stats["before_year_ends_pln"] = round(self.wallet_stats["daily_estimate_pln"] *
                                                          (datetime.date(2022, 1, 1) - datetime.date.today()).days, 2)
        self.wallet_stats["current_hashrate"] = round(miner_stats['data']['currentHashrate'] / 1000000, 2)
        self.wallet_stats["reported_hashrate"] = round(miner_stats['data']['reportedHashrate'] / 1000000, 2)
        self.wallet_stats["average_hashrate"] = round(miner_stats['data']['averageHashrate'] / 1000000, 2)
        self.wallet_stats["unpaid_balance_eth"] = round(miner_stats['data']['unpaid'] / 1000000000000000000, 5)
        self.wallet_stats["unpaid_balance_usd"] = round(self.wallet_stats["unpaid_balance_eth"] *
                                                        exchanger.eth_price_usd, 2)
        self.wallet_stats["unpaid_balance_pln"] = round(exchanger.usd_to_pln(self.wallet_stats["unpaid_balance_usd"]), 2)

    def save(self, filename):
        CsvSaver.save(filename, self.wallet_stats)

    def print(self):
        print(f"Ethereum price: \t"
              f"{'{:.2f}'.format(self.wallet_stats['eth_price_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['eth_price_pln'])} PLN\n"
              f"Daily estimate: \t"
              f"{'{:.2f}'.format(self.wallet_stats['daily_estimate_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['daily_estimate_pln'])} PLN\t    -/-    "
              f"{'{:.4f}'.format(self.wallet_stats['daily_estimate_eth'])} ETH\n"
              f"Monthly estimate:\t"
              f"{'{:.2f}'.format(self.wallet_stats['monthly_estimate_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['monthly_estimate_pln'])} PLN\t    -/-    "
              f"{'{:.3f}'.format(self.wallet_stats['monthly_estimate_eth'])} ETH\n"
              f"Yearly estimate:\t{'{:.2f}'.format(self.wallet_stats['yearly_estimate_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['yearly_estimate_pln'])} PLN\t    -/-    "
              f"{'{:.3f}'.format(self.wallet_stats['yearly_estimate_eth'])} ETH\n"
              f"Before ETH 2.0: \t"
              f"{'{:.2f}'.format(self.wallet_stats['before_year_ends_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['before_year_ends_pln'])} PLN\t    -/-    "
              f"{'{:.3f}'.format(self.wallet_stats['before_year_ends_eth'])} ETH\n"
              f"Unpaid balance: \t"
              f"{'{:.2f}'.format(self.wallet_stats['unpaid_balance_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['unpaid_balance_pln'])} PLN\t    -/-    "
              f"{'{:.4f}'.format(self.wallet_stats['unpaid_balance_eth'])} ETH\n"
              f"Reported hashrate:  "
              f"{'{:.2f}'.format(self.wallet_stats['reported_hashrate'])} MH/s\t\t"
              f"Average hashrate:  "
              f"{'{:.2f}'.format(self.wallet_stats['average_hashrate'])} MH/s\t\t"
              f"Pool hashrate:  "
              f"{'{:.2f}'.format(self.wallet_stats['current_hashrate'])} MH/s\n")
