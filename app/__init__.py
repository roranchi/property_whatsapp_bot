from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    
    # تحميل الإعدادات من متغيرات البيئة
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # إعداد rate limiting
    limiter.init_app(app)
    
    # استيراد وتفعيل الواجهات (Routes)
    from app.routes.webhook import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app