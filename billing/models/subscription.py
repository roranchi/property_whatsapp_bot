from datetime import datetime, timedelta
from database.connection import get_connection

class Subscription:
    PLANS = {
        'basic': {'price': 5, 'features': ['عقود', 'مدفوعات', 'تقارير']},
        'advanced': {'price': 8, 'features': ['عقود', 'مدفوعات', 'تقارير', 'صيانة']},
        'professional': {'price': 12, 'features': ['جميع الميزات', 'دعم مخصص']}
    }

    @staticmethod
    def create_subscription(phone_number, plan_type):
        """إنشاء اشتراك جديد"""
        conn = get_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
        
        cursor.execute('''
            INSERT INTO subscriptions (phone_number, plan_type, start_date, end_date, active)
            VALUES (?, ?, ?, ?, 1)
        ''', (phone_number, plan_type, start_date, end_date))
        
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_subscription(phone_number):
        """الحصول على بيانات الاشتراك"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM subscriptions WHERE phone_number = ?', (phone_number,))
        subscription = cursor.fetchone()
        
        conn.close()
        return subscription
