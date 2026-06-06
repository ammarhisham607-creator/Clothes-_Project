import streamlit as st
import requests
import json
import base64
import time

# 1️⃣ ديكور النيون والبرق الحركي (CSS Custom Styling)
def inject_neon_theme():
    neon_css = """
    <style>
    /* الخلفية الداكنة ولمسات النيون */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    
    /* عنوان الموقع الرئيسي تأثير البرق والنيون */
    .neon-title {
        font-size: 45px;
        font-weight: bold;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff;
        animation: lightning-blink 2s infinite alternate;
        margin-bottom: 30px;
    }
    
    /* كروت الكتب العادية */
    .book-card {
        border: 1px solid #1f2833;
        border-radius: 10px;
        padding: 15px;
        background-color: #1f2833;
        box-shadow: 0 4px 15px rgba(0, 243, 255, 0.1);
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .book-card:hover {
        box-shadow: 0 4px 20px rgba(0, 243, 255, 0.4);
        transform: scale(1.02);
    }

    /* كروت قسم العروض (تأثير البرق الوردي المشتعل) */
    .offer-card {
        border: 2px solid #ff0055;
        border-radius: 12px;
        padding: 15px;
        background: linear-gradient(135deg, #1f2833 0%, #2d142c 100%);
        box-shadow: 0 0 15px #ff0055, inset 0 0 10px #ff0055;
        margin-bottom: 20px;
        animation: lightning-glow 1.5s infinite ease-in-out;
    }
    
    /* شارة العرض المشتعلة */
    .offer-badge {
        background-color: #ff0055;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 12px;
        text-shadow: 0 0 5px #fff;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* الأنيكيشن الخاصة بالبرق والوهج */
    @keyframes lightning-blink {
        0%, 100% { text-shadow: 0 0 5px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; }
        92% { text-shadow: 0 0 5px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; }
        93% { text-shadow: none; color: #888; }
        94% { text-shadow: 0 0 5px #00f3ff, 0 0 20px #00f3ff; }
        95% { text-shadow: none; color: #666; }
        96% { text-shadow: 0 0 8px #00f3ff, 0 0 25px #00f3ff, 0 0 50px #00f3ff; }
    }
    @keyframes lightning-glow {
        0%, 100% { box-shadow: 0 0 10px #ff0055, inset 0 0 5px #ff0055; }
        50% { box-shadow: 0 0 25px #00ffcc, inset 0 0 12px #00ffcc; border-color: #00ffcc; }
    }
    </style>
    """
    st.markdown(neon_css, unsafe_allow_html=True)

# 2️⃣ دالة رفع الصور الذكية إلى GitHub لضمان عدم اختفائها
def upload_image_to_github(file_bytes, filename):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
    except Exception:
        st.error("❌ تأكد من إعداد GITHUB_TOKEN و GITHUB_REPO في الـ Secrets!")
        return None

    # تحويل الصورة إلى Base64 لرفعها عبر الـ API
    encoded_content = base64.b64encode(file_bytes).decode("utf-8")
    
    # تنظيف اسم الملف وإضافة تايم-ستامب لمنع التكرار
    clean_filename = f"img_{int(time.time())}_{filename.replace(' ', '_')}"
    path = f"images/{clean_filename}"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"رفع صورة كتاب جديدة: {clean_filename}",
        "content": encoded_content,
        "branch": "main"  # أو master حسب مستودعك
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        # إرجاع رابط الصورة المباشر من جيت هب
        return f"https://raw.githubusercontent.com/{repo}/main/{path}"
    else:
        st.error(f"فشل الرفع لجيت هب: {response.json().get('message', '')}")
        return None

# دالة محاكاة لجلب وحفظ البيانات (استبدلها بالدوال الفندامنتال عندك)
def load_books():
    if 'books_db' not in st.session_state:
        st.session_state.books_db = [
            {"title": "كتاب نموذج 1", "price": 150, "is_offer": True, "old_price": 250, "image": "https://via.placeholder.com/150", "category": "روايات"},
            {"title": "كتاب نموذج 2", "price": 120, "is_offer": False, "old_price": 120, "image": "https://via.placeholder.com/150", "category": "علم نفس"}
        ]
    return st.session_state.books_db

# تشغيل الثيم والموقع
inject_neon_theme()
st.markdown('<div class="neon-title">⚡ WORLD OF BOOKS ⚡</div>', unsafe_allow_html=True)

# القائمة الجانبية للموقع
menu = st.sidebar.selectbox("🚀 تنقل في الموقع", ["🏠 متجر الكتب", "🔥 قسم العروض الحصرية", "⚙️ لوحة الإدارة"])
books = load_books()

