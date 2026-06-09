import sqlite3
from Database import conn

class Customer:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

    def create_table():
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)
        conn.commit()
        cur.close()

    def insert_customer(name, contact):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (name, contact) VALUES (?, ?)",
            (name, contact)
        )
        conn.commit()
        cur.close()

    def update_customer(customer_id, name=None, contact=None):
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )

        customer = cur.fetchone()

        if not customer:
            cur.close()
            return

        if name and contact:
            cur.execute(
                "UPDATE customers SET name=?, contact=? WHERE id=?",
                (name, contact, customer_id)
            )

        elif name:
            cur.execute(
                "UPDATE customers SET name=? WHERE id=?",
                (name, customer_id)
            )

        elif contact:
            cur.execute(
                "UPDATE customers SET contact=? WHERE id=?",
                (contact, customer_id)
            )

        conn.commit()
        cur.close()

    def delete_customer(customer_id):
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM customers WHERE id=?",
            (customer_id,)
        )
        conn.commit()
        cur.close()

    def get_all_customers():
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        cur.close()
        return customers

    def view_customer_by_id(customer_id):
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM customers WHERE id=?",
            (customer_id,)
        )
        customer = cur.fetchone()
        cur.close()
        return customer

    def search_customer(name):
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM customers WHERE name LIKE ?",
            ('%' + name + '%',)
        )
        customers = cur.fetchall()
        cur.close()
        return customers

    def get_sales_by_customer(customer_id):
        cur = conn.cursor()
        cur.execute("""
            SELECT s.id, s.date, s.total_amount
            FROM sales s
            WHERE s.customer_id = ?
        """, (customer_id,))
        sales = cur.fetchall()
        cur.close()
        return sales