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
    parser.add_argument(
        "-t",
        "--time",
        type=int,
        help="Time in seconds between network calls. To avoid getting blocked.",
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

    if args.time:
        waittime = args.time
    else:
        waittime = 0

    # If we specified a start or a range, trim the symbol list
    if args.start:
        all_symbols = [x for x in all_symbols if x >= args.start]
    elif args.range:
        all_symbols = [x for x in all_symbols if x >= args.range[0] and x <= args.range[1]]

    # Uncomment to test parallel process launch
    # from random import randint
    # from time import sleep
    # i = randint(0, 5)
    # while i > 0:
    #     print(i)
    #     i = i - 1

    print(
        f"Preparing to scrape symbols from {all_symbols[0]} to {all_symbols[-1]} ({len(all_symbols)} symbols) on {exchange}"
    )

    s = requests.Session()
    db_handler = DbHandler()
    conn = db_handler.create_connection()
    suspended = json.load(open("data/symbols/suspended.json", "r"))

    for symbol in all_symbols:
        try:
            getquote.get_quote(s, conn, symbol, suspended)
        except Exception as e:
            print(e)
            continue
        # Sleep between each call
        time.sleep(waittime)

    end_time = time.perf_counter()
    total_time = int(round(end_time - start_time, 0))
    print(
        f"Finished. Scraped from {all_symbols[0]} to {all_symbols[-1]} ({len(all_symbols)} symbols) on {exchange} in {total_time} s"
    )
