#!/usr/bin/env python3
# سكريبت الإرسال اليومي للتنبيهات - يعمل تلقائياً

import sys
sys.path.append('.')

from whatsapp.handlers.contract_handler import ContractHandler
from database.connection import get_connection

class DailyReminderService:
    def __init__(self, whatsapp_client):
        self.contract_handler = ContractHandler(whatsapp_client)
    
    def run_daily_reminders(self):
        """تشغيل جميع التنبيهات اليومية"""
        print('🔄 بدء التنبيهات اليومية...')
        
        # إرسال تنبيهات العقود
        contract_count = self.contract_handler.send_contract_reminders()
        print(f'✅ تم إرسال {contract_count} تنبيه عقود')
        
        # هنا سيتم إضافة تنبيهات المدفوعات لاحقاً
        
        return {
            'contract_reminders': contract_count,
            'payment_reminders': 0
        }

if __name__ == "__main__":
    # محاكاة عميل واتساب للاختبار
    class MockWhatsAppClient:
        def send_message(self, phone, message):
            print(f'📤 [TEST] إرسال إلى {phone}: {message[:50]}...')
            return True
    
    service = DailyReminderService(MockWhatsAppClient())
    results = service.run_daily_reminders()
    
    print(f'\\n🎯 النتائج: {results}')
    print('✅ تم تشغيل التنبيهات اليومية بنجاح!')
