# Container object to be filled with scraped information before writing to the database
class TmxQuote:
    def __init__(self):
        self.name = None
        self.price = None
        self.priceChange = None
        self.percentChange = None
        self.exchangeName = None
        self.exShortName = None
        self.exchangeCode = None
        self.marketPlace = None
        self.sector = None
        self.industry = None
        self.volume = None
        self.openPrice = None
        self.dayHigh = None
        self.dayLow = None
        self.MarketCap = None
        self.MarketCapAllClasses = None
        self.peRatio = None
        self.prevClose = None
        self.dividendFrequency = None
        self.dividendYield = None
        self.dividendAmount = None
        self.dividendCurrency = None
        self.beta = None
        self.eps = None
        self.exDividendDate = None
        self.shortDescription = None
        self.longDescription = None
        self.website = None
        self.email = None
        self.phoneNumber = None
        self.fullAddress = None
        self.employees = None
        self.shareOutStanding = None
        self.totalDebtToEquity = None
        self.totalSharesOutStanding = None
        self.sharesESCROW = None
        self.vwap = None
        self.dividendPayDate = None
        self.weeks52high = None
        self.weeks52low = None
        self.alpha = None
        self.averageVolume10D = None
        self.averageVolume30D = None
        self.averageVolume50D = None
        self.priceToBook = None
        self.priceToCashFlow = None
        self.returnOnEquity = None
        self.returnOnAssets = None
        self.day21MovingAvg = None
        self.day50MovingAvg = None
        self.day200MovingAvg = None
        self.dividend3Years = None
        self.dividend5Years = None
        self.datatype = None

    def dump_fields_as_tuple(self):
        return (
            self.name,
            self.price,
            self.priceChange,
            self.percentChange,
            self.exchangeName,
            self.exShortName,
            self.exchangeCode,
            self.marketPlace,
            self.sector,
            self.industry,
            self.volume,
            self.openPrice,
            self.dayHigh,
            self.dayLow,
            self.MarketCap,
            self.MarketCapAllClasses,
            self.peRatio,
            self.prevClose,
            self.dividendFrequency,
            self.dividendYield,
            self.dividendAmount,
            self.dividendCurrency,
            self.beta,
            self.eps,
            self.exDividendDate,
            self.shortDescription,
            self.longDescription,
            self.website,
            self.email,
            self.phoneNumber,
            self.fullAddress,
            self.employees,
            self.shareOutStanding,
            self.totalDebtToEquity,
            self.totalSharesOutStanding,
            self.sharesESCROW,
            self.vwap,
            self.dividendPayDate,
            self.weeks52high,
            self.weeks52low,
            self.alpha,
            self.averageVolume10D,
            self.averageVolume30D,
            self.averageVolume50D,
            self.priceToBook,
            self.priceToCashFlow,
            self.returnOnEquity,
            self.returnOnAssets,
            self.day21MovingAvg,
            self.day50MovingAvg,
            self.day200MovingAvg,
            self.dividend3Years,
            self.dividend5Years,
            self.datatype,
        )
