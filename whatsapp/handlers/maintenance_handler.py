from database.connection import get_connection
from database.models.technician import Technician
from datetime import datetime
import random

class MaintenanceHandler:
    def __init__(self, whatsapp_client):
        self.client = whatsapp_client
    
    def handle_maintenance_request(self, phone_number, message):
        """معالجة طلبات الصيانة من المستأجرين"""
        try:
            # استخراج نوع العطل من الرسالة
            issue_type = self._detect_issue_type(message)
            
            # البحث عن المستأجر برقم الهاتف
            tenant = self._get_tenant_by_phone(phone_number)
            
            if not tenant:
                return "❌ عذراً، لم يتم العثور على بياناتك. يرجى التواصل مع الإدارة."
            
            # إنشاء تذكرة الصيانة
            ticket_id = self._create_maintenance_ticket(tenant['id'], message, issue_type)
            
            # إنشاء رقم التذكرة
            ticket_number = f"TKT-{datetime.now().strftime('%Y%m%d')}-{ticket_id:04d}"
            self._update_ticket_number(ticket_id, ticket_number)
            
            # توجيه التذكرة للفني المناسب
            response = self._assign_to_technician(ticket_id, ticket_number, issue_type, tenant['name'], message)
            
            return response
            
        except Exception as e:
            print(f"❌ خطأ في معالجة طلب الصيانة: {e}")
            return "❌ حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً."
    
    def _get_tenant_by_phone(self, phone_number):
        """البحث عن المستأجر باستخدام رقم الهاتف"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name FROM tenants WHERE phone = ?', (phone_number,))
        tenant = cursor.fetchone()
        conn.close()
        return tenant
    
    def _create_maintenance_ticket(self, tenant_id, description, issue_type):
        """إنشاء تذكرة صيانة جديدة"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # تحديد الأولوية بناءً على نوع العطل
        priority = self._determine_priority(issue_type)
        
        cursor.execute('''
            INSERT INTO maintenance (tenant_id, description, issue_type, status, priority_level)
            VALUES (?, ?, ?, 'open', ?)
        ''', (tenant_id, description, issue_type, priority))
        
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return ticket_id
    
    def _determine_priority(self, issue_type):
        """تحديد أولوية التذكرة"""
        priority_map = {
            'كهرباء': 'high',
            'سباكة': 'high',
            'نقاشة': 'medium',
            'عامة': 'low'
        }
        return priority_map.get(issue_type, 'medium')
    
    def _update_ticket_number(self, ticket_id, ticket_number):
        """تحديث رقم التذكرة"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE maintenance SET ticket_number = ? WHERE id = ?', 
                      (ticket_number, ticket_id))
        conn.commit()
        conn.close()
    
    def _assign_to_technician(self, ticket_id, ticket_number, issue_type, tenant_name, description):
        """توجيه التذكرة إلى الفني المناسب"""
        technician = Technician.get_by_specialty(issue_type)
        
        if not technician:
            # إذا لم يوجد فني متخصص، استخدام فني عام
            technician = Technician.get_by_specialty('عامة')
        
        if technician:
            # تحديث التذكرة بالفني
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE maintenance 
                SET assigned_technician = ?, status = 'assigned', assigned_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (technician.id, ticket_id))
            
            conn.commit()
            conn.close()
            
            # إرسال تنبيه للفني
            tech_message = self._create_technician_message(ticket_number, tenant_name, issue_type, description)
            self.client.send_message(technician.phone, tech_message)
            
            return self._create_tenant_response(ticket_number, technician, issue_type)
        
        return self._create_general_response(ticket_number)
    
    def _create_technician_message(self, ticket_number, tenant_name, issue_type, description):
        """إنشاء رسالة للفني"""
        return f"""
🔧 *طلب صيانة جديد*
─────────────────
📋 رقم التذكرة: #{ticket_number}
👤 المستأجر: {tenant_name}
🔧 نوع العطل: {issue_type}
📝 الوصف: {description[:100]}...
⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')}
─────────────────
يرجى التواصل مع المستأجر خلال ٢٤ ساعة.
        """.strip()
    
    def _create_tenant_response(self, ticket_number, technician, issue_type):
        """إنشاء رد للمستأجر مع تفاصيل الفني"""
        return f"""
✅ *تم استلام بلاغك بنجاح*
─────────────────
📋 رقم التذكرة: #{ticket_number}
🔧 نوع العطل: {issue_type}
👨‍🔧 الفني المسؤول: {technician.name}
📞 هاتف الفني: {technician.phone}
⏰ سيتم التواصل خلال ٢٤ ساعة
─────────────────
شكراً لثقتكم بنا
        """.strip()
    
    def _create_general_response(self, ticket_number):
        """إنشاء رد عام للمستأجر"""
        return f"""
✅ تم استلام بلاغك بنجاح
📋 رقم التذكرة: #{ticket_number}
⏰ سيتواصل معك أحد الفنيين قريباً
        """.strip()
    
    def _detect_issue_type(self, message):
        """الكشف التلقائي عن نوع العطل"""
        message_lower = message.lower()
        
        electric_keywords = ['كهرب', 'تيار', 'إنارة', 'لمبة', 'مصباح', 'فيوز', 'قاطع', 'كهربائ']
        plumbing_keywords = ['سباك', 'ماء', 'صنبور', 'حمام', 'مرحاض', 'مواسير', 'تسرب', 'سباكة']
        painting_keywords = ['دهان', 'نقاش', 'حائط', 'جدار', 'طلاء', 'لون', 'نقاشة']
        
        if any(word in message_lower for word in electric_keywords):
            return 'كهرباء'
        elif any(word in message_lower for word in plumbing_keywords):
            return 'سباكة'
        elif any(word in message_lower for word in painting_keywords):
            return 'نقاشة'
        else:
            return 'عامة'
    
    def get_maintenance_status(self, phone_number):
        """الحصول على حالة تذاكر الصيانة"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.ticket_number, m.description, m.status, m.issue_type, m.created_at
            FROM maintenance m
            JOIN tenants t ON m.tenant_id = t.id
            WHERE t.phone = ? AND m.status != 'closed'
            ORDER BY m.created_at DESC
        ''', (phone_number,))
        
        tickets = cursor.fetchall()
        conn.close()
        
        if not tickets:
            return "📋 لا توجد لديك تذاكر صيانة نشطة"
        
        response = "📋 *تذاكر الصيانة النشطة*\n─────────────────\n"
        for ticket in tickets:
            status_emoji = "🟢" if ticket['status'] == 'closed' else "🟡" if ticket['status'] == 'in_progress' else "🔴"
            response += f"""
{status_emoji} التذكرة #{ticket['ticket_number']}
📝 {ticket['description'][:50]}...
🔧 {ticket['issue_type']}
📊 {ticket['status']}
⏰ {ticket['created_at']}
─────────────────
            """.strip() + "\n"
        
        return response