# ==================== [ 🏠 متجر الكتب ] ====================
if menu == "🏠 متجر الكتب":
    st.subheader("📚 جميع الكتب المتاحة")
    cols = st.columns(2)
    for idx, book in enumerate(books):
        with cols[idx % 2]:
            if book.get("is_offer"):
                # إذا كان كتاب عادي لكن عليه عرض يظهر بشكل مميز أيضاً
                st.markdown(f'<div class="offer-card"><div class="offer-badge">⚡ عرض خاص</div><h3>{book["title"]}</h3><p>السعر: <del>{book["old_price"]} ج.م</del> <b>{book["price"]} ج.م</b></p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="book-card"><h3>{book["title"]}</h3><p>السعر: {book["price"]} ج.م</p></div>', unsafe_allow_html=True)
            st.image(book["image"], use_container_width=True)
            st.button("إضافة للعربة 🛒", key=f"buy_{idx}")

# ==================== [ 🔥 قسم العروض الحصرية ] ====================
elif menu == "🔥 قسم العروض الحصرية":
    st.markdown("<h2 style='color: #ff0055; text-shadow: 0 0 10px #ff0055;'>💥 أقوى عروض البرق والخصومات لفترة محدودة!</h2>", unsafe_allow_html=True)
    
    # تصفية الكتب التي تحتوي على عروض فقط
    offer_books = [b for b in books if b.get("is_offer") == True]
    
    if not offer_books:
        st.info("لا توجد عروض نشطة حالياً، انتظرونا قريباً! ⚡")
    else:
        cols = st.columns(2)
        for idx, book in enumerate(offer_books):
            with cols[idx % 2]:
                # كارت مخصص ومشع بالبرق للعروض
                st.markdown(f"""
                <div class="offer-card">
                    <div class="offer-badge">🔥 وفّر {int(book['old_price'] - book['price'])} ج.م</div>
                    <h3 style='color: #fff;'>{book['title']}</h3>
                    <p style='font-size: 18px;'>
                        السعر القديم: <span style='text-decoration: line-through; color: #ff0055;'>{book['old_price']} ج.م</span><br>
                        <span style='color: #00ffcc; font-weight: bold;'>السعر الحالي: {book['price']} ج.م ⚡</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.image(book["image"], use_container_width=True)
                st.button("اقتنص العرض فوراً 🛍️", key=f"offer_buy_{idx}")

# ==================== [ ⚙️ لوحة الإدارة ] ====================
elif menu == "⚙️ لوحة الإدارة":
    st.subheader("🛠️ إضافة وتعديل الكتب والعروض")
    
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("اسم الكتاب:")
        category = st.selectbox("التصنيف:", ["روايات", "علم نفس", "تطوير ذات", "بيزنس"])
        
        # مدخلات قسم العروض الجديدة
        st.markdown("---")
        is_offer = st.checkbox("هل تريد وضع هذا الكتاب في قسم العروض؟ 🔥")
        
        col1, col2 = st.columns(2)
        with col1:
            price = st.number_input("السعر الحالي (سعر البيع):", min_value=0)
        with col2:
            old_price = st.number_input("السعر الأصلي قبل العرض (إذا لم يكن عليه عرض اتركه مساوياً للسعر الحالي):", min_value=0)
        
        # رفع الصورة وحل المشكلة
        uploaded_file = st.file_uploader("اختر صورة الكتاب (سيتم رفعها مباشرة وحفظها على الـ GitHub):", type=["jpg", "png", "jpeg"])
        st.markdown("---")
        
        submit = st.form_submit_form_button("إضافة الكتاب إلى السيستم 🚀")
        
        if submit:
            if title and uploaded_file:
                with st.spinner("⚡ جاري معالجة ورفع الصورة إلى GitHub بدقة..."):
                    file_bytes = uploaded_file.read()
                    # رفع الصورة لـ GitHub وجلب الرابط المباشر
                    img_url = upload_image_to_github(file_bytes, uploaded_file.name)
                    
                    if img_url:
                        # إنشاء كائن الكتاب الجديد
                        new_book = {
                            "title": title,
                            "price": price,
                            "is_offer": is_offer,
                            "old_price": old_price if is_offer else price,
                            "image": img_url,
                            "category": category
                        }
                        
                        # حفظ في قاعدة البيانات
                        st.session_state.books_db.append(new_book)
                        # (ملحوظة: هنا تقوم باستدعاء دالة الحفظ الخاصة بك لتحديث ملف books.json على جيت هب)
                        
                        st.success(f"✔️ تم رفع الصورة بنجاح على الرابط المتين، وتم إضافة كتاب '{title}' بنجاح!")
                        st.rerun()
            else:
                st.error("❌ من فضلك أكتب اسم الكتاب وارفع الصورة أولاً!")
