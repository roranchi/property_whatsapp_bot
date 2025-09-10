import hmac
import hashlib
import os
import logging

logger = logging.getLogger(__name__)

def verify_webhook_signature(signature, payload):
    """التحقق من التوقيع الرقمي لضمان أن الطلب من واتساب"""
    if not signature:
        logger.warning("No signature provided")
        return False
    
    if not signature.startswith('sha256='):
        logger.warning(f"Invalid signature format: {signature}")
        return False
    
    # استخدام WHATSAPP_APP_SECRET للتحقق (ليس ACCESS_TOKEN)
    whatsapp_app_secret = os.environ.get('WHATSAPP_APP_SECRET', '').encode('utf-8')
    
    if not whatsapp_app_secret:
        logger.error("WHATSAPP_APP_SECRET not set in environment variables")
        return False
    
    # إنشاء التوقيع المتوقع
    expected_signature = hmac.new(
        whatsapp_app_secret,
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # إضافة 'sha256=' للتوقيع المتوقع
    expected_signature_with_prefix = 'sha256=' + expected_signature
    
    # إزالة 'sha256=' من التوقيع المستلم للمقارنة
    received_signature = signature[7:]  # إزالة 'sha256=' من البداية
    
    # المقارنة الآمنة
    result = hmac.compare_digest(expected_signature_with_prefix, signature)
    
    if not result:
        logger.warning(f"Signature verification failed. Expected: {expected_signature_with_prefix}, Received: {signature}")
    
    return result