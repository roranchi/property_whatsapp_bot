import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # إعدادات واتساب من .env
    WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', '')
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
    WHATSAPP_APP_SECRET = os.getenv('WHATSAPP_APP_SECRET', '')
    
    # إعدادات التطبيق من .env
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key_change_in_production')
    PORT = int(os.getenv('PORT', 3000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # إعدادات قاعدة البيانات
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///property.db')
    
    # إعدادات الإدارة
    ADMIN_NUMBERS = os.getenv('ADMIN_NUMBERS', '+96891234567,+96898765432').split(',')
    
    # إعدادات التسعير
    BASIC_PRICE = 5
    ADVANCED_PRICE = 8
    PROFESSIONAL_PRICE = 12

# إنشاء كائن الإعدادات
config = Config()
