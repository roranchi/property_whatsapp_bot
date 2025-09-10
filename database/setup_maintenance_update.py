#!/usr/bin/env python3
# تأكد من تحديث جدول الصيانة بالحقول الجديدة

import sqlite3
import sys
import os

# إضافة المسار الحالي إلى sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from database.connection import get_connection

def verify_maintenance_table():
    """التأكد من اكتمال جدول الصيانة"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # الحقول المطلوبة
    required_columns = [
        'assigned_technician', 'issue_type', 'priority_level',
        'ticket_number', 'assigned_at', 'resolved_at'
    ]
    
    # التحقق من وجود الحقول
    cursor.execute("PRAGMA table_info(maintenance)")
    existing_columns = [col['name'] for col in cursor.fetchall()]
    
    print("🔍 التحقق من جدول الصيانة:")
    print("=" * 40)
    
    all_columns_exist = True
    for column in required_columns:
        if column in existing_columns:
            print(f"✅ {column}: موجود")
        else:
            print(f"❌ {column}: غير موجود")
            all_columns_exist = False
    
    if all_columns_exist:
        print("=" * 40)
        print("🎉 جدول الصيانة مكتمل وجاهز للاستخدام")
    else:
        print("=" * 40)
        print("⚠️  بعض الحقول مفقودة، يرجى تشغيل update_maintenance_table.py")
    
    conn.close()
    return all_columns_exist

if __name__ == "__main__":
    verify_maintenance_table()
