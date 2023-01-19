import sqlite3

def connect_to_db():
    connection = sqlite3.connect("Ecommerce_DB.db")
    connection.execute("PRAGMA foreign_key = 1")
    return connection


sql_query = """CREATE TABLE IF NOT EXISTS user(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               username  TEXT NOT NULL, 
               password  TEXT NOT NULL,
               email TEXT,
               balance  INTEGER);"""


sql_query2 = """CREATE TABLE IF NOT EXISTS category(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name  TEXT NOT NULL, 
               description TEXT,
               product_id INTEGER);"""


sql_query3 = """CREATE TABLE IF NOT EXISTS product(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name  TEXT NOT NULL, 
               description TEXT,
               price INTEGER NOT NULL,
               category_id INTEGER,
               FOREIGN KEY (category_id) REFERENCES category(product_id));"""


sql_query4 = """CREATE TABLE IF NOT EXISTS cart(
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                cart_user_id INTEGER NOT NULL,
                cart_product_id INTEGER NOT NULL,
                total_value INTEGER,
                FOREIGN KEY (cart_user_id) REFERENCES user (id),
                FOREIGN KEY (cart_product_id) REFERENCES product (id)
                );"""

sql_query5 = """CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_user_id INTEGER NOT NULL,
                order_product_id INTEGER NOT NULL,
                total_value INTEGER,
                FOREIGN KEY (order_user_id) REFERENCES user (id),
                FOREIGN KEY (order_product_id) REFERENCES cart (cart_product_id)
                );"""





conn = connect_to_db()
curr = conn.cursor()
curr.execute(sql_query5)
conn.close()