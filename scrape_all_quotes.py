import json
import sys
import time
import requests
import quote as quote
from dbhandler import DbHandler

if __name__ == "__main__":

    start_time = time.perf_counter()

    all_symbols = []
    exchange = ""

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Syntax:\n{sys.argv[0]} exchange [start-symbol]")

    if sys.argv[1].lower() == "tsx":
        exchange = "TSX"
        with open("data/symbols/TSX.json", "r") as infile:
            all_symbols.extend(json.load(infile))
    elif sys.argv[1].lower() == "tsxv":
        exchange = "TSXV"
        with open("data/symbols/TSXV.json", "r") as infile:
            all_symbols.extend(json.load(infile))

    if len(sys.argv) == 3:
        start_symbol = sys.argv[2]
        all_symbols = [x for x in all_symbols if x >= start_symbol]

    print(f"Preparing to scrape: {all_symbols}")

    s = requests.Session()
    db_handler = DbHandler()
    conn = db_handler.create_connection()

    for symbol in all_symbols:
        quote.get_quote(s, conn, symbol)

    print(
        f"Finished scraping symbols {all_symbols[0]} to {all_symbols[-1]} ({len(all_symbols)} symbols total) from {exchange}"
    )

    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time} s")
