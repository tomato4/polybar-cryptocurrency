#!/usr/bin/env python3.6

import requests
import argparse
import json
import sys
import os

parser = argparse.ArgumentParser(description="Display currencies on polybar")
parser.add_argument("--coins", type=str,
                    nargs="+", help="Select coins to display")
parser.add_argument("--base", type=str,
                    nargs="?", default="USD", help="Currency base to convert against")
parser.add_argument("--decimals", type=int,
                    nargs="?", default=2, help="How many decimals to show")
parser.add_argument("--display", type=str,
                    nargs="?", default="price", choices=["price", "percentage", "both"], help="Display mode")

args = parser.parse_args()
home = os.path.expanduser("~/")

unicode_dict = {}
with open(f"{home}.config/polybar/modules_binary/polybar-cryptocurrency/coins.svg", "r", encoding="utf-8") as icons:
    for line in icons:
        unicode, coin = line.strip().split(":")
        unicode_dict[unicode] = coin

sys.stdout.write(" ")

for coin in args.coins:
    try:
        get = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={args.base}&ids={coin}").json()[0]
    except requests.ConnectionError:
        print(" ")
        exit()
    price = str(round(float(get["current_price"]), args.decimals))
    change = round(float(get["price_change_percentage_24h"]), 2)

    for _unicode, _coin in unicode_dict.items():
        if _coin == get["symbol"]:
            icon = chr(int(_unicode, 16)) if len(_unicode) > 1 else _unicode
            if args.display == "price":
                sys.stdout.write(f"{icon} {price} ")
            if args.display == "percentage":
                sys.stdout.write(f"{icon} {change:+}% ")
            if args.display == "both":
                sys.stdout.write(f"{icon} {price} ({change:+}%) ")
