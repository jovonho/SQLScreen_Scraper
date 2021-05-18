"""Launch the TMXSceen Scraper Updater.

Perform all required initialization and scrape all symbols of the TSX and TSXV:

1) Launch dbinit.py if requested
2) Launch symbols.py to collect symbols
3) Launch scrape_symbols in multiple parallel processes
4) Remove delisted symbols from the DB """

import argparse
import json
import subprocess
import numpy
import sys
import time

import subprocess

if __name__ == "__main__":

    start = time.time()

    parser = argparse.ArgumentParser(
        epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-db", "--create-table", action="store_true", help="Create the quotes table"
    )
    parser.add_argument(
        "-ss", "--skip-symbols", action="store_true", help="Skip symbol list scraping"
    )
    parser.add_argument("-dr", "--dry-run", action="store_true", help="Dry run")
    parser.add_argument(
        "-t", "time", type=int, help="Time (in seconds) to wait between successive calls to tmx.com"
    )
    parser.add_argument(
        "-sd",
        "--skip-delisted",
        action="store_true",
        help="Skip removing delisted symbols from the DB",
    )
    args = parser.parse_args()

    if args.time:
        waittime = args.time
    else:
        waittime = 0

    if args.create_table:
        # Call dbinit.py to create the quotes table
        subprocess.call([sys.executable, "dbinit.py"])

    if not args.skip_symbols:
        # Call symbols.py to collect symbols
        subprocess.call([sys.executable, "symbols.py"])
        time.sleep(1)

    # Read the symbols from the previsouly written files
    symbols_TSX = json.load(open("data/symbols/TSX.json", "r"))
    symbols_TSXV = json.load(open("data/symbols/TSXV.json", "r"))

    # Split the symbol lists into chunks that we will scrape in parallel
    tsx_split = numpy.array_split(symbols_TSX, 4)
    tsxv_split = numpy.array_split(symbols_TSXV, 3)

    procs = []

    # Create a subprocess for each symbol chunk using Popen to launch scrape_symbols.py
    for symbols in tsx_split:
        print(f"Splitting TSX into subprocess covering {symbols[0]} to {symbols[-1]}")
        p = subprocess.Popen(
            [
                sys.executable,
                "scrape_symbols.py",
                "TSX",
                "-t",
                waittime,
                "-r",
                symbols[0],
                symbols[-1],
            ]
        )
        procs.append(p)

    for symbols in tsxv_split:
        print(f"Splitting TSXV into subprocess covering {symbols[0]} to {symbols[-1]}")
        p = subprocess.Popen(
            [sys.executable, "scrape_symbols.py", "TSXV", "-r", symbols[0], symbols[-1]]
        )
        procs.append(p)

    print("\n############ Preparing to Scrape ############\n")

    # Wait for all subprocesses to finish
    for p in procs:
        p.communicate()

    if not args.skip_delisted:
        # Call symbols.py to remove delisted symbols from DB
        subprocess.call([sys.executable, "delisted.py"])
        time.sleep(1)

    end = time.time()
    total_time = end - start
    min, sec = int(total_time / 60), int(round(total_time % 60, 0))

    print("\n############ All Done! ############\n")

    print(f"TMXSceen Scraper completed in {min} min {sec} s")
