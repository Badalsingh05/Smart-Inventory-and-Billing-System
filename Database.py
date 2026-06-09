#Database Connection Settings
import psycopg2


def connection():
    con = psycopg2.connect(
        host="localhost",
        database="Ecommerce",
        user="postgres",
        password="Badal1234",
        port=5433
    )

    if con:
        print("Connection successful")
    else:
        print("Connection failed")
    return con
conn = connection()