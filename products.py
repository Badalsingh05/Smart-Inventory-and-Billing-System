import sqlite3
from Database import conn

class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def create_table():
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        conn.commit()
        cur.close()

    def insert_product(name, description, price, quantity):
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO products
            (name, description, price, quantity)
            VALUES (?, ?, ?, ?)
            """,
            (name, description, price, quantity)
        )
        conn.commit()
        cur.close()

    def update_product(product_id, name=None, description=None, price=None, quantity=None):
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )

        product = cur.fetchone()

        if not product:
            cur.close()
            return

        if name is not None and description is not None and price is not None and quantity is not None:
            cur.execute("""
                UPDATE products
                SET name=?, description=?, price=?, quantity=?
                WHERE id=?
            """, (name, description, price, quantity, product_id))

        elif quantity is not None:
            cur.execute("""
                UPDATE products
                SET quantity=?
                WHERE id=?
            """, (quantity, product_id))

        conn.commit()
        cur.close()

    def delete_product(product_id):
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM products WHERE id=?",
            (product_id,)
        )
        conn.commit()
        cur.close()

    def view_products():
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.close()
        return products

    def view_product_id(product_id):
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE id=?",
            (product_id,)
        )
        product = cur.fetchone()
        cur.close()
        return product

    def product_menu():
        while True:
            print("1. Create Table")
            print("2. Insert Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. View Products")
            print("6. View Product by ID")
            print("0. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                Product.create_table()

            elif choice == '2':
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Product.insert_product(name, description, price, quantity)

            elif choice == '3':
                product_id = int(input("Enter product id: "))
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                Product.update_product(
                    product_id,
                    name,
                    description,
                    price,
                    quantity
                )

            elif choice == '4':
                product_id = int(input("Enter product id: "))
                Product.delete_product(product_id)

            elif choice == '5':
                products = Product.view_products()
                for product in products:
                    print(product)

            elif choice == '6':
                product_id = int(input("Enter product id: "))
                print(Product.view_product_id(product_id))

            elif choice == '0':
                break