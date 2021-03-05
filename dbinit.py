"""Create the quotes table if it does not exist."""

from dbhandler import DbHandler


def create_quotes_table(connection):
    sql_create_quotes_table = open("./sql/create_table_quotes.sql", "r", encoding="utf-8").read()
    db.execute(connection, sql_create_quotes_table)


if __name__ == "__main__":

    db = DbHandler()
    print("Creating quotes table if it does not exist...")
    conn = db.create_connection()
    try:
        create_quotes_table(conn)
        conn.commit()
        print("All good!")
    except Exception as e:
        print(e)
        print("Could not create table.")
