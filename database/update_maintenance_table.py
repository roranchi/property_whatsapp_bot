#!/usr/bin/env python3
# تحديث جدول الصيانة لإضافة الحقول الجديدة

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

def update_maintenance_table():
    """تحديث جدول الصيانة"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # إضافة الحقول الجديدة
    new_columns = [
        ('assigned_technician', 'INTEGER'),
        ('issue_type', 'TEXT'),
        ('priority_level', 'TEXT DEFAULT "medium"'),
        ('ticket_number', 'TEXT'),
        ('assigned_at', 'TIMESTAMP'),
        ('resolved_at', 'TIMESTAMP')
    ]
    
    for column_name, column_type in new_columns:
        try:
            cursor.execute(f'ALTER TABLE maintenance ADD COLUMN {column_name} {column_type}')
            print(f"✅ تم إضافة حقل {column_name}")
        except sqlite3.OperationalError:
            print(f"✅ حقل {column_name} موجود بالفعل")
    
    conn.commit()
    conn.close()
    print("✅ تم تحديث جدول الصيانة بنجاح")

if __name__ == "__main__":
    update_maintenance_table()
