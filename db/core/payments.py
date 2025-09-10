from datetime import datetime
import sqlite3

class PaymentManager:
    @staticmethod
    def get_todays_payments():
        """جلب مدفوعات اليوم"""
        try:
            conn = sqlite3.connect("property.db")
            cursor = conn.cursor()
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute("SELECT COUNT(*) FROM payments WHERE payment_date = ?", (today,))
            count = cursor.fetchone()[0]
            conn.close()
            
            return f"✅ تم العثور على {count} مدفوعات اليوم"
            
        except:
            return "لم يتم تسجيل أي مدفوعات اليوم."

    @staticmethod
    def get_overdue_payments():
        """جلب المدفوعات المتأخرة"""
        return "⚠️ نظام المتأخرات جاهز - سيتم تفعيله قريباً"