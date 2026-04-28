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
    data = cursor.fetchall()

    conn.close()
    return data



def create_transaction(property_id, client_id, ttype, amount, date):
    conn = connect()
    cursor = conn.cursor()

    
    cursor.execute("SELECT status FROM properties WHERE id=?", (property_id,))
    result = cursor.fetchone()

    if not result:
        raise Exception("Propiedad no existe")

    status = result[0]

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
    def get_available_properties():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM available_properties")
    data = cursor.fetchall()

    conn.close()
    return data


def get_dashboard_stats():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM properties")
    total_properties = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM properties WHERE status='available'")
    available = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM properties WHERE status='sold'")
    sold = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM properties WHERE status='rented'")
    rented = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clients")
    total_clients = cursor.fetchone()[0]

    conn.close()

    return {
        "total_properties": total_properties,
        "available": available,
        "sold": sold,
        "rented": rented,
        "clients": total_clients
    }


def get_transactions():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    conn.close()
    return data