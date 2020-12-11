import json
import sys
import time
import random
import instruments as instr
from dbhandler import DbHandler

if __name__ == '__main__':

    all_symbols = []
    exchange = ""

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Syntax:\n{sys.argv[0]} exchange [start-symbol]")

    if sys.argv[1].lower() == 'tsx':
        exchange = "TSX"
        with open("data/symbols/TSX.json", "r") as infile:
            all_symbols.extend(json.load(infile))
    elif sys.argv[1].lower() == 'tsxv':
        exchange = "TSXV"
        with open("data/symbols/TSXV.json", "r") as infile:
            all_symbols.extend(json.load(infile))

    start_symbol = sys.argv[2]
    if start_symbol is not None:
        all_symbols = [x for x in all_symbols if x >= start_symbol]

    print(all_symbols)
    # exit()

    db_handler = DbHandler()
    conn = db_handler.create_connection()

    start_time = time.perf_counter()

    for symbol in all_symbols:
        print(f"Scraping symbol {symbol}")
        instr.get_quote(conn, symbol)

        # sleep_time = random.randrange(1, 3)
        # print(f"Sleeping {sleep_time}")
        # time.sleep(sleep_time)

    print(f"Finished scraping from {exchange}")

    end_time = time.perf_counter()
    print(f"Total time: {end_time - start_time} s")
