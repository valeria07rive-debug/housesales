
import sqlite3

conn = sqlite3.connect("real_estate.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    address TEXT NOT NULL,
    property_type TEXT,
    price REAL CHECK(price > 0),
    status TEXT CHECK(status IN ('available','sold','rented','reserved')),
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    client_id INTEGER,
    transaction_type TEXT CHECK(transaction_type IN ('sale','rent')),
    amount REAL,
    transaction_date TEXT
)
""")

conn.commit()
conn.close()

print("DB creada bien xfin")
