"""Scrape data for all symbols in data/symbols/*.json

Called from the command line as:
python scrape_symbols.py <exchange> [start-symbol]
"""

import json
import sys
import argparse
import time
import requests
import getquote as getquote
from dbhandler import DbHandler

if __name__ == "__main__":
    # Start a timer for performance monitoring
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(description="Scrape symbols from the TSX or TSXV.")
    parser.add_argument(
        "exchange", choices=["TSX", "TSXV"], help="exchange from which to scrape. TSX or TSXV."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--start", help="symbol from which to start scraping")
    group.add_argument(
        "-r", "--range", nargs=2, help="first and last symbol of the range to scrape"
    )
    args = parser.parse_args()

    all_symbols = []
    exchange = args.exchange

    # Read the symbol list for the chosen exchange
    if exchange == "TSX":
        with open("data/symbols/TSX.json", "r") as infile:
            all_symbols.extend(json.load(infile))
    else:
        with open("data/symbols/TSXV.json", "r") as infile:
            all_symbols.extend(json.load(infile))

    # If we specified a start or a range, trim the symbol list
    if args.start:
        all_symbols = [x for x in all_symbols if x >= args.start]
    elif args.range:
        all_symbols = [x for x in all_symbols if x >= args.range[0] and x <= args.range[1]]

    # To test parallel process launch, remove after
    from random import randint
    from time import sleep

    sleep(randint(1, 10))

    print(
        f"Preparing to scrape symbols from {all_symbols[0]} to {all_symbols[-1]} ({len(all_symbols)} symbols) on {exchange}"
    )

    exit()

    s = requests.Session()
    db_handler = DbHandler()
    conn = db_handler.create_connection()

    for symbol in all_symbols:
        getquote.get_quote(s, conn, symbol)

    print("Finished scraping")

    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time} s")
