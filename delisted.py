import json
from dbhandler import DbHandler


# Database object
db = DbHandler()
conn = db.create_connection()


def main():
    delisted = json.load(open("data/symbols/delisted.json", "r"))
    print(delisted)

    for symbol in delisted:
        db.delete_quote(conn, symbol)


if __name__ == "__main__":
    main()
