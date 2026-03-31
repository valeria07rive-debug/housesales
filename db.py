import sqlite3

def connect():
    return sqlite3.connect("real_estate.db")

def add_property(title, address, ptype, price, status, desc):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO properties (title, address, property_type, price, status, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (title, address, ptype, price, status, desc))

    conn.commit()
    conn.close()


def get_properties():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM properties")
    data = cursor.fetchall()

    conn.close()
    return data


def add_client(name, phone, email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clients (full_name, phone, email)
    VALUES (?, ?, ?)
    """, (name, phone, email))

    conn.commit()
    conn.close()


def get_clients():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients")
    return cursor.fetchall()


def create_transaction(property_id, client_id, ttype, amount, date):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("SELECT status FROM properties WHERE id=?", (property_id,))
    status = cursor.fetchone()[0]

    if status in ["sold", "rented"]:
        raise Exception("Propiedad no disponible")

    cursor.execute("""
    INSERT INTO transactions (property_id, client_id, transaction_type, amount, transaction_date)
    VALUES (?, ?, ?, ?, ?)
    """, (property_id, client_id, ttype, amount, date))


    if ttype == "sale":
        cursor.execute("UPDATE properties SET status='sold' WHERE id=?", (property_id,))
    else:
        cursor.execute("UPDATE properties SET status='rented' WHERE id=?", (property_id,))

    conn.commit()
    conn.close()
