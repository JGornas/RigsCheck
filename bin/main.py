import datetime
import os
import argparse
import time

from EthWalletStats import EthWalletStats
from RvnWalletStats import RvnWalletStats


def get_stats():
    print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    if args.wallet_eth:
        eth = EthWalletStats(args.wallet_eth)
        eth.print()
        if args.save:
            eth.save("ETH_data.csv")
    if args.wallet_rvn:
        rvn = RvnWalletStats(args.wallet_rvn)
        rvn.print()
        if args.save:
            rvn.save("RVN_data.csv")


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
    elif args.interval != 0:
        while True:
            get_stats()
            print(f"Next refresh in {int(args.interval / 60)} minutes")
            time.sleep(args.interval)
            os.system('cls')
    else:
        input("No configuration entered! Press Enter to exit.")
