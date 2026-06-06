import streamlit as st
import requests
import json
import base64
import time
from urllib.parse import quote

# ضبط إعدادات الصفحة الرئيسية للمتجر ستايل البرندات الكبيرة
st.set_page_config(
    page_title="متجر عالم الكتب | World of Books 📚",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1️⃣ ثيم النيون المتطور المدمج بلمسات المتاجر العالمية (أمازون/نون)
def inject_neon_theme():
    neon_css = """
    <style>
    /* خلفية داكنة فخمة لإبراز الكتب والنيون */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
        font-family: 'Cairo', sans-serif;
    }
    
    /* الهيدر الرئيسي بتأثير البرق الصاعق */
    .neon-title {
        font-size: 48px;
        font-weight: 900;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff;
        animation: lightning-blink 2.5s infinite alternate;
        margin-bottom: 5px;
    }
    
    .neon-subtitle {
        text-align: center;
        color: #00f3ff;
        font-size: 16px;
        margin-bottom: 30px;
        text-shadow: 0 0 5px rgba(0, 243, 255, 0.4);
    }
    
    /* كروت الكتب الاحترافية ستايل نون وأمازون مع لمسة نيون */
    .book-card {
        border: 1px solid #1f2833;
        border-radius: 12px;
        padding: 20px;
        background-color: #1f2833;
        box-shadow: 0 4px 15px rgba(0, 243, 255, 0.03);
        margin-bottom: 25px;
        transition: 0.3s ease-in-out;
        text-align: right;
        position: relative;
    }
    .book-card:hover {
        box-shadow: 0 4px 25px rgba(0, 243, 255, 0.25);
        transform: translateY(-4px);
    }

    /* كروت قسم العروض المشتعلة من نون */
    .offer-card {
        border: 2px solid #ff0055;
        border-radius: 12px;
        padding: 20px;
        background: linear-gradient(135deg, #1f2833 0%, #2d142c 100%);
        box-shadow: 0 0 15px #ff0055, inset 0 0 8px #ff0055;
        margin-bottom: 25px;
        animation: lightning-glow 2s infinite ease-in-out;
        text-align: right;
        position: relative;
    }
    
    /* شارات أمازون ونون لتحفيز الشراء الفوري */
    .offer-badge {
        background-color: #ff0055;
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 12px;
        text-shadow: 0 0 3px #fff;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .stock-badge {
        color: #ffc107;
        font-size: 13px;
        font-weight: bold;
        display: block;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    .rating-stars {
        color: #ffc107;
        font-size: 14px;
        margin-bottom: 8px;
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
    
    @keyframes lightning-glow {
        0%, 100% { box-shadow: 0 0 12px #ff0055, inset 0 0 6px #ff0055; border-color: #ff0055; }
        50% { box-shadow: 0 0 25px #00ffcc, inset 0 0 12px #00ffcc; border-color: #00ffcc; }
    }
    </style>
    """
    st.markdown(neon_css, unsafe_allow_html=True)

# 2️⃣ دالة رفع الصور لـ GitHub (الحل الدائم والآمن واختفاء الصور)
def upload_image_to_github(file_bytes, filename):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
    except Exception:
        st.error("❌ خطأ بالـ Secrets: تأكد من تهيئة مفاتيح جيت هب في لوحة Streamlit.")
        return None

    encoded_content = base64.b64encode(file_bytes).decode("utf-8")
    clean_filename = f"book_{int(time.time())}_{filename.replace(' ', '_')}"
    path = f"images/{clean_filename}"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"رفع غلاف كتاب: {clean_filename}",
        "content": encoded_content,
        "branch": "main"
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return f"https://raw.githubusercontent.com/{repo}/main/{path}"
    return None

# 3️⃣ جلب وحفظ البيانات سحابياً عبر الـ JSON
def load_books_data():
    if "books_list" in st.session_state:
        return st.session_state["books_list"]
        
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
        
        data = {"message": "تحديث قاعدة بيانات الكتب", "content": encoded, "branch": "main"}
        if sha: data["sha"] = sha
            
        requests.put(url, headers=headers, json=data)
    except Exception:
        pass

if "book_cart" not in st.session_state:
    st.session_state.book_cart = []

inject_neon_theme()
st.markdown('<div class="neon-title">⚡ WORLD OF BOOKS ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">⚡ تجربة تسوق ذكية ومحمية مستوحاة من أكبر المنصات العالمية ⚡</div>', unsafe_allow_html=True)

# 4️⃣ إعداد نظام المنيو الجانبي للزائر (تمت إزالة صفحة الإدارة منه نهائياً لمنع الفضول)
st.sidebar.markdown("<h2 style='text-align:center; color:#00f3ff;'>🛒 أقسام المتجر</h2>", unsafe_allow_html=True)
menu = st.sidebar.selectbox(
    "انتقل إلى:",
    ["🏠 بوابة التصفح الرئيسية", "🔥 العروض اليومية الخاطفة", "🛍️ سلة مشترياتك المعلقة"]
)

# 🔐 جدار الحماية والأمان (خانة سرية منفصلة تماماً في أسفل الـ Sidebar للمسؤول فقط)
st.sidebar.markdown("---")
with st.sidebar.expander("🔒 دخول المشرف والمسؤولين"):
    admin_password = st.text_input("أدخل كلمة المرور السرية:", type="password")
    # الباسورد الافتراضي admin123
    if admin_password == "admin123":
        st.success("🔓 تم التحقق بنجاح! خيار الإدارة متاح الآن بالأسفل:")
        if st.checkbox("⚙️ فتح لوحة التحكم السحابية"):
            menu = "⚙️ لوحة تحكم الإدارة"
    elif admin_password:
        st.error("❌ كلمة مرور خاطئة! غير مصرح لك.")

books = load_books_data()

# ==================== [ 🏠 بوابة التصفح الرئيسية (أمازون/نون ستايل) ] ====================
if menu == "🏠 بوابة التصفح الرئيسية":
    # هيدر البحث والفلترة الاحترافي العلوي مثل نون وچوميا
    st.markdown("<h3 style='text-align:right; color:#00f3ff;'>🔍 ماذا تريد أن تقرأ اليوم؟</h3>", unsafe_allow_html=True)
    
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("ابحث باسم الكتاب أو الرواية الحركية...", placeholder="مثال: أرض زيكولا، العادات الذرية...")
    with col_filter:
        category_filter = st.selectbox("تصفية بالأقسام:", ["كل الأقسام", "روايات", "علم نفس", "تطوير ذات", "بيزنس", "تاريخ"])

    # تصفية وفلترة المنتجات بناء على مدخلات الزبون
    filtered_books = books
    if search_query:
        filtered_books = [b for b in filtered_books if search_query.lower() in b['title'].lower()]
    if category_filter != "كل الأقسام":
        filtered_books = [b for b in filtered_books if b.get('category') == category_filter]

    st.markdown("---")
    
    if not filtered_books:
        st.info("💡 لم نجد كتباً تطابق بحثك حالياً، جرب تصفح قسم آخر!")
    else:
        cols = st.columns(3) # عرض 3 كتب في الصف الواحد لترتيب فخم
        for idx, book in enumerate(filtered_books):
            with cols[idx % 3]:
                if book.get("is_offer"):
                    st.markdown(f"""
                    <div class="offer-card">
                        <div class="offer-badge">⚡ صفقة اليوم</div>
                        <h3>{book['title']}</h3>
                        <div class="rating-stars">⭐ 4.9 (140 تقييم)</div>
                        <p style='color:#ccc; font-size:13px;'>القسم: {book.get('category', 'عام')}</p>
                        <p style='font-size:17px;'>السعر: <del style='color:#ff0055;'>{book.get('old_price')} ج.م</del> <b style='color:#00ffcc;'>{book['price']} ج.م</b></p>
                        <span class="stock-badge">🔥 متبقي نسختين فقط في المخزن!</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="book-card">
                        <h3>{book['title']}</h3>
                        <div class="rating-stars">⭐ 4.7 (85 تقييم)</div>
                        <p style='color:#ccc; font-size:13px;'>القسم: {book.get('category', 'عام')}</p>
                        <p style='font-size:17px; color:#00f3ff;'>السعر: <b>{book['price']} ج.م</b></p>
                        <span class="stock-badge" style="color:#28a745;">✔️ متوفر وجاهز للشحن الفوري</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                if book.get("image"):
                    st.image(book["image"], use_container_width=True)
                
                if st.button(f"أضف إلى العربة 🛒", key=f"main_b_{idx}"):
                    st.session_state.book_cart.append(book)
                    st.toast(f"✔️ أضيف {book['title']} للسلة")

# ==================== [ 🔥 العروض اليومية الخاطفة ] ====================
elif menu == "🔥 العروض اليومية الخاطفة":
    st.markdown("<h2 style='text-align:right; color:#ff0055; text-shadow: 0 0 10px #ff0055;'>⚡ تخفيضات البرق الحصرية (لفترة محدودة جداً)</h2>", unsafe_allow_html=True)
    
    offer_books = [b for b in books if b.get("is_offer") == True]
    
    if not offer_books:
        st.info("كل عروض اليوم الخاطفة انتهت! انتظرونا في موجة الخصومات القادمة.")
    else:
        cols = st.columns(2)
        for idx, book in enumerate(offer_books):
            with cols[idx % 2]:
                saving = int(book.get('old_price', 0) - book.get('price', 0))
                st.markdown(f"""
                <div class="offer-card">
                    <div class="offer-badge">🔥 وفر كاش {saving} ج.م</div>
                    <h3>{book['title']}</h3>
                    <div class="rating-stars">⭐ 5.0 (أعلى تقييم بمصر)</div>
                    <p style='font-size: 18px;'>
                        السعر الأصلي: <span style='text-decoration: line-through; color: #ff0055;'>{book.get('old_price')} ج.م</span><br>
                        <span style='color: #00ffcc; font-weight: bold; font-size:23px;'>سعر التصفية: {book['price']} ج.م ⚡</span>
                    </p>
                    <span class="stock-badge">🚨 أوشك على النفاذ - طلب عالي جداً!</span>
                </div>
                """, unsafe_allow_html=True)
                
                if book.get("image"):
                    st.image(book["image"], use_container_width=True)
                
                if st.button("اقتنص العرض الحركي فورا 🛍️", key=f"off_page_{idx}"):
                    st.session_state.book_cart.append(book)
                    st.success("✔️ تم حجز نسخة العرض بنجاح!")

# ==================== [ 🛍️ سلة مشترياتك المعلقة ] ====================
elif menu == "🛍️ سلة مشترياتك المعلقة":
    st.markdown("<h2 style='text-align:right; color:#00f3ff;'>🛒 مراجعة حقيبة طلباتك</h2>", unsafe_allow_html=True)
    
    if not st.session_state.book_cart:
        st.info("عربة تسوقك فارغة حالياً. تصفح أقسام الكتب واقتنص روائعك!")
    else:
        total_price = 0
        for idx, cart_item in enumerate(st.session_state.book_cart):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"#### 📖 {cart_item['title']} - **{cart_item['price']} ج.م**")
                total_price += cart_item['price']
            with col2:
                if st.button("إلغاء الحجز ❌", key=f"rem_cart_{idx}"):
                    st.session_state.book_cart.pop(idx)
                    st.rerun()
        
        st.markdown(f"### 💰 الحساب النهائي المطلوب: `{total_price} ج.م`")
        st.markdown("---")
        
        st.subheader("📝 تفاصيل الشحن والتوصيل بالمحافظات")
        with st.form("whatsapp_secure_form"):
            user_name = st.text_input("اسم المستلم رباعي:")
            user_phone = st.text_input("رقم الموبايل الفعال (عليه واتساب):")
            user_address = st.text_area("العنوان بالتفصيل الملل:")
            
            submit_order = st.form_submit_button("إرسال الفاتورة عبر الواتساب لتأكيد الشحن 💬")
            
            if submit_order:
                if user_name and user_phone and user_address:
                    books_details = ""
                    for i, item in enumerate(st.session_state.book_cart):
                        books_details += f"- كتاب {i+1}: {item['title']} ({item['price']} ج.م)\n"
                    
                    whatsapp_msg = (
                        f"🚨 *طلب شراء جديد من متجر World of Books* 🚨\n\n"
                        f"👤 *الاسم للطلب:* {user_name}\n"
                        f"📞 *الموبايل:* {user_phone}\n"
                        f"📍 *العنوان الفعلي:* {user_address}\n\n"
                        f"📚 *قائمة المحتويات:*\n{books_details}\n"
                        f"💰 *حساب الشحن الكلي الصافي:* {total_price} ج.م\n"
                        f"⚡ _يرجى مراجعة وتأكيد خروج الشحنة للمندوب فوراً._"
                    )
                    
                    encoded_msg = quote(whatsapp_msg)
                    wa_url = f"https://wa.me/201200000000?text={encoded_msg}"
                    
                    st.markdown(f'<a href="{wa_url}" target="_blank" style="background-color:#25D366; color:white; padding:12px; border-radius:8px; text-decoration:none; font-weight:bold; display:block; text-align:center;">👉 اضغط هنا للانتقال وتأكيد الطلب بالواتساب الخاص بالمتجر</a>', unsafe_allow_html=True)
                    st.session_state.book_cart = [] 
                else:
                    st.error("❌ من فضلك سجل كافة بيانات الشحن والتواصل لتأمين خروج الشحنة!")

# ==================== [ ⚙️ لوحة تحكم الإدارة (المحمية تماماً) ] ====================
elif menu == "⚙️ لوحة تحكم الإدارة":
    st.markdown("<h2 style='text-align:right; color:#ffc107;'>🛠️ لوحة تحكم الإدارة السحابية والتحكم بمخازن الكتب</h2>", unsafe_allow_html=True)
    
    st.markdown("### ➕ إدراج كتاب أو إصدار جديد بالرفوف السحابية")
    # تم تثبيت الكود الصحيح بالكامل لمنع الـ Crash
    with st.form("admin_add_secure_form", clear_on_submit=True):
        book_title = st.text_input("عنوان الكتاب / الرواية:")
        book_category = st.selectbox("تصنيف وضعه بالمتجر:", ["روايات", "علم نفس", "تطوير ذات", "بيزنس", "تاريخ"])
        
        st.markdown("---")
        is_book_offer = st.checkbox("وضعه فوراً في قسم العروض والتخفيضات اليومية؟ 🔥")
        
        c1, c2 = st.columns(2)
        with c1:
            curr_price = st.number_input("سعر البيع المباشر (ج.م):", min_value=0, step=5)
        with c2:
            old_b_price = st.number_input("السعر القديم قبل الشطب والخصم (إن وجد):", min_value=0, step=5)
            
        book_img = st.file_uploader("ارفع صورة غلاف الكتاب (سيتم تأمين رفعها في جيت هب):", type=["jpg", "png", "jpeg"])
        st.markdown("---")
        
        # التعديل البرمجي الخالي من الأخطاء:
        admin_submit = st.form_submit_button("رفع وتحديث المتجر السحابي 🚀")
        
        if admin_submit:
            if book_title and book_img:
                with st.spinner("⚡ جاري معالجة غلاف الكتاب وتأمينه سحابياً..."):
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
                        st.success(f"✔️ تم تأمين غلاف وتفاصيل '{book_title}' بالمتجر بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ فشل معالجة صلاحيات جيت هب أثناء الرفع السحابي.")
            else:
                st.error("❌ من فضلك املأ البيانات وارفع صورة غلاف أولاً.")
                
    st.markdown("### 🗑️ جرد وتصفية الكتب الموجودة بالسيستم")
    if not books:
        st.info("الرفوف فارغة.")
    else:
        for i, item in enumerate(books):
            col_t, col_b = st.columns([5, 1])
            with col_t:
                st.write(f"📖 **{item['title']}** - القسم: `{item['category']}` - السعر المطبق: `{item['price']} ج.م`")
            with col_b:
                if st.button("حذف وتصفية 🗑️", key=f"del_secure_b_{i}"):
                    books.pop(i)
                    save_books_data(books)
                    st.success("تم الحذف بنجاح وتحديث واجهة المستخدمين.")
                    st.rerun()
