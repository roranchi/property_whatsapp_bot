#!/usr/bin/env python3
# إنشاء جدول تذكير العقود

import sqlite3
import sys
import os

# إضافة المسار الحالي إلى sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

DB_PATH = "property.db"

def get_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_contract_reminders_table():
    """إنشاء جدول تذكير العقود"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER,
            reminder_type TEXT NOT NULL,
            sent_date DATE NOT NULL,
            status TEXT DEFAULT 'sent',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(contract_id) REFERENCES contracts(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ تم إنشاء جدول contract_reminders")

if __name__ == "__main__":
    create_contract_reminders_table()
