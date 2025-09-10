#!/usr/bin/env python3
# إنشاء جدول المدفوعات

import sqlite3
import sys
import os

# إضافة المسار الحالي إلى sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from database.connection import get_connection

def create_payments_table():
    """إنشاء جدول المدفوعات"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT NOT NULL,
            amount REAL DEFAULT 0,
            status TEXT DEFAULT 'pending',
            reference_number TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ تم إنشاء جدول المدفوعات بنجاح")

if __name__ == "__main__":
    create_payments_table()
