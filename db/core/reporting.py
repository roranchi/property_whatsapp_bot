from datetime import datetime, timedelta
from core.db import get_db_connection
from core.payments import PaymentManager
from core.contracts import ContractManager

class ReportGenerator:
    @staticmethod
    def generate_daily_report():
        """تقرير يومي شامل"""
        payment_report = PaymentManager.get_todays_payments()
        overdue_report = PaymentManager.get_overdue_payments()
        contract_report = ContractManager.get_contracts_report()
        
        report_text = f"""
📊 التقرير اليومي - {datetime.now().strftime('%Y-%m-%d')}
{contract_report}

{payment_report}

{overdue_report}
        """
        return report_text

    @staticmethod
    def generate_weekly_report():
        """تقرير أسبوعي"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # حساب بداية الأسبوع (السبت)
        today = datetime.now().date()
        start_week = today - timedelta(days=today.weekday() + 2)  # 
adjusted for week start Saturday
        
        cursor.execute("""
            SELECT t.name, p.amount, p.method, p.payment_date
            FROM payments p
            JOIN tenants t ON p.tenant_id = t.id
            WHERE p.payment_date BETWEEN ? AND ?
        """, (start_week.strftime('%Y-%m-%d'), 
today.strftime('%Y-%m-%d')))
        
        weekly_payments = cursor.fetchall()
        conn.close()
        
        if not weekly_payments:
            return "لا توجد مدفوعات هذا الأسبوع."
        
        report_text = "📈 التقرير الأسبوعي:\n"
        total = 0
        for payment in weekly_payments:
            report_text += f"• {payment['name']}: {payment['amount']} ريال 
({payment['method']}) - {payment['payment_date']}\n"
            total += payment['amount']
        
        report_text += f"\nالمجموع الأسبوعي: {total} ريال"
        return report_text

    @staticmethod
    def generate_monthly_report():
        """تقرير شهري"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        today = datetime.now().date()
        start_month = today.replace(day=1)
        
        cursor.execute("""
            SELECT t.name, p.amount, p.method, p.payment_date
            FROM payments p
            JOIN tenants t ON p.tenant_id = t.id
            WHERE p.payment_date BETWEEN ? AND ?
        """, (start_month.strftime('%Y-%m-%d'), 
today.strftime('%Y-%m-%d')))
        
        monthly_payments = cursor.fetchall()
        conn.close()
        
        if not monthly_payments:
            return "لا توجد مدفوعات هذا الشهر."
        
        report_text = "📊 التقرير الشهري:\n"
        total = 0
        for payment in monthly_payments:
            report_text += f"• {payment['name']}: {payment['amount']} ريال 
({payment['method']}) - {payment['payment_date']}\n"
            total += payment['amount']
        
        report_text += f"\nالمجموع الشهري: {total} ريال"
        return report_text

    @staticmethod
    def generate_custom_report(report_type):
        """توليد تقارير مخصصة حسب الطلب"""
        if report_type == "daily":
            return ReportGenerator.generate_daily_report()
        elif report_type == "weekly":
            return ReportGenerator.generate_weekly_report()
        elif report_type == "monthly":
            return ReportGenerator.generate_monthly_report()
        elif report_type == "payments":
            return PaymentManager.get_todays_payments()
        elif report_type == "overdue":
            return PaymentManager.get_overdue_payments()
        elif report_type == "contracts":
            return ContractManager.get_contracts_report()
        else:
            return "نوع التقرير غير معروف. استخدم: daily, weekly, monthly, 
payments, overdue, contracts"



