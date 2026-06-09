from Database import conn
from customers import Customer
from products import Product
import random
from datetime import datetime, timedelta

print("Generating Dummy Data...")

# -----------------------------
# 1. Customers (1000 Records)
# -----------------------------
print("Creating Customers...")

for i in range(1, 1001):
    Customer.insert_customer(
        f"Customer_{i}",
        f"98{random.randint(10000000,99999999)}"
    )

print("1000 Customers Created")

# -----------------------------
# 2. Products (500 Records)
# -----------------------------
print("Creating Products...")

product_names = [
    "Laptop","Mouse","Keyboard","Monitor","Printer",
    "SSD","RAM","USB Drive","Webcam","Speaker",
    "Router","Scanner","Projector","Tablet","Mobile",
    "Power Bank","Hard Disk","Graphics Card","CPU","Headphone"
]

for i in range(1, 501):

    product_name = random.choice(product_names)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products
        (name, description, price, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (
            f"{product_name}_{i}",
            f"Description for {product_name}_{i}",
            round(random.uniform(100, 50000), 2),
            random.randint(5, 500)
        )
    )

conn.commit()

print("500 Products Created")

# -----------------------------
# 3. Sales (2000 Records)
# -----------------------------
print("Creating Sales...")

cur = conn.cursor()

start_date = datetime(2025, 1, 1)

for i in range(1, 2001):

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
# 4. Sale Items (10000 Records)
# -----------------------------
print("Creating Sale Items...")

for sale_id in range(1, 2001):

    item_count = random.randint(2, 8)

    total_amount = 0

    for _ in range(item_count):

        product_id = random.randint(1, 500)

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
                product_id,
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
# 5. Create Low Stock Products
# -----------------------------
print("Creating Low Stock Items...")

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