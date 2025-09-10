#!/usr/bin/env python3
# إنشاء جدول الفنيين وتخصصاتهم

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

def create_technicians_table():
    """إنشاء جدول الفنيين"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS technicians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            specialty TEXT NOT NULL,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إضافة فنيين افتراضيين
    sample_technicians = [
        ('محمد أحمد', '+966500000001', 'كهرباء'),
        ('علي حسن', '+966500000002', 'سباكة'), 
        ('سعيد عبدالله', '+966500000003', 'نقاشة'),
        ('فهد محمد', '+966500000004', 'عامة'),
        ('خالد سليمان', '+966500000005', 'كهرباء'),
        ('طارق علي', '+966500000006', 'سباكة')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO technicians (name, phone, specialty)
        VALUES (?, ?, ?)
    ''', sample_technicians)
    
    conn.commit()
    conn.close()
    print("✅ تم إنشاء جدول الفنيين وإضافة بيانات تجريبية")

if __name__ == "__main__":
    create_technicians_table()
