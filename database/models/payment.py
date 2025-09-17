import sqlite3
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from database.connection import get_connection

class Payment:
    def __init__(self, tenant_id, amount=0, payment_date=None, status='pending'):
        self.tenant_id = tenant_id
        self.amount = amount
        self.payment_date = payment_date or datetime.now().strftime('%Y-%m-%d')
        self.status = status
    
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (tenant_id, amount, payment_date, status)
            VALUES (?, ?, ?, ?)
        ''', (self.tenant_id, self.amount, self.payment_date, self.status))
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_pending_payments():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payments WHERE status = "pending" ORDER BY payment_date DESC')
        payments = cursor.fetchall()
        conn.close()
        return payments

if __name__ == "__main__":
    print("✅ نموذج المدفوعات جاهز")
