import sqlite3


def connect():
    return sqlite3.connect("real_estate.db", timeout=10)





def add_property(title, address, ptype, price, status, desc):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO properties (title, address, property_type, price, status, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, address, ptype, price, status, desc))




def get_properties():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM properties")
        return cursor.fetchall()





def add_client(name, phone, email):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clients (full_name, phone, email)
        VALUES (?, ?, ?)
        """, (name, phone, email))




def get_clients():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        return cursor.fetchall()





def create_transaction(property_id, client_id, t_type, amount, date):
    conn = connect()
    cursor = conn.cursor()


    try:
        
        cursor.execute("SELECT status FROM properties WHERE id=?", (property_id,))
        result = cursor.fetchone()


        if not result or result[0] != "available":
            raise Exception("Property is not available")


        
        cursor.execute("""
        INSERT INTO transactions (property_id, client_id, transaction_type, amount, transaction_date)
        VALUES (?, ?, ?, ?, ?)
        """, (property_id, client_id, t_type, amount, date))


        
        new_status = "sold" if t_type == "sale" else "rented"


        cursor.execute(
            "UPDATE properties SET status=? WHERE id=?",
            (new_status, property_id)
        )


        conn.commit()


    finally:
        conn.close()




def get_transactions():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT t.id, p.title, c.full_name, t.transaction_type, t.amount, t.transaction_date
        FROM transactions t
        JOIN properties p ON t.property_id = p.id
        JOIN clients c ON t.client_id = c.id
        """)
        return cursor.fetchall()





def get_available_properties():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM properties WHERE status='available'")
        return cursor.fetchall()




def get_dashboard_stats():
    with connect() as conn:
        cursor = conn.cursor()


        cursor.execute("SELECT COUNT(*) FROM properties")
        total = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM properties WHERE status='available'")
        available = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM properties WHERE status='sold'")
        sold = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM properties WHERE status='rented'")
        rented = cursor.fetchone()[0]


        cursor.execute("SELECT COUNT(*) FROM clients")
        clients = cursor.fetchone()[0]


    return {
        "total_properties": total,
        "available": available,
        "sold": sold,
        "rented": rented,
        "clients": clients
    }
