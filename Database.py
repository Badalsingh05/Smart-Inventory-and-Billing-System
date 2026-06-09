import sqlite3

def connection():
    con = sqlite3.connect(
        "inventory.db",
        check_same_thread=False
    )
    return con

conn = connection()