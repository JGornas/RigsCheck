# RigsCheck

RigsCheck - Python API wrapper for ethermine.org and ravencoin.flypool.org. Gathers statistics about a workers and prints it in command line. Can be set to refresh automaticaly every x seconds. Can be set to save stats to a .csv file.


## Installation

Use the package manager pip to install required libraries.

```bash
pip install -r requirements.txt
```

or use install.bat.

## Usage

usage: main.py [-h] [-we WALLET_ETH] [-wr WALLET_RVN] [-s] [-i INTERVAL]

optional arguments:
  -h, --help - show this help message and exit
  -we WALLET_ETH, --wallet_eth WALLET_ETH - Ethereum wallet address
  -wr WALLET_RVN, --wallet_rvn WALLET_RVN - Ravencoin wallet address
  -s, --save - Save to a file 'coin_data.csv'
  -i INTERVAL, --interval INTERVAL - Set refresh interval for automatic refresh

## License

[MIT](https://choosealicense.com/licenses/mit/)

