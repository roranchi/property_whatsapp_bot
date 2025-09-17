from app import create_app
import threading
import time
from services.payment_collector import run_daily_collection

app = create_app()

def payment_scheduler():
    print("⏰ بدء جدولة المدفوعات اليومية...")
    while True:
        try:
            current_time = time.strftime("%H:%M")
            if current_time == "09:00":
                print("🕘 الوقت 9:00 صباحاً - بدء التجميع...")
                run_daily_collection()
                time.sleep(3600)
            time.sleep(60)
        except Exception as e:
            print(f"❌ خطأ في الجدولة: {e}")
            time.sleep(300)

scheduler_thread = threading.Thread(target=payment_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
