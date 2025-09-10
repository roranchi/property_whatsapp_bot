import sqlite3
from db import DB_FILE

def add_tenant(name, phone, building_id, payment_method):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tenants (name, phone, building_id, payment_method) VALUES (?, ?, ?, ?)",
        (name, phone, building_id, payment_method)
    )
    conn.commit()
    conn.close()

def list_tenants():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tenants")
    rows = cursor.fetchall()
    conn.close()
    return rows
