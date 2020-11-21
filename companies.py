import requests
import json
from datetime import datetime


def get_quote(symbol: str) -> None:

    headers = {
        "authority": "app-money.tmx.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "*/*",
        "authorization": "",
        "locale": "en",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.228",
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
        "query": "query getQuoteBySymbol($symbol: String, $locale: String) {\n  getQuoteBySymbol(symbol: $symbol, locale: $locale) {\n    symbol\n    name\n    price\n    priceChange\n    percentChange\n    exchangeName\n    exShortName\n    exchangeCode\n    marketPlace\n    sector\n    industry\n    volume\n    openPrice\n    dayHigh\n    dayLow\n    MarketCap\n    MarketCapAllClasses\n    peRatio\n    prevClose\n    dividendFrequency\n    dividendYield\n    dividendAmount\n    dividendCurrency\n    beta\n    eps\n    exDividendDate\n    shortDescription\n    longDescription\n    website\n    email\n    phoneNumber\n    fullAddress\n    employees\n    shareOutStanding\n    totalDebtToEquity\n    totalSharesOutStanding\n    sharesESCROW\n    vwap\n    dividendPayDate\n    weeks52high\n    weeks52low\n    alpha\n    averageVolume10D\n    averageVolume30D\n    averageVolume50D\n    priceToBook\n    priceToCashFlow\n    returnOnEquity\n    returnOnAssets\n    day21MovingAvg\n    day50MovingAvg\n    day200MovingAvg\n    dividend3Years\n    dividend5Years\n    datatype\n    __typename\n  }\n}\n",
    }

    s = requests.Session()
    r = s.post("https://app-money.tmx.com/graphql", headers=headers, json=request_body)

    if r.status_code == 200:
        with open("data/quotes/" + symbol + ".json", "w", encoding="utf-8") as outfile:
            data = json.loads(r.text)
            json.dump(data, outfile, indent=4)


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
    # get_quote("ACB")

    get_time_series("HIVE", "20191105", "20201105")
