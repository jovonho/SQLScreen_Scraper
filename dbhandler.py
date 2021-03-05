"""Handler class for PostgreSQL database access."""

import psycopg2
import psycopg2.extras
from dbconfig import config


class DbHandler:
    def __init__(self):
        super()

    def create_connection(self):
        """Create a database connection to a PostgreSQL database."""
        conn = None

        try:
            params = config()
            print("Connecting to db...")
            conn = psycopg2.connect(**params)

            cur = conn.cursor()
            cur.execute("SELECT version()")
            db_version = cur.fetchone()
            print(f"PostgreSQL version {db_version}")
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return conn

    def execute(self, conn, sql_statement):
        """Execute a given SQL statement using the given connection."""
        result = None
        try:
            c = conn.cursor()
            c.execute(sql_statement)
            result = c.fetchall()
            c.close()
        except Exception as e:
            print(e)
        finally:
            return result

    def execute_self_contained(self, sql_statement):
        """Create a single-use connection to execute the given SQL statement."""
        conn = self.create_connection()

        result = None
        try:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            result = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.commit()
            return result

    def insert_quote(self, conn, quote_info):
        """Insert a TMX quote object in the db with all financial information."""
        result = None

        try:
            c = conn.cursor()

            sql = """INSERT INTO quotes (symbol, name, price, priceChange, percentChange, exchangeName, exShortName, exchangeCode, marketPlace, 
                    sector, industry, volume, openPrice, dayHigh, dayLow, MarketCap, MarketCapAllClasses, peRatio, prevClose, dividendFrequency, 
                    dividendYield, dividendAmount, dividendCurrency, beta, eps, exDividendDate, shortDescription, longDescription, website, email,
                    phoneNumber, fullAddress, employees, shareOutStanding, totalDebtToEquity, totalSharesOutStanding, sharesESCROW, vwap, 
                    dividendPayDate, weeks52high, weeks52low, alpha, averageVolume10D, averageVolume30D, averageVolume50D, priceToBook, 
                    priceToCashFlow, returnOnEquity, returnOnAssets, day21MovingAvg, day50MovingAvg, day200MovingAvg, dividend3Years, 
                    dividend5Years, datatype, __typename)  
                    VALUES 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (symbol) DO UPDATE SET 
                    (name, price, priceChange, percentChange, exchangeName, exShortName, exchangeCode, marketPlace, 
                    sector, industry, volume, openPrice, dayHigh, dayLow, MarketCap, MarketCapAllClasses, peRatio, prevClose, dividendFrequency, 
                    dividendYield, dividendAmount, dividendCurrency, beta, eps, exDividendDate, shortDescription, longDescription, website, email,
                    phoneNumber, fullAddress, employees, shareOutStanding, totalDebtToEquity, totalSharesOutStanding, sharesESCROW, vwap, 
                    dividendPayDate, weeks52high, weeks52low, alpha, averageVolume10D, averageVolume30D, averageVolume50D, priceToBook, 
                    priceToCashFlow, returnOnEquity, returnOnAssets, day21MovingAvg, day50MovingAvg, day200MovingAvg, dividend3Years, 
                    dividend5Years, datatype, __typename)  
                    = 
                    (EXCLUDED.name, EXCLUDED.price, EXCLUDED.priceChange, EXCLUDED.percentChange, EXCLUDED.exchangeName, EXCLUDED.exShortName, 
                    EXCLUDED.exchangeCode, EXCLUDED.marketPlace, EXCLUDED.sector, EXCLUDED.industry, EXCLUDED.volume, EXCLUDED.openPrice, 
                    EXCLUDED.dayHigh, EXCLUDED.dayLow, EXCLUDED.MarketCap, EXCLUDED.MarketCapAllClasses, EXCLUDED.peRatio, EXCLUDED.prevClose, 
                    EXCLUDED.dividendFrequency, EXCLUDED.dividendYield, EXCLUDED.dividendAmount, EXCLUDED.dividendCurrency, EXCLUDED.beta, 
                    EXCLUDED.eps, EXCLUDED.exDividendDate, EXCLUDED.shortDescription, EXCLUDED.longDescription, EXCLUDED.website, EXCLUDED.email, 
                    EXCLUDED.phoneNumber, EXCLUDED.fullAddress, EXCLUDED.employees, EXCLUDED.shareOutStanding, EXCLUDED.totalDebtToEquity, 
                    EXCLUDED.totalSharesOutStanding, EXCLUDED.sharesESCROW, EXCLUDED.vwap, EXCLUDED.dividendPayDate, EXCLUDED.weeks52high, 
                    EXCLUDED.weeks52low, EXCLUDED.alpha, EXCLUDED.averageVolume10D, EXCLUDED.averageVolume30D, EXCLUDED.averageVolume50D, 
                    EXCLUDED.priceToBook, EXCLUDED.priceToCashFlow, EXCLUDED.returnOnEquity, EXCLUDED.returnOnAssets, EXCLUDED.day21MovingAvg, 
                    EXCLUDED.day50MovingAvg, EXCLUDED.day200MovingAvg, EXCLUDED.dividend3Years, EXCLUDED.dividend5Years, EXCLUDED.datatype, 
                    EXCLUDED.__typename)
                    
                    RETURNING symbol;"""

            c.execute(sql, quote_info)
            result = c.fetchone()
            c.close()

        except (Exception, psycopg2.Error) as e:
            print(e)
        finally:
            conn.commit()
            return result
