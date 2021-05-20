"""Fetches all currently listed symbols for the TSX and TSXV exchanges."""

import argparse
import requests
import string
import json
import time
import os
from pathlib import Path


def list_symbols_to_remove():
    url_delisted_tsx = "https://www.tsx.com/json/company-directory/delisted/tsx"
    url_delisted_tsxv = "https://www.tsx.com/json/company-directory/delisted/tsxv"

    url_suspended_tsx = "https://www.tsx.com/json/company-directory/suspended/tsx"
    url_suspended_tsxv = "https://www.tsx.com/json/company-directory/suspended/tsxv"

    urls_delisted = [url_delisted_tsx, url_delisted_tsxv]
    urls_suspended = [url_suspended_tsx, url_suspended_tsxv]

    symbols_delisted = []
    symbols_suspended = []

    s = requests.Session()

    for url in urls_delisted:
        print("Fecthing symbols to delist")
        resp = s.get(url)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"Request failed for url: {url}")
            next

        data = json.loads(resp.text)["results"]

        for _ in data:
            symbols_delisted.append(_["symbol"])
            print(_["symbol"], end=" ")

        symbols_delisted.sort()

        # Remove duplicates
        symbols_delisted = list(dict.fromkeys(symbols_delisted))
        print("\nDone")

    for url in urls_suspended:
        print("Fecthing suspended symbols")
        resp = s.get(url)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"Request failed for url: {url}")
            next

        data = json.loads(resp.text)["results"]

        for _ in data:
            symbols_suspended.append(_["symbol"])
            print(_["symbol"], end=" ")

        symbols_suspended.sort()

        # Remove duplicates
        symbols_suspended = list(dict.fromkeys(symbols_suspended))
        print("\nDone")

    with open("data/symbols/delisted.json", "w", encoding="utf-8") as out_delisted, open(
        "data/symbols/suspended.json", "w", encoding="utf-8"
    ) as out_suspended:
        json.dump(symbols_delisted, out_delisted, ensure_ascii=True)
        json.dump(symbols_suspended, out_suspended, ensure_ascii=True)

    print(
        "\n\nSuccessfully wrote files:\n\t./data/symbols/delisted.json\n\t./data/symbols/suspended.json\n"
    )

    return len(symbols_delisted), len(symbols_suspended)


def list_symbols():
    """Query TMX API for listed symbols and write them to two JSON files."""

    alphabet = list(string.ascii_uppercase)
    alphabet.append("0-9")

    user_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 OPR/67.0.3575.53"""
    headers = {"User-Agent": user_agent}

    symbols_TSX = []
    symbols_TSXV = []

    s = requests.Session()

    # Iterate over the alphabet and fetch all TSX/TSXV symbols
    for letter in alphabet:
        print(f"\n\nCompanies starting with letter {letter}:")

        url_TSX = "https://www.tsx.com/json/company-directory/search/tsx/" + letter
        url_TSXV = "https://www.tsx.com/json/company-directory/search/tsxv/" + letter

        resp_TSX = s.get(url_TSX, headers=headers)
        resp_TSXV = s.get(url_TSXV, headers=headers)

        try:
            resp_TSX.raise_for_status()
            resp_TSXV.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"Company directory request failed for {letter}")
            next

        json_listed_TSX = json.loads(resp_TSX.text)
        json_listed_TSXV = json.loads(resp_TSXV.text)

        # TMX API returns an array of objects
        listed_companies_TSX = json_listed_TSX["results"]
        listed_companies_TSXV = json_listed_TSXV["results"]

        for _ in listed_companies_TSX:
            for __ in _["instruments"]:
                symbols_TSX.append(__["symbol"])
                print(__["symbol"], end=" ")

        for _ in listed_companies_TSXV:
            for __ in _["instruments"]:
                symbols_TSXV.append(__["symbol"])
                print(__["symbol"], end=" ")

    symbols_TSX.sort()
    symbols_TSXV.sort()

    # Remove duplicates
    symbols_TSX = list(dict.fromkeys(symbols_TSX))
    symbols_TSXV = list(dict.fromkeys(symbols_TSXV))

    with open("data/symbols/TSX.json", "w", encoding="utf-8") as out_tsx, open(
        "data/symbols/TSXV.json", "w", encoding="utf-8"
    ) as out_tsxv:
        json.dump(symbols_TSX, out_tsx, ensure_ascii=True)
        json.dump(symbols_TSXV, out_tsxv, ensure_ascii=True)

    print("\n\nSuccessfully wrote files:\n\t./data/symbols/TSX.json\n\t./data/symbols/TSXV.json\n")

    return len(symbols_TSX), len(symbols_TSXV)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Collect all symbols currently listed on the TSX and TSXV."
    )
    parser.add_argument(
        "-ss", "--skip-symbols", action="store_true", help="Skip scraping symbol lists."
    )
    parser.add_argument(
        "-sr",
        "--skip-removals",
        action="store_true",
        help="Skip scraping suspended and delisted symbols.",
    )
    args = parser.parse_args()

    # Create necessary dir if not present
    if not os.path.isdir("data/symbols"):
        os.makedirs("data/symbols")

    if not args.skip_symbols:
        print("\n############ Collecting Symbols to Scrape ############")
        time.sleep(1)

        num_symbols_tsx, num_symbols_tsxv = list_symbols()

        print("############ Symbols Collected ############\n")
        print(f"Symbols listed on TSX:\t {num_symbols_tsx}")
        print(f"Symbols listed on TSXV:\t {num_symbols_tsxv}")
        print(f"Total:\t\t\t {num_symbols_tsx + num_symbols_tsxv}")

    if not args.skip_removals:
        print("\n############ Collecting Delisted and Suspended Symbols ############")
        time.sleep(1)

        num_delisted, num_suspended = list_symbols_to_remove()

        print("############ Symbols Collected ############\n")
        print(f"Symbols delisted:\t {num_delisted}")
        print(f"Symbols suspended:\t {num_suspended}")