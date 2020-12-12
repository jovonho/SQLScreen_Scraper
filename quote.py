import requests
import json
from datetime import datetime
from dbhandler import DbHandler
import time
import sys


"""
    Fetch an instrument's financial data.
"""

db_handler = DbHandler()


def get_quote(session, connection, symbol: str) -> None:

    # TODO: See if we can save memory by having these be shared, but really not a problem rn.

    headers = {
        "authority": "app-money.tmx.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "*/*",
        "authorization": "",
        "locale": "en",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.228",
        "content-type": "application/json",
        "origin": "https://money.tmx.com",
        "referer": "https://money.tmx.com/en/quote/" + symbol,
        "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
    }

    request_body = {
        "operationName": "getQuoteBySymbol",
        "variables": {"symbol": symbol, "locale": "en"},
        "query": "query getQuoteBySymbol($symbol: String, $locale: String) { getQuoteBySymbol(symbol: $symbol, "
        "locale: $locale) { symbol name price priceChange percentChange "
        "exchangeName exShortName exchangeCode marketPlace sector industry "
        "volume openPrice dayHigh dayLow MarketCap MarketCapAllClasses "
        "peRatio prevClose dividendFrequency dividendYield dividendAmount "
        "dividendCurrency beta eps exDividendDate shortDescription "
        "longDescription  website email phoneNumber fullAddress employees "
        "shareOutStanding totalDebtToEquity totalSharesOutStanding sharesESCROW vwap "
        " dividendPayDate weeks52high weeks52low alpha averageVolume10D "
        "averageVolume30D averageVolume50D priceToBook priceToCashFlow returnOnEquity "
        "  returnOnAssets day21MovingAvg day50MovingAvg day200MovingAvg dividend3Years "
        "   dividend5Years datatype __typename }}",
    }

    start_time = time.perf_counter()

    r = session.post("https://app-money.tmx.com/graphql", headers=headers, json=request_body)

    if r.status_code == 200:
        data = json.loads(r.text)

        quote_info = data["data"]["getQuoteBySymbol"]

        # Convert data here
        if quote_info["employees"] != "":
            quote_info["employees"] = int(quote_info["employees"])

        quote_tuple = tuple(
            [quote_info[k] if quote_info[k] != "" else None for k in quote_info.keys()]
        )

        result = db_handler.insert_quote(connection, quote_tuple)

        end_time = time.perf_counter()
        print(f"Scraped {result[0]} in {end_time - start_time} s")


def get_time_series(symbol: str, startDate: str, endDate: str, interval_min: int = 30) -> None:

    timestamp_start = int(datetime.strptime(startDate, "%Y%m%d").replace(hour=9).timestamp())
    timestamp_end = int(datetime.strptime(endDate, "%Y%m%d").replace(hour=9).timestamp())

    headers = {
        "authority": "app-money.tmx.com",
        "scheme": "https",
        "path": "/graphql",
        "accept": "*/*",
        "authorization": "",
        "locale": "en",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.228",
        "origin": "https://money.tmx.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://money.tmx.com/en/quote/" + symbol,
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q: 0.9,fr-FR;q: 0.8,fr;q: 0.7",
    }

    request_body = {
        "operationName": "getTimeSeriesData",
        "variables": {
            "symbol": symbol,
            "interval": interval_min,
            "startDateTime": timestamp_start,
            "endDateTime": timestamp_end,
        },
        "query": "query getTimeSeriesData($symbol: String!, $freq: String, $interval: Int, $start: String, $end: String, $startDateTime: Int, $endDateTime: Int) {\n  getTimeSeriesData(symbol: $symbol, freq: $freq, interval: $interval, start: $start, end: $end, startDateTime: $startDateTime, endDateTime: $endDateTime) {\n    dateTime\n    open\n    high\n    low\n    close\n    volume\n}\n}\n",
    }

    s = requests.Session()
    r = s.post("https://app-money.tmx.com/graphql", headers=headers, json=request_body)

    if r.status_code == 200:
        with open("data/timeseries/" + symbol + "_ts.json", "w", encoding="utf-8") as outfile:
            data = json.loads(r.text)
            json.dump(data, outfile, indent=4)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} symbol")
        exit()

    symbol = sys.argv[1]
    session = requests.Session()

    conn = db_handler.create_connection()

    get_quote(session, conn, symbol)

    # get_time_series("HIVE", "20191105", "20201105")
