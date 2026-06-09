
from Database import conn
from customers import Customer
import random
from datetime import datetime, timedelta


def generate_data():

    cur = conn.cursor()

    # Check if data already exists
    cur.execute("SELECT COUNT(*) FROM customers")
    customer_count = cur.fetchone()[0]

    if customer_count > 0:
        print("Database already contains data.")
        return

    print("Generating Dummy Data...")

    # -----------------------------
    # Customers
    # -----------------------------
    for i in range(1, 1001):
        Customer.insert_customer(
            f"Customer_{i}",
            f"98{random.randint(10000000, 99999999)}"
        )

    print("1000 Customers Created")

    # -----------------------------
    # Products
    # -----------------------------
    product_names = [
        "Laptop", "Mouse", "Keyboard", "Monitor", "Printer",
        "SSD", "RAM", "USB Drive", "Webcam", "Speaker",
        "Router", "Scanner", "Projector", "Tablet", "Mobile",
        "Power Bank", "Hard Disk", "Graphics Card", "CPU", "Headphone"
    ]

    for i in range(1, 501):

        cur.execute(
            """
            INSERT INTO products
            (name, description, price, quantity)
            VALUES (?, ?, ?, ?)
            """,
            (
                f"{random.choice(product_names)}_{i}",
                f"Description {i}",
                round(random.uniform(100, 50000), 2),
                random.randint(5, 500)
            )
        )

    conn.commit()

    print("500 Products Created")

    # -----------------------------
    # Sales
    # -----------------------------
    start_date = datetime(2025, 1, 1)

    for _ in range(2000):

        customer_id = random.randint(1, 1000)

        sale_date = start_date + timedelta(
            days=random.randint(0, 365)
        )

        cur.execute(
            """
            INSERT INTO sales
            (customer_id, date, total_amount)
            VALUES (?, ?, ?)
            """,
            (
                customer_id,
                str(sale_date.date()),
                0
            )
        )

    conn.commit()

    print("2000 Sales Created")

    # -----------------------------
    # Sale Items
    # -----------------------------
    for sale_id in range(1, 2001):

        total_amount = 0

        for _ in range(random.randint(2, 8)):

            quantity = random.randint(1, 10)

            price = round(
                random.uniform(100, 10000),
                2
            )

            total_amount += quantity * price

            cur.execute(
                """
                INSERT INTO sale_items
                (sale_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
                """,
                (
                    sale_id,
                    random.randint(1, 500),
                    quantity,
                    price
                )
            )

        cur.execute(
            """
            UPDATE sales
            SET total_amount = ?
            WHERE id = ?
            """,
            (
                total_amount,
                sale_id
            )
        )

    conn.commit()

    # -----------------------------
    # Low Stock Products
    # -----------------------------
    for product_id in random.sample(range(1, 501), 20):

        cur.execute(
            """
            UPDATE products
            SET quantity = ?
            WHERE id = ?
            """,
            (
                random.randint(1, 5),
                product_id
            )
        )

    conn.commit()

    cur.close()

    print("=" * 50)
    print("DATA GENERATED SUCCESSFULLY")
    print("=" * 50)
    print("Customers : 1000")
    print("Products  : 500")
    print("Sales     : 2000")
    print("Sale Items: 10000+")
    print("=" * 50)


if __name__ == "__main__":
    generate_data()
