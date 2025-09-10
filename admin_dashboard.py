from flask import Flask, render_template_string

app = Flask(__name__)

# ========== لوحة التحكم الإدارية ========== #
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>لوحة تحكم نظام العقارات</title>
    <style>
        body { 
            font-family: 'Arial', sans-serif; 
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #2c3e50; 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .menu { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 25px; 
            margin-top: 40px; 
        }
        .menu-item { 
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white; 
            padding: 30px 20px; 
            text-align: center; 
            border-radius: 12px; 
            text-decoration: none; 
            transition: all 0.3s ease;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }
        .menu-item:hover { 
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(52, 152, 219, 0.5);
            background: linear-gradient(45deg, #2980b9, #3498db);
        }
        .icon {
            font-size: 2em;
            margin-bottom: 15px;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 لوحة تحكم نظام إدارة العقارات</h1>
        <div class="menu">
            <a href="/admin/owners" class="menu-item">
                <span class="icon">👥</span>
                إدارة الملاك
            </a>
            <a href="/admin/tenants" class="menu-item">
                <span class="icon">🏠</span>
                إدارة المستأجرين
            </a>
            <a href="/admin/payments" class="menu-item">
                <span class="icon">💳</span>
                إدارة المدفوعات
            </a>
            <a href="/admin/maintenance" class="menu-item">
                <span class="icon">🔧</span>
                طلبات الصيانة
            </a>
            <a href="/admin/reports" class="menu-item">
                <span class="icon">📊</span>
                التقارير والإحصائيات
            </a>
            <a href="/admin/settings" class="menu-item">
                <span class="icon">⚙️</span>
                الإعدادات
            </a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return "🚀 نظام إدارة العقارات يعمل! تفضلي بـ /admin"

@app.route('/admin')
def admin_dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/admin/owners')
def manage_owners():
    return """
    <div style='text-align: center; padding: 50px; font-family: Arial;'>
        <h1>👥 إدارة الملاك</h1>
        <p style='font-size: 1.2em;'>هذه الصفحة تحت التطوير...</p>
        <a href='/admin' style='display: inline-block; margin-top: 20px; padding: 10px 20px; 
            background: #3498db; color: white; text-decoration: none; border-radius: 5px;'>
            العودة للوحة التحكم
        </a>
    </div>
    """

@app.route('/admin/tenants')
def manage_tenants():
    return """
    <div style='text-align: center; padding: 50px; font-family: Arial;'>
        <h1>🏠 إدارة المستأجرين</h1>
        <p style='font-size: 1.2em;'>هذه الصفحة تحت التطوير...</p>
        <a href='/admin' style='display: inline-block; margin-top: 20px; padding: 10px 20px; 
            background: #3498db; color: white; text-decoration: none; border-radius: 5px;'>
            العودة للوحة التحكم
        </a>
    </div>
    """

@app.route('/admin/payments')
def manage_payments():
    return """
    <div style='text-align: center; padding: 50px; font-family: Arial;'>
        <h1>💳 إدارة المدفوعات</h1>
        <p style='font-size: 1.2em;'>هذه الصفحة تحت التطوير...</p>
        <a href='/admin' style='display: inline-block; margin-top: 20px; padding: 10px 20px; 
            background: #3498db; color: white; text-decoration: none; border-radius: 5px;'>
            العودة للوحة التحكم
        </a>
    </div>
    """

@app.route('/admin/maintenance')
def manage_maintenance():
    return """
    <div style='text-align: center; padding: 50px; font-family: Arial;'>
        <h1>🔧 طلبات الصيانة</h1>
        <p style='font-size: 1.2em;'>هذه الصفحة تحت التطوير...</p>
        <a href='/admin' style='display: inline-block; margin-top: 20px; padding: 10px 20px; 
            background: #3498db; color: white; text-decoration: none; border-radius: 5px;'>
            العودة للوحة التحكم
        </a>
    </div>
    """

if __name__ == '__main__':
    print("🚀 لوحة التحكم جاهزة على: http://127.0.0.1:5001")
    print("📋 تفضلي بزيارة: http://127.0.0.1:5001/admin")
    app.run(debug=True, host='0.0.0.0', port=5001)