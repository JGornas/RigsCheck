import requests
import datetime
from collections import OrderedDict

from Exchanger import Exchanger
from CsvSaver import CsvSaver


class RvnWalletStats:
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
        self.wallet_stats = OrderedDict()
        self.update()

    def update(self):
        exchanger = Exchanger()
        miner_stats = requests.get(
            f"https://api-ravencoin.flypool.org/miner/{self.wallet_address}/currentStats").json()
        self.wallet_stats["rvn_price_usd"] = requests.get('https://api-ravencoin.flypool.org/poolStats').json()['data']['price']['usd']
        self.wallet_stats["rvn_price_pln"] = round(exchanger.usd_to_pln(self.wallet_stats["rvn_price_usd"]), 2)
        self.wallet_stats["daily_estimate_rvn"] = round(miner_stats['data']['coinsPerMin'] * 60 * 24, 3)
        self.wallet_stats["daily_estimate_usd"] = round(miner_stats['data']['usdPerMin'] * 60 * 24, 2)
        self.wallet_stats["daily_estimate_pln"] = round(60 * 24 *
                                                        exchanger.usd_to_pln(miner_stats['data']['usdPerMin']), 2)
        self.wallet_stats["monthly_estimate_rvn"] = round(self.wallet_stats["daily_estimate_rvn"] * 30, 2)
        self.wallet_stats["monthly_estimate_usd"] = round(self.wallet_stats["daily_estimate_usd"] * 30, 2)
        self.wallet_stats["monthly_estimate_pln"] = round(self.wallet_stats["daily_estimate_pln"] * 30, 2)
        self.wallet_stats["yearly_estimate_rvn"] = round(self.wallet_stats["daily_estimate_rvn"] * 365, 2)
        self.wallet_stats["yearly_estimate_usd"] = round(self.wallet_stats["daily_estimate_usd"] * 365, 2)
        self.wallet_stats["yearly_estimate_pln"] = round(self.wallet_stats["daily_estimate_pln"] * 365, 2)
        self.wallet_stats["before_year_ends_rvn"] = round(self.wallet_stats["daily_estimate_rvn"] *
                                                          (datetime.date(2022, 1, 1) - datetime.date.today()).days, 2)
        self.wallet_stats["before_year_ends_usd"] = round(self.wallet_stats["daily_estimate_usd"] *
                                                          (datetime.date(2022, 1, 1) - datetime.date.today()).days, 2)
        self.wallet_stats["before_year_ends_pln"] = round(self.wallet_stats["daily_estimate_pln"] *
                                                          (datetime.date(2022, 1, 1) - datetime.date.today()).days, 2)
        self.wallet_stats["current_hashrate"] = round(miner_stats['data']['currentHashrate'] / 1000000, 2)
        self.wallet_stats["average_hashrate"] = round(miner_stats['data']['averageHashrate'] / 1000000, 2)
        self.wallet_stats["unpaid_balance_rvn"] = round(miner_stats['data']['unpaid'] / 100000000, 2)
        self.wallet_stats["unpaid_balance_usd"] = round(self.wallet_stats["unpaid_balance_rvn"] *
                                                        exchanger.rvn_price_usd, 2)
        self.wallet_stats["unpaid_balance_pln"] = round(exchanger.usd_to_pln(self.wallet_stats["unpaid_balance_usd"]), 2)

    def save(self, filename):
        CsvSaver.save(filename, self.wallet_stats)

    def print(self):
        print(f"Ravencoin price: \t"
              f"{'{:.2f}'.format(self.wallet_stats['rvn_price_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['rvn_price_pln'])} PLN\n"
              f"Daily estimate: \t"
              f"{'{:.2f}'.format(self.wallet_stats['daily_estimate_usd'])} USD \t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['daily_estimate_pln'])} PLN \t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['daily_estimate_rvn'])} RVN\n"
              f"Monthly estimate: \t"
              f"{'{:.2f}'.format(self.wallet_stats['monthly_estimate_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['monthly_estimate_pln'])} PLN\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['monthly_estimate_rvn'])} RVN\n"
              f"Yearly estimate: \t"
              f"{'{:.2f}'.format(self.wallet_stats['yearly_estimate_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['yearly_estimate_pln'])} PLN\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['yearly_estimate_rvn'])} RVN\n"
              f"This year estimate:\t"
              f"{'{:.2f}'.format(self.wallet_stats['before_year_ends_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['before_year_ends_pln'])} PLN\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['before_year_ends_rvn'])} RVN\n"
              f"Unpaid balance: \t"
              f"{'{:.2f}'.format(self.wallet_stats['unpaid_balance_usd'])} USD\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['unpaid_balance_pln'])} PLN\t    -/-    "
              f"{'{:.2f}'.format(self.wallet_stats['unpaid_balance_rvn'])} RVN\n"
              f"Current hashrate:  "
              f"{'{:.2f}'.format(self.wallet_stats['current_hashrate'])} MH/s\t\t"
              f"Average hashrate:  "
              f"{'{:.2f}'.format(self.wallet_stats['average_hashrate'])} MH/s\n")
