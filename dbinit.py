from dbhandler import DbHandler as db


db_handler = db()


def create_quotes_table(connection):
    sql_create_quotes_table = open("create_table_quotes.sql", "r", encoding="utf-8").read()
    db_handler.execute(connection, sql_create_quotes_table)


if __name__ == "__main__":

    conn = db_handler.create_connection()

    create_quotes_table(conn)

    conn.commit()
