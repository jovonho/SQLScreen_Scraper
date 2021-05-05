"""This module contains functions to call the TMX graphql API.

Fetches all the info for a given symbol and writes the result to the database.
Examples of returned data can be found in ./data/quotes/ and ./data/timeseries/

Called by scrape_symbols.py on each symbol. 

To scrape a single symbol, call directly from the command line as:
python getquote.py <symbol>
"""

import argparse
import requests
import json
import time

from datetime import date, datetime
from dbhandler import DbHandler


class NoSuchSymbolError(Exception):
    """Raised when a symbol is not listed on TMX exchanges."""

    pass


# Database object
db = DbHandler()


def get_quote(session, connection, symbol: str, suspended) -> None:
    """Fetch a symbol's data from the TMX graphql API.

    Writes the results directly to the database.

    Paramaters
    ----------
    session - requests.Session object that will be used to call the API.
    connection - database connection object that will be used to write to the DB.
    symbol - The symbol to parse
    """

    # HTTP headers used to make the call, copied from obeserved network traffic
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

    # Graphql request, copied from obeserved network traffic
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
        "returnOnAssets day21MovingAvg day50MovingAvg day200MovingAvg dividend3Years "
        "dividend5Years datatype __typename }}",
    }

    start_time = time.perf_counter()

    # Actual call to the API
    r = session.post("https://app-money.tmx.com/graphql", headers=headers, json=request_body)

    # If successful, perform any and all data processing then write to db
    if r.status_code == 200:
        data = json.loads(r.text)

        quote_info = data["data"]["getQuoteBySymbol"]

        # TODO: Add more data processing/formatting here to avoid having to do it in the javascript
        if quote_info["employees"] != "":
            quote_info["employees"] = int(quote_info["employees"])

        # Mark the symbol as suspended if it's in the list
        quote_info["suspended"] = symbol in suspended

        quote_tuple = tuple(
            [quote_info[k] if quote_info[k] != "" else None for k in quote_info.keys()]
        )

        # Write results to the db
        result = db.insert_quote(connection, quote_tuple, datetime.utcnow())

        end_time = time.perf_counter()
        total_time = round(end_time - start_time, 4)

        print(f"Scraped {result[0]} in {total_time} s")
    elif r.status_code == 404:
        raise NoSuchSymbolError(f"Error: Symbol {symbol} does not exist.")
    else:
        raise Exception(f"Error fetching symbol.\n\tStatus: {r.status_code}\n\tReason: {r.reason}")


def get_time_series(symbol: str, start_date: str, end_date: str, interval_min: int = 30) -> None:
    """Fetch a symbol's timeseries data

    The TMX API also gives access to timeseries data. I only explored this a bit but we could extract
    all the past price history of an instrument to draw charts. This will be very heavy however.

    Writes results to ./data/timeseries/<symbol>_ts.json

    Paramaters
    ----------
    symbol - The symbol to get time series info on.
    start_date - Start date of time series.
    end_date - End date of time series.
    interval_min - Time interval size in minutes.

    """

    # Convert string dates to POSIX timestamps
    timestamp_start = int(datetime.strptime(start_date, "%Y%m%d").replace(hour=9).timestamp())
    timestamp_end = int(datetime.strptime(end_date, "%Y%m%d").replace(hour=9).timestamp())

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
        "query": "query getTimeSeriesData($symbol: String!, $freq: String, $interval: Int, $start: String, $end: String, $startDateTime: Int, $endDateTime: Int) \
            { getTimeSeriesData(symbol: $symbol, freq: $freq, interval: $interval, start: $start, end: $end, startDateTime: $startDateTime, endDateTime: $endDateTime) \
            { dateTime open high low close volume }}",
    }

    s = requests.Session()
    r = s.post("https://app-money.tmx.com/graphql", headers=headers, json=request_body)

    # If successful, write data to file.
    if r.status_code == 200:
        with open("data/timeseries/" + symbol + "_ts.json", "w", encoding="utf-8") as outfile:
            data = json.loads(r.text)
            json.dump(data, outfile, indent=4)
    elif r.status_code == 400:
        raise NoSuchSymbolError(f"Symbol {symbol} does not exist.")
    else:
        raise Exception(f"Error fetching {symbol}.\nStatus: {r.status_code}\nReason: {r.reason}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get a symbol's current quote from TMX.")
    parser.add_argument("symbol", help="The symbol to quote.")
    args = parser.parse_args()

    session = requests.Session()

    conn = db.create_connection()

    try:
        get_quote(session, conn, args.symbol)
    except NoSuchSymbolError as e:
        print(e)
    except Exception as e:
        print(e)

    # Uncomment to try the timeseries function.
    # get_time_series("HIVE", "20191105", "20201105")
