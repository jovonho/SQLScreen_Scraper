import requests
import string
import json
import logging
import sys


logger = logging.getLogger(__name__)

formater = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formater)

file_handler = logging.FileHandler("logs/symbols.log")
file_handler.setFormatter(formater)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def list_symbols():
    alphabet = list(string.ascii_uppercase)
    alphabet.append("0-9")

    user_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 OPR/67.0.3575.53"""
    headers = {"User-Agent": user_agent}

    symbols_TSX = []
    symbols_TSXV = []

    s = requests.Session()

    # Iterate over the alphabet and fetch all TSX/TSXV symbols
    for letter in alphabet:
        logger.info("Looking at companies starting with", letter)

        url_TSX = "https://www.tsx.com/json/company-directory/search/tsx/" + letter
        url_TSXV = "https://www.tsx.com/json/company-directory/search/tsxv/" + letter

        resp_TSX = s.get(url_TSX, headers=headers)
        resp_TSXV = s.get(url_TSXV, headers=headers)

        try:
            resp_TSX.raise_for_status()
            resp_TSXV.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.exeption(f"Company directory request failed for letter {letter}")
            next

        json_listed_TSX = json.loads(resp_TSX.text)
        json_listed_TSXV = json.loads(resp_TSXV.text)

        listed_companies_TSX = json_listed_TSX["results"]
        listed_companies_TSXV = json_listed_TSXV["results"]

        for _ in listed_companies_TSX:
            for __ in _["instruments"]:
                symbols_TSX.append(__["symbol"])

        for _ in listed_companies_TSXV:
            for __ in _["instruments"]:
                symbols_TSXV.append(__["symbol"])

    symbols_TSX.sort()
    symbols_TSXV.sort()

    with open("data/symbol_lists/TSX.json", "w", encoding="utf-8") as out_tsx, open(
        "data/symbol_lists/TSXV.json", "w", encoding="utf-8"
    ) as out_tsxv:
        json.dump(symbols_TSX, out_tsx, ensure_ascii=True)
        json.dump(symbols_TSXV, out_tsxv, ensure_ascii=True)


if __name__ == "__main__":
    print("############ Creating symbols list files ############\n")
    list_symbols()

    tsx = tsxv = []

    with open("data/symbol_lists/TSX.json", "r") as infile:
        tsx = json.load(infile)

    with open("data/symbol_lists/TSXV.json", "r") as infile:
        tsxv = json.load(infile)

    print(f"Symbols listed on TSX:\t {len(tsx)}")
    print(f"Symbols listed on TSXV:\t {len(tsxv)}")
    print(f"Total:\t\t\t {len(tsx)+len(tsxv)}")
