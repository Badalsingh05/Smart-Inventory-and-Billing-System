from Database import conn

class Sale:
    def __init__(self, customer_id, date, total_amount):
        self.customer_id = customer_id
        self.date = date
        self.total_amount = total_amount

    def create_table():
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                total_amount REAL NOT NULL
            )
        """)

        conn.commit()
        cur.close()

    def insert_sale(customer_id, date, total_amount):
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sales
            (customer_id, date, total_amount)
            VALUES (?, ?, ?)
        """, (customer_id, date, total_amount))

        conn.commit()
        cur.close()

    def view_sales():
        cur = conn.cursor()

        cur.execute("SELECT * FROM sales")

        sales = cur.fetchall()

        cur.close()

        return sales

    def view_sale_by_id(sale_id):
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM sales WHERE id=?",
            (sale_id,)
        )

        sale = cur.fetchone()

        cur.close()

        return sale

    def generate_bill(sale_id):
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM sale_items WHERE sale_id=?",
            (sale_id,)
        )

        sale_items = cur.fetchall()

        total_amount = 0

        for item in sale_items:
            total_amount += item[3] * item[4]

        cur.close()

        return total_amount

    # Analytics

    def get_total_sales_by_date(start_date, end_date):
        cur = conn.cursor()

        cur.execute("""
            SELECT SUM(total_amount)
            FROM sales
            WHERE date BETWEEN ? AND ?
        """, (start_date, end_date))

        total_sales = cur.fetchone()[0]

        cur.close()

        return total_sales

    def get_top_selling_products():
        cur = conn.cursor()

        cur.execute("""
            SELECT product_id,
                   SUM(quantity) AS total_quantity
            FROM sale_items
            GROUP BY product_id
            ORDER BY total_quantity DESC
            LIMIT 5
        """)

        top_products = cur.fetchall()

        cur.close()

        return top_products

    def get_sales_by_customer(customer_id):
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM sales WHERE customer_id=?",
            (customer_id,)
        )

        sales = cur.fetchall()

        cur.close()

        return sales