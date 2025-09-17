import sqlite3

DB_PATH = "property.db"

def get_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
