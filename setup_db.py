import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("business.db")
cursor = conn.cursor()

cursor.executescript("""
        create table if not exists customers (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     email TEXT,
                     city TEXT,
                     joined_date TEXT
                     );
        create table if not exists products (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     category TEXT,
                     price REAL
                     );
        create table if not exists orders(
                     id INTEGER PRIMARY KEY,
                     customer_id INTEGER,
                     product_id INTEGER,
                     quantity INTEGER,
                     order_date TEXT,
                     status TEXT,
                     FOREIGN KEY (customer_id) REFERENCES customers(id),
                     FOREIGN KEY (product_id) REFERENCES products(id)
                     );""")

cities= ["Chennai","Madurai","Trichy","Tirunelveli","Kancheepuram"]
status=["Completed","Pending","Cancelled"]

products=[
    ("Laptop","Electronics",999.99),
    ("Iphone","Electronics",1234.22),
    ("Kettle","Electronics",678.99),
    ("Jean","Clothing",500.99),
    ("Cycle","Fitness",234.99)
]

cursor.executemany(
    "INSERT INTO products (name,category,price) values (?,?,?)",products
)

for i in range(1,51):
    days_ago=random.randint(30,500)
    joined=(datetime.now()-timedelta(days=days_ago)).strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO customers (name,email,city,joined_date) values (?,?,?,?)",
        (f"Customer {i}",f"customer{i}@gmail.com",random.choice(cities),joined)
    )

for i in range (1,201):
    days_ago=random.randint(30,500)
    order_date=(datetime.now()-timedelta(days=days_ago)).strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO orders (customer_id,product_id,quantity,order_date,status) values (?,?,?,?,?)",
        (random.randint(1,50),random.randint(1,5),random.randint(1,5),order_date,random.choice(status) ))
    

conn.commit()
conn.close()
print("Database configured for Customers, orders and products")