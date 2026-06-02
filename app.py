from flask import Flask, render_template_string

app = Flask(__name__)

# قاعدة بيانات مصغرة للكتب
books = [
    {"id": 1, "title": "رواية الخيميائي", "author": "باولو كويلو", "price": 150, "image": "https://via.placeholder.com/150"},
    {"id": 2, "title": "أصلياء", "author": "دان براون", "price": 200, "image": "https://via.placeholder.com/150"},
    {"id": 3, "title": "فن اللامبالاة", "author": "مارك مانسون", "price": 120, "image": "https://via.placeholder.com/150"}
]

# كود الواجهة وتصميم الموقع (HTML & CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>مكتبتي للروايات</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; text-align: center; margin: 0; padding: 0; }
        header { background-color: #2c3e50; color: white; padding: 20px; font-size: 24px; }
        .container { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; padding: 40px; }
        .book-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); width: 220px; transition: transform 0.3s; }
        .book-card:hover { transform: translateY(-5px); }
        .book-card img { width: 100%; border-radius: 8px; }
        .book-title { font-size: 20px; font-weight: bold; margin: 15px 0 5px; color: #333; }
        .book-author { color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }
        .book-price { color: #27ae60; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
        .buy-btn { background: #3498db; color: white; border: none; padding: 12px; width: 100%; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; }
        .buy-btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <header>📚 أهلاً بك في متجر الكتب والروايات</header>
    
    <div class="container">
        {% for book in books %}
        <div class="book-card">
            <img src="{{ book.image }}" alt="غلاف {{ book.title }}">
            <div class="book-title">{{ book.title }}</div>
            <div class="book-author">{{ book.author }}</div>
            <div class="book-price">{{ book.price }} جنيه</div>
            <button class="buy-btn" onclick="alert('تمت إضافة ({{ book.title }}) إلى سلة المشتريات بنجاح!')">أضف إلى السلة</button>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# ربط واجهة الموقع بلغة البايثون
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, books=books)

if __name__ == '__main__':
    # تشغيل الموقع
    app.run(debug=True)
