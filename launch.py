import argparse
import json
import numpy
import sys

from symbols import list_symbols
from subprocess import CREATE_NEW_CONSOLE, Popen, PIPE


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create list of symbols and scrape them all storing results in the DB."
    )
    args = parser.parse_args()

    print("############ Collecting symbols to scrape ############\n")

    # num_symbols_tsx, num_symbols_tsxv = list_symbols()
    num_symbols_tsx, num_symbols_tsxv = 2432, 1673

    print("############ Symbols Collected ############\n")
    print(f"Symbols listed on TSX:\t {num_symbols_tsx}")
    print(f"Symbols listed on TSXV:\t {num_symbols_tsxv}")
    print(f"Total:\t\t\t {num_symbols_tsx + num_symbols_tsxv}")

    # Read the symbols from the previsouly written files
    symbols_TSX = json.load(open("data/symbols/TSX.json", "r"))
    symbols_TSXV = json.load(open("data/symbols/TSXV.json", "r"))

    # Split the symbol lists into chunks that we will scrape in parallel
    tsx_split = numpy.array_split(symbols_TSX, 4)
    tsxv_split = numpy.array_split(symbols_TSXV, 2)
    # print("\nRecommended splits:")

    processes = []

    for split in tsx_split:
        # print(f"\tTSX {split[0]} {split[-1]}")
        processes.append(
            Popen(
                [sys.executable, "./scrape_symbols.py", "TSX", "-r", split[0], split[-1]],
                stdout=PIPE,
                stderr=PIPE,
            )
        )

    for split in tsxv_split:
        processes.append(
            Popen(
                [sys.executable, "./scrape_symbols.py", "TSXV", "-r", split[0], split[-1]],
                stdout=PIPE,
                stderr=PIPE,
            )
        )

    finished = 0
    while True:
        for proc in processes:
            proc.poll()
            print(proc.stdout.readline())

        # print(f"\tTSXV {split[0]} {split[-1]}")

    # TSX AAB DXG
    # TSX DXM JFS.UN
    # TSX JOSE SHLE
    # TSX SHOP ZZZD
    # TSXV A LL
    # TSXV LLG ZUM
