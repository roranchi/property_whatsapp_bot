# قوالب رسائل تجديد العقود - WhatsApp Templates

class ContractTemplates:
    @staticmethod
    def contract_90_days_reminder(tenant_name, end_date, days_left):
        """قالب تنبيه 90 يوم"""
        return f"""
*تنبيه تجديد عقد 🏢*

عزيزي/عزيزتي {tenant_name},

يرجى العلم أن عقد الإيجار الحالي سينتهي خلال {days_left} يوم (في تاريخ {end_date}).

نأمل منكم التواصل لتحديد موعد تجديد العقد.

مع خالص التقدير،
إدارة العقارات
        """.strip()

    @staticmethod
    def contract_60_days_reminder(tenant_name, end_date, days_left):
        """قالب تنبيه 60 يوم"""
        return f"""
*تذكير تجديد عقد ⏳*

السيد/السيدة {tenant_name},

باقي {days_left} يوم فقط على انتهاء عقد الإيجار (تاريخ الانتهاء: {end_date}).

الرجاء تحديد موعد لمراجعة وتجديد العقد.

شكراً لتعاونكم،
إدارة العقارات
        """.strip()

    @staticmethod
    def contract_30_days_reminder(tenant_name, end_date, days_left):
        """قالب تنبيه 30 يوم"""
        return f"""
*تنبيه مهم! 🔔*

الأستاذ/الأستاذة {tenant_name},

باقي {days_left} يوم على انتهاء العقد ({end_date}).

يرجى التواصل العاجل لإتمام إجراءات التجديد.

مع التقدير،
إدارة العقارات
        """.strip()

    @staticmethod
    def contract_7_days_reminder(tenant_name, end_date, days_left):
        """قالب تنبيه 7 أيام"""
        return f"""
*تنبيه عاجل! 🚨*

السيد/السيدة {tenant_name} المحترم/ة,

باقي {days_left} أيام فقط على انتهاء العقد (تاريخ {end_date}).

التواصل العاجل ضروري لتجنب انقطاع الخدمات.

إدارة العقارات
        """.strip()
