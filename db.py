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




def update_property_status(property_id, new_status):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE properties SET status=? WHERE id=?
    """, (new_status, property_id))


    conn.commit()
    conn.close()





def update_property(pid, title, address, price, status):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE properties 
    SET title=?, address=?, price=?, status=? 
    WHERE id=?
    """, (title, address, price, status, pid))


    conn.commit()
    conn.close()





def delete_property(pid):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("DELETE FROM properties WHERE id=?", (pid,))


    conn.commit()
    conn.close()




def get_property_status(property_id):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("SELECT status FROM properties WHERE id=?", (property_id,))
    result = cursor.fetchone()


    conn.close()
    return result[0] if result else None





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





def delete_client(cid):
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("DELETE FROM clients WHERE id=?", (cid,))


    conn.commit()
    conn.close()





def create_transaction(property_id, client_id, t_type, amount, date):


    
    status = get_property_status(property_id)


    if status != "available":
        raise Exception("Property is not available")


    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO transactions (property_id, client_id, transaction_type, amount, transaction_date)
    VALUES (?, ?, ?, ?, ?)
    """, (property_id, client_id, t_type, amount, date))


   
    if t_type == "sale":
        update_property_status(property_id, "sold")
    elif t_type == "rent":
        update_property_status(property_id, "rented")


    conn.commit()
    conn.close()




def get_transactions():
    conn = connect()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT t.id, p.title, c.full_name, t.transaction_type, t.amount, t.transaction_date
    FROM transactions t
    JOIN properties p ON t.property_id = p.id
    JOIN clients c ON t.client_id = c.id
    """)


    data = cursor.fetchall()


    conn.close()
    return data





def get_available_properties():
    conn = connect()
    cursor = conn.cursor()


    
    try:
        cursor.execute("SELECT * FROM available_properties")
    except:
        cursor.execute("SELECT * FROM properties WHERE status='available'")


    data = cursor.fetchall()


    conn.close()
    return data




def get_dashboard_stats():
    conn = connect()
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


    conn.close()


    return {
        "total_properties": total,
        "available": available,
        "sold": sold,
        "rented": rented,
        "clients": clients
    }





def get_property_list():
    """Para dropdowns"""
    props = get_properties()
    return [(p[0], p[1]) for p in props]




def get_client_list():
    """Para dropdowns"""
    clients = get_clients()
    return [(c[0], c[1]) for c in clients]
