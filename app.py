import streamlit as st
import requests
import json
import base64
import time
from urllib.parse import quote

# ضبط إعدادات الصفحة الرئيسية للمكتبة
st.set_page_config(
    page_title="متجر عالم الكتب | World of Books 📚",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1️⃣ تصميم ثيم النيون والبرق الحركي المخصص للمكتبة (Neon & Lightning CSS)
def inject_neon_theme():
    neon_css = """
    <style>
    /* خلفية داكنة فخمة تبرز توهج الكتب والنيون */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
        font-family: 'Cairo', sans-serif;
    }
    
    /* عنوان المكتبة الرئيسي بتأثير رعشة البرق والكهرباء */
    .neon-title {
        font-size: 50px;
        font-weight: 900;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff;
        animation: lightning-blink 2.5s infinite alternate;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    
    .neon-subtitle {
        text-align: center;
        color: #00f3ff;
        font-size: 18px;
        margin-bottom: 35px;
        text-shadow: 0 0 5px rgba(0, 243, 255, 0.5);
    }
    
    /* كروت الكتب العادية */
    .book-card {
        border: 1px solid #1f2833;
        border-radius: 12px;
        padding: 18px;
        background-color: #1f2833;
        box-shadow: 0 4px 15px rgba(0, 243, 255, 0.05);
        margin-bottom: 25px;
        transition: 0.3s ease-in-out;
        text-align: right;
    }
    .book-card:hover {
        box-shadow: 0 4px 25px rgba(0, 243, 255, 0.3);
        transform: translateY(-5px);
    }

    /* كروت قسم العروض والخصومات (وهج البرق المشتعل) */
    .offer-card {
        border: 2px solid #ff0055;
        border-radius: 12px;
        padding: 18px;
        background: linear-gradient(135deg, #1f2833 0%, #2d142c 100%);
        box-shadow: 0 0 15px #ff0055, inset 0 0 8px #ff0055;
        margin-bottom: 25px;
        animation: lightning-glow 2s infinite ease-in-out;
        text-align: right;
    }
    
    /* شارة الخصم الفسفورية */
    .offer-badge {
        background-color: #ff0055;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
        text-shadow: 0 0 5px #fff;
        display: inline-block;
        margin-bottom: 12px;
    }

    /* أنيميشن ضربات البرق الكهربائية للعنوان */
    @keyframes lightning-blink {
        0%, 100% { text-shadow: 0 0 5px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; }
        92% { text-shadow: 0 0 5px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; }
        93% { text-shadow: none; color: #444; }
        94% { text-shadow: 0 0 5px #00f3ff, 0 0 20px #00f3ff; }
        95% { text-shadow: none; color: #333; }
        96% { text-shadow: 0 0 8px #00f3ff, 0 0 25px #00f3ff, 0 0 50px #00f3ff; }
    }
    
    /* أنيميشن توهج وتبديل ألوان النيون في كروت العروض */
    @keyframes lightning-glow {
        0%, 100% { box-shadow: 0 0 12px #ff0055, inset 0 0 6px #ff0055; border-color: #ff0055; }
        50% { box-shadow: 0 0 25px #00ffcc, inset 0 0 12px #00ffcc; border-color: #00ffcc; }
    }
    </style>
    """
    st.markdown(neon_css, unsafe_allow_html=True)

# 2️⃣ دالة رفع الصور الذكية لـ GitHub (لحل مشكلة اختفاء الصور على السيرفر)
def upload_image_to_github(file_bytes, filename):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
    except Exception:
        st.error("❌ خطأ في الـ Secrets: تأكد من إضافة GITHUB_TOKEN و GITHUB_REPO في لوحة تحكم Streamlit.")
        return None

    # تحويل الصورة إلى base64 لرفعها عبر الـ API
    encoded_content = base64.b64encode(file_bytes).decode("utf-8")
    
    # اسم فريد لكل صورة بناءً على الوقت منعاً للتكرار
    clean_filename = f"book_{int(time.time())}_{filename.replace(' ', '_')}"
    path = f"images/{clean_filename}"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"رفع صورة كتاب جديدة: {clean_filename}",
        "content": encoded_content,
        "branch": "main"
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        # الرابط الدائم للملف على جيت هب
        return f"https://raw.githubusercontent.com/{repo}/main/{path}"
    else:
        st.error(f"فشل الرفع إلى جيت هب: {response.json().get('message', '')}")
        return None

# 3️⃣ إدارة جلب وتخزين بيانات الكتب عبر ملف الـ JSON السحابي على جيت هب
def load_books_data():
    if "books_list" in st.session_state:
        return st.session_state["books_list"]
        
    # كتب افتراضية في حال لم يتم جلب الملف بنجاح بعد
    fallback_books = [
        {"title": "رواية أرض زيكولا", "price": 90, "is_offer": True, "old_price": 120, "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500", "category": "روايات"},
        {"title": "كتاب العادات الذرية", "price": 140, "is_offer": False, "old_price": 140, "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500", "category": "تطوير ذات"}
    ]
    
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        url = f"https://api.github.com/repos/{repo}/contents/books.json"
        headers = {"Authorization": f"token {token}"}
        
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            file_content = base64.b64decode(res.json()['content']).decode('utf-8')
            st.session_state["books_list"] = json.loads(file_content)
            return st.session_state["books_list"]
    except Exception:
        pass
        
    st.session_state["books_list"] = fallback_books
    return fallback_books

def save_books_data(updated_list):
    st.session_state["books_list"] = updated_list
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        url = f"https://api.github.com/repos/{repo}/contents/books.json"
        headers = {"Authorization": f"token {token}"}
        
        res = requests.get(url, headers=headers)
        sha = res.json()['sha'] if res.status_code == 200 else None
        
        json_string = json.dumps(updated_list, ensure_ascii=False, indent=4)
        encoded = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')
        
        data = {
            "message": "تحديث مستودع كتب المتجر",
            "content": encoded,
            "branch": "main"
        }
        if sha:
            data["sha"] = sha
            
        requests.put(url, headers=headers, json=data)
    except Exception:
        pass

# تهيئة عربة المشتريات للزائر
if "book_cart" not in st.session_state:
    st.session_state.book_cart = []

# تفعيل النيون والبرق في الواجهة
inject_neon_theme()
st.markdown('<div class="neon-title">⚡ WORLD OF BOOKS ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">⚡ بوابتك السحرية لأقوى الكتب والروايات بتأثيرات النيون المشعة ⚡</div>', unsafe_allow_html=True)

# 4️⃣ قائمة التنقل الجانبية
st.sidebar.markdown("<h2 style='text-align:center; color:#00f3ff;'>⚡ أقسام القائمة ⚡</h2>", unsafe_allow_html=True)
menu = st.sidebar.selectbox(
    "اختر وجهتك:",
    ["🏠 مكتبة الكتب الرئيسية", "🔥 قسم العروض والخصومات", "🛒 عربة القراءة والمشتريات", "⚙️ لوحة تحكم الإدارة"]
)

books = load_books_data()

# ==================== [ 🏠 مكتبة الكتب الرئيسية ] ====================
if menu == "🏠 مكتبة الكتب الرئيسية":
    st.markdown("<h2 style='text-align:right; color:#00f3ff;'>📚 جميع الكتب المتاحة بالمتجر</h2>", unsafe_allow_html=True)
    
    if not books:
        st.warning("جاري ملء الرفوف بالكتب والروايات... انتظرونا!")
    else:
        cols = st.columns(2)
        for idx, book in enumerate(books):
            with cols[idx % 2]:
                if book.get("is_offer"):
                    st.markdown(f"""
                    <div class="offer-card">
                        <div class="offer-badge">⚡ عرض خاص</div>
                        <h3>{book['title']}</h3>
                        <p>التصنيف: {book.get('category', 'عام')}</p>
                        <p style='font-size:18px;'>السعر: <del style='color:#ff0055;'>{book.get('old_price')} ج.م</del> <b style='color:#00ffcc;'>{book['price']} ج.م</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <p>التصنيف: {book.get('category', 'عام')}</p>
                        <p style='font-size:18px; color:#00f3ff;'>السعر: <b>{book['price']} ج.م</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if book.get("image"):
                    st.image(book["image"], use_container_width=True)
                
                if st.button(f"إضافة لعربة المشتريات 🛒", key=f"add_b_{idx}"):
                    st.session_state.book_cart.append(book)
                    st.success(f"✔️ أضيف كتاب '{book['title']}' إلى عربتك!")

# ==================== [ 🔥 قسم العروض والخصومات ] ====================
elif menu == "🔥 قسم العروض والخصومات":
    st.markdown("<h2 style='text-align:right; color:#ff0055; text-shadow: 0 0 10px #ff0055;'>💥 عروض البرق الخاطفة على الروايات والكتب!</h2>", unsafe_allow_html=True)
    
    # تصفية الكتب اللي عليها عروض فقط
    offer_books = [b for b in books if b.get("is_offer") == True]
    
    if not offer_books:
        st.info("لا توجد عروض نشطة حالياً، انتظروا كولكشن عروض المعرض القادم! ⚡")
    else:
        cols = st.columns(2)
        for idx, book in enumerate(offer_books):
            with cols[idx % 2]:
                saving = int(book.get('old_price', 0) - book.get('price', 0))
                st.markdown(f"""
                <div class="offer-card">
                    <div class="offer-badge">🔥 وفرت {saving} ج.م من سعر الكتاب</div>
                    <h3>{book['title']}</h3>
                    <p style='font-size: 18px;'>
                        السعر الأصلي: <span style='text-decoration: line-through; color: #ff0055;'>{book.get('old_price')} ج.م</span><br>
                        <span style='color: #00ffcc; font-weight: bold; font-size:22px;'>سعر العرض الحركي: {book['price']} ج.م ⚡</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if book.get("image"):
                    st.image(book["image"], use_container_width=True)
                
                if st.button("اقتنص عرض الكتاب فوراً 🛍️", key=f"add_offer_b_{idx}"):
                    st.session_state.book_cart.append(book)
                    st.success("✔️ تم حجز نسخة من كتاب العرض في عربتك!")

# ==================== [ 🛒 عربة القراءة والمشتريات ] ====================
elif menu == "🛒 عربة القراءة والمشتريات":
    st.markdown("<h2 style='text-align:right; color:#00f3ff;'>🛒 الكتب التي اخترتها لقراءتها</h2>", unsafe_allow_html=True)
    
    if not st.session_state.book_cart:
        st.info("عربتك فارغة. اذهب للمكتبة واختر بعض الكتب لتغذية عقلك! 📚")
    else:
        total_price = 0
        for idx, cart_item in enumerate(st.session_state.book_cart):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"#### 📚 {cart_item['title']} - **{cart_item['price']} ج.م**")
                total_price += cart_item['price']
            with col2:
                if st.button("إزالة ❌", key=f"rem_b_{idx}"):
                    st.session_state.book_cart.pop(idx)
                    st.rerun()
        
        st.markdown(f"### 💰 الحساب الإجمالي للكتب: `{total_price} ج.م`")
        st.markdown("---")
        
        st.subheader("📝 بيانات استلام الأوردر وتأكيد التوصيل")
        with st.form("whatsapp_book_form"):
            user_name = st.text_input("اسم المستلم بالكامل:")
            user_phone = st.text_input("رقم الواتساب / الموبايل:")
            user_address = st.text_area("عنوان التوصيل بالتفصيل (المحافظة والمنطقة):")
            
            submit_order = st.form_submit_button("تأكيد وحجز طلب الكتب عبر الواتساب 💬")
            
            if submit_order:
                if user_name and user_phone and user_address:
                    books_details = ""
                    for i, item in enumerate(st.session_state.book_cart):
                        books_details += f"- كتاب {i+1}: {item['title']} ({item['price']} ج.م)\n"
                    
                    whatsapp_msg = (
                        f"🚨 *أوردر جديد من متجر World of Books* 🚨\n\n"
                        f"👤 *الاسم:* {user_name}\n"
                        f"📞 *الرقم:* {user_phone}\n"
                        f"📍 *العنوان:* {user_address}\n\n"
                        f"📚 *الكتب المطلوبة:*\n{books_details}\n"
                        f"💰 *الحساب الكلي للطلب:* {total_price} ج.م\n"
                        f"⚡ _برجاء تأكيد الشحن والتجهيز فوراً._"
                    )
                    
                    encoded_msg = quote(whatsapp_msg)
                    wa_url = f"https://wa.me/201200000000?text={encoded_msg}" # حط رقمك هنا مكان الاصفار
                    
                    st.markdown(f'<a href="{wa_url}" target="_blank" style="background-color:#25D366; color:white; padding:12px; border-radius:8px; text-decoration:none; font-weight:bold; display:block; text-align:center;">👉 اضغط هنا للانتقال الفوري للواتساب لإرسال أوردر الكتب</a>', unsafe_allow_html=True)
                    st.session_state.book_cart = [] 
                else:
                    st.error("❌ من فضلك اكتب اسمك وعنوانك بالكامل لحجز الأوردر!")

# ==================== [ ⚙️ لوحة تحكم الإدارة ] ====================
elif menu == "⚙️ لوحة تحكم الإدارة":
    st.markdown("<h2 style='text-align:right; color:#00f3ff;'>🛠️ لوحة إدارة الكتب والعروض للمتجر</h2>", unsafe_allow_html=True)
    
    st.markdown("### ➕ إضافة كتاب أو رواية جديدة للمتجر")
    # تم تصليح السطر رقم 200 وحل مشكلة الـ Typo نهائياً!
    with st.form("admin_add_book_form", clear_on_submit=True):
        book_title = st.text_input("اسم الكتاب / الرواية:")
        book_category = st.selectbox("تصنيف الكتاب:", ["روايات", "علم نفس", "تطوير ذات", "بيزنس", "تاريخ"])
        
        st.markdown("---")
        is_book_offer = st.checkbox("تفعيل الخصم ووضع الكتاب في قسم العروض الحصرية؟ 🔥")
        
        c1, c2 = st.columns(2)
        with c1:
            curr_price = st.number_input("سعر البيع الحالي (ج.م):", min_value=0, step=5)
        with c2:
            old_b_price = st.number_input("السعر الأصلي قبل الخصم (إذا كان عليه عرض):", min_value=0, step=5)
            
        book_img = st.file_uploader("اختر صورة غلاف الكتاب (ستُرفع مباشرة لجيت هب وتثبت):", type=["jpg", "png", "jpeg"])
        st.markdown("---")
        
        # الزرار الصحيح الخالي من الأخطاء:
        admin_submit = st.form_submit_button("إدراج الكتاب وتحديث المكتبة السحابية 🚀")
        
        if admin_submit:
            if book_title and book_img:
                with st.spinner("⚡ جاري رفع الغلاف وتأمين الرابط السحابي على جيت هب..."):
                    img_bytes = book_img.read()
                    uploaded_link = upload_image_to_github(img_bytes, book_img.name)
                    
                    if uploaded_link:
                        added_book = {
                            "title": book_title,
                            "price": curr_price,
                            "is_offer": is_book_offer,
                            "old_price": old_b_price if is_book_offer else curr_price,
                            "image": uploaded_link,
                            "category": book_category
                        }
                        
                        books.append(added_book)
                        save_books_data(books)
                        
                        st.success(f"✔️ تم رفع غلاف الكتاب وتثبيت رواية '{book_title}' بالسيستم بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ مشكلة في التوكن أو الصلاحيات أثناء رفع الصورة.")
            else:
                st.error("❌ يجب كتابة اسم الكتاب ورفع صورة غلافه أولاً!")
                
    st.markdown("### 🗑️ إدارة وحذف الكتب الحالية بالمتجر")
    if not books:
        st.info("لا توجد كتب مسجلة حالياً.")
    else:
        for i, item in enumerate(books):
            col_t, col_b = st.columns([5, 1])
            with col_t:
                st.write(f"📖 **{item['title']}** - التصنيف: `{item['category']}` - السعر الحالي: `{item['price']} ج.م`")
            with col_b:
                if st.button("حذف الكتاب 🗑️", key=f"del_b_{i}"):
                    books.pop(i)
                    save_books_data(books)
                    st.success("تم حذف الكتاب بنجاح من الرفوف!")
                    st.rerun()
