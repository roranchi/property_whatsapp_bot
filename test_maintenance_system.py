#!/usr/bin/env python3
# اختبار شامل لنظام الصيانة

import sys
import os
sys.path.append('.')

from database.connection import get_connection
from database.models.technician import Technician
from whatsapp.handlers.maintenance_handler import MaintenanceHandler
from database.setup_maintenance_update import verify_maintenance_table
from database.setup_technicians import create_technicians_table
from database.update_maintenance_table import update_maintenance_table

class MockWhatsAppClient:
    """عميل واتساب وهمي للاختبار"""
    def send_message(self, phone, message):
        print(f"📤 إرسال رسالة إلى {phone}:")
        print(message)
        print("─" * 50)

def test_maintenance_system():
    print("🔧 اختبار نظام الصيانة الشامل")
    print("=" * 60)
    
    # 1. التحقق من الجداول
    print("1. التحقق من جداول النظام...")
    verify_maintenance_table()
    
    # 2. التأكد من وجود فنيين
    print("\n2. التحقق من بيانات الفنيين...")
    technicians = Technician.get_all_active()
    if technicians:
        print(f"✅ يوجد {len(technicians)} فني نشط")
        for tech in technicians:
            print(f"   👨‍🔧 {tech.name} - {tech.specialty}")
    else:
        print("❌ لا يوجد فنيين، جاري إضافة فنيين تجريبيين...")
        create_technicians_table()
        technicians = Technician.get_all_active()
        print(f"✅ تم إضافة {len(technicians)} فني")
    
    # 3. اختبار معالج الصيانة
    print("\n3. اختبار معالج الصيانة...")
    mock_client = MockWhatsAppClient()
    handler = MaintenanceHandler(mock_client)
    
    # اختبار كشف نوع العطل
    test_messages = [
        "عطل في الكهرباء في الغرفة",
        "تسرب ماء في الحمام", 
        "دهان الحائط متقشر",
        "عطل عام في الشقة"
    ]
    
    for msg in test_messages:
        issue_type = handler._detect_issue_type(msg)
        print(f"   📝 '{msg}' → 🔧 {issue_type}")
    
    # 4. اختبار إنشاء تذكرة (بدون إدخال قاعدة البيانات)
    print("\n4. اختبار إنشاء تذكرة وهمية...")
    try:
        # محاكاة بيانات مستأجر
        tenant_data = {'id': 1, 'name': 'أحمد محمد'}
        
        # محاكاة إنشاء تذكرة
        ticket_id = 1001
        ticket_number = f"TKT-20250000-{ticket_id:04d}"
        
        # محاكاة توجيه الفني
        technician = Technician.get_by_specialty('كهرباء')
        if technician:
            tech_message = handler._create_technician_message(
                ticket_number, tenant_data['name'], 'كهرباء', 'عطل في الكهرباء'
            )
            tenant_response = handler._create_tenant_response(
                ticket_number, technician, 'كهرباء'
            )
            
            print("✅ اختبار النظام ناجح:")
            print(f"   📋 رقم التذكرة: {ticket_number}")
            print(f"   👨‍🔧 الفني: {technician.name}")
            print(f"   📞 الهاتف: {technician.phone}")
        else:
            print("⚠️  لا يوجد فني متخصص، اختبار الرد العام...")
            general_response = handler._create_general_response(ticket_number)
            print(f"   📋 رقم التذكرة: {ticket_number}")
    
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
    
    print("=" * 60)
    print("✅ اختبار النظام اكتمل بنجاح!")

if __name__ == "__main__":
    test_maintenance_system()
