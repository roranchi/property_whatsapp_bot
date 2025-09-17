import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env في المجلد الرئيسي
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

DATABASE_URL = os.getenv('DATABASE_URL')
WHATSAPP_API_TOKEN = os.getenv('WHATSAPP_API_TOKEN')
WHATSAPP_PHONE_NUMBER = os.getenv('WHATSAPP_PHONE_NUMBER')

try:
    if DATABASE_URL:
        # إنشاء pool للاتصالات مع إعدادات SSL
        connection_pool = SimpleConnectionPool(
            1, 20, 
            dsn=DATABASE_URL,
            sslmode="require"
        )
        print("✅ تم تهيئة connection pool بنجاح")
    else:
        print("⚠️ لم يتم العثور على DATABASE_URL. تأكد من وجوده في ملف .env")
        exit()
except psycopg2.OperationalError as e:
    print(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
    exit()

def get_db_connection():
    """الحصول على اتصال من الـ pool"""
    if connection_pool:
        return connection_pool.getconn()
    return None

def release_db_connection(conn):
    """إعادة الاتصال إلى الـ pool"""
    if connection_pool and conn:
        connection_pool.putconn(conn)
