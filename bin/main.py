import datetime
import os
import argparse
import time

from EthWalletStats import EthWalletStats
from RvnWalletStats import RvnWalletStats


def get_stats():
    print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    if args.wallet_eth:
        try:
            eth = EthWalletStats(args.wallet_eth)
            eth.print()
            if args.save:
                eth.save("ETH_data.csv")
        except KeyError:
            print("Error getting eth data.")
    if args.wallet_rvn:
        try:
            rvn = RvnWalletStats(args.wallet_rvn)
            rvn.print()
            if args.save:
                rvn.save("RVN_data.csv")
        except KeyError:
            print("Error getting rvn data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-we", "--wallet_eth", help="Ethereum wallet address",
                        type=str, default="")
    parser.add_argument("-wr", "--wallet_rvn", help="Ravencoin wallet address",
                        type=str, default="")
    parser.add_argument("-s", "--save", help="Save to a file 'coin_data.csv'", action="store_true")
    parser.add_argument("-i", "--interval", help="Set refresh interval for automatic refresh",
                        type=int)
    args = parser.parse_args()

    if not args.interval:
        while True:
            get_stats()
            input("Press Enter to refresh...\n")
            os.system('cls')
    else:
        while True:
            get_stats()
            print(f"Next refresh in {int(args.interval / 60)} minutes")
            time.sleep(args.interval)
            os.system('cls')
