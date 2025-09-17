import sqlite3
from db import DB_FILE

def add_building(name, address, system_type):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO buildings (name, address, system_type) VALUES (?, ?, ?)",
        (name, address, system_type)
    )
    conn.commit()
    conn.close()

def list_buildings():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buildings")
    rows = cursor.fetchall()
    conn.close()
    return rows
