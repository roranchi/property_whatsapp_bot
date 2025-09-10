#!/usr/bin/env python3
# تقارير الصيانة - حسب الخطة الأصلية

import sqlite3
import sys
import os
from datetime import datetime, timedelta

# إضافة المسار الحالي إلى Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from database.connection import get_connection

class MaintenanceReports:
    @staticmethod
    def generate_daily_report():
        """تقرير يومي عن الصيانة - حسب الخطة"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # إحصائيات اليوم
        today = datetime.now().date()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_tickets,
                SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open_tickets,
                SUM(CASE WHEN status = 'assigned' THEN 1 ELSE 0 END) as assigned_tickets,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_tickets,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tickets
            FROM maintenance
            WHERE DATE(created_at) = ?
        ''', (today,))
        
        stats = cursor.fetchone()
        
        # التذاكر حسب النوع
        cursor.execute('''
            SELECT issue_type, COUNT(*) as count
            FROM maintenance
            WHERE DATE(created_at) = ?
            GROUP BY issue_type
        ''', (today,))
        
        by_type = cursor.fetchall()
        
        conn.close()
        
        return {
            'date': today,
            'stats': dict(stats) if stats else {},
            'by_type': [dict(row) for row in by_type]
        }

if __name__ == "__main__":
    report = MaintenanceReports.generate_daily_report()
    print("📊 تقرير الصيانة اليومي - مطابق للخطة الأصلية")
