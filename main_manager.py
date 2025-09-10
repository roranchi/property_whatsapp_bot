"""
مدير المشروع الرئيسي - كل شي في مكان واحد
"""
import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path

class DatabaseManager:
    def __init__(self):
        self.db_path = "db/property.db"
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)

class ContractManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_expiring_contracts(self, days=30):
        """العقود المنتهية خلال X يوم"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        target_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT t.name, c.end_date 
            FROM contracts c
            JOIN tenants t ON c.tenant_id = t.id
            WHERE c.active = 1 AND c.end_date BETWEEN date('now') AND ?
        """, (target_date,))
        
        expiring_contracts = cursor.fetchall()
        conn.close()
        
        return expiring_contracts

    def get_contracts_report(self):
        """تقرير شامل عن العقود"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # العقود النشطة
            cursor.execute("SELECT COUNT(*) FROM contracts WHERE active = 1")
            active_count = cursor.fetchone()[0]
            
            # العقود المنتهية
            cursor.execute("SELECT COUNT(*) FROM contracts WHERE active = 0")
            expired_count = cursor.fetchone()[0]
            
            # العقود التي ستنتهي خلال 30 يوم
            expiring_soon = len(self.get_expiring_contracts(30))
            
            report_text = f"""
📋 تقرير العقود:
- العقود النشطة: {active_count}
- العقود المنتهية: {expired_count}
- العقود المنتهية خلال 30 يوم: {expiring_soon}
            """
            return report_text
            
        except Exception as e:
            return f"⚠️ خطأ في التقرير: {e}"
        finally:
            conn.close()

def quick_test():
    """اختبار سريع"""
    contract_manager = ContractManager()
    print("🔄 اختبار نظام العقود...")
    print(contract_manager.get_contracts_report())

if __name__ == "__main__":
    quick_test()
