"""Fetches all currently listed symbols for the TSX and TSXV exchanges."""

import argparse
import requests
import string
import json
import time
import uuid


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
    args = parser.parse_args()

    print("\n############ Collecting symbols to scrape ############")
    time.sleep(1)

    num_symbols_tsx, num_symbols_tsxv = list_symbols()

    print("############ Symbols Collected ############\n")
    print(f"Symbols listed on TSX:\t {num_symbols_tsx}")
    print(f"Symbols listed on TSXV:\t {num_symbols_tsxv}")
    print(f"Total:\t\t\t {num_symbols_tsx + num_symbols_tsxv}")
