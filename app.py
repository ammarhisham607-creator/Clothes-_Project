import streamlit as st
import base64
import requests
import json

# 1. إعدادات الصفحة العامة
st.set_page_config(page_title="World of Books", page_icon="📚", layout="wide")

# 2. كود الـ CSS النيون المطور
neon_style = """
<style>
.stApp {
    background: linear-gradient(rgba(15, 15, 26, 0.96), rgba(15, 15, 26, 0.98)), 
                url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600');
    background-size: cover; background-position: center; background-attachment: fixed;
}
.main .block-container, [data-testid="stSidebarUserContent"] {
    direction: rtl !important;
    text-align: right !important;
}
@keyframes neon-glow {
    0% { text-shadow: 0 0 8px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; opacity: 1; }
    50% { text-shadow: 0 0 3px #00f3ff, 0 0 8px #00f3ff, 0 0 15px #00f3ff; opacity: 0.85; }
    100% { text-shadow: 0 0 8px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; opacity: 1; }
}
.neon-title { 
    color: #fff; text-align: center; font-size: 3.5rem; font-weight: bold; 
    margin-bottom: 10px; padding-top: 20px;
    animation: neon-glow 2.5s infinite ease-in-out;
}
.neon-subtitle { color: #ff007f; text-align: center; font-size: 1.5rem; text-shadow: 0 0 5px #ff007f; margin-bottom: 40px; }
.login-box {
    background: rgba(25, 25, 40, 0.9); border: 2px solid #00f3ff; border-radius: 15px;
    padding: 30px; box-shadow: 0 0 20px rgba(0, 243, 255, 0.2); margin-top: 50px;
}
.deposit-warning {
    background: rgba(255, 0, 127, 0.15); border: 1px solid #ff007f; border-radius: 10px;
    padding: 15px; color: #ff007f; font-weight: bold; font-size: 1.1rem;
    text-align: center; margin-bottom: 20px; text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
}
.book-card { 
    background: rgba(25, 25, 40, 0.85); border: 2px solid #ff007f; border-radius: 15px; 
    padding: 25px; text-align: center; box-shadow: 0 0 15px rgba(255, 0, 127, 0.2); 
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 520px; margin-bottom: 20px; width: 100% !important;
}
.book-img { width: 100%; height: 280px; object-fit: cover; border-radius: 10px; border: 1px solid #ff007f; margin-bottom: 15px; }
.book-title { color: #fff; font-size: 1.4rem; font-weight: bold; line-height: 1.6 !important; margin: 5px 0 !important; }
.book-author { color: #00f3ff; font-size: 1.05rem; line-height: 1.5 !important; margin-bottom: 5px !important; }
.book-rating-display { color: #f1c40f; font-size: 1.1rem; margin-bottom: 5px; font-weight: bold; }
.book-category { color: #a0a0b0; font-size: 0.9rem; margin-bottom: 15px !important; display: block; }
.book-price { color: #39ff14; font-size: 1.4rem; font-weight: bold; text-shadow: 0 0 5px #39ff14; margin-top: auto; padding-top: 10px; }
div.stButton > button { background-color: transparent !important; color: #00f3ff !important; border: 2px solid #00f3ff !important; border-radius: 8px !important; font-weight: bold !important; width: 100%; margin-top: 5px;}
div.stButton > button:hover { background-color: #00f3ff !important; color: #121212 !important; box-shadow: 0 0 25px #00f3ff !important; }
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; font-size: 16px; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# دوال جيت هاب لحفظ واسترجاع الطلبات
def load_orders_from_github():
    try:
        # التأكد من وجود البيانات في st.secrets لتجنب الأخطاء أثناء التطوير المحلي
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
            repo = st.secrets["GITHUB_REPO"]
            path = "orders.json"
            url = f"https://api.github.com/repos/{repo}/contents/{path}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_data = response.json()
                content = base64.b64decode(file_data["content"]).decode('utf-8')
                return json.loads(content)
    except Exception as e:
        pass
    return []

def save_order_to_github(new_order):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        path = "orders.json"
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        
        response = requests.get(url, headers=headers)
        current_orders = []
        sha = None
        
        if response.status_code == 200:
            file_data = response.json()
            sha = file_data["sha"]
            content = base64.b64decode(file_data["content"]).decode('utf-8')
            current_orders = json.loads(content)
            
        current_orders.append(new_order)
        updated_content = json.dumps(current_orders, ensure_ascii=False, indent=4)
        encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')
        
        payload = {"message": "📦 تسجيل أوردر جديد عبر الموقع", "content": encoded_content}
        if sha: payload["sha"] = sha
            
        put_response = requests.put(url, headers=headers, json=payload)
        return put_response.status_code in [200, 201]
    except Exception as e:
        return False

# 3. إعداد متغيرات الجلسة (Session State)
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_role" not in st.session_state: st.session_state.user_role = "user"
if "user_info" not in st.session_state: st.session_state.user_info = {"name": "", "whatsapp": ""}
if "categories" not in st.session_state: st.session_state.categories = ["روايات فانتازيا", "رعب وغموض", "أدب وروايات عالمية", "تنمية ذاتية وفكر"]
if "books" not in st.session_state:
    st.session_state.books = [
        {"id": "b1", "title": "رواية الفيل الأزرق", "author": "أحمد مراد", "price": 150, "category": "رعب وغموض", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.8},
        {"id": "b2", "title": "رواية أرض زيكولا", "author": "عمرو عبد الحميد", "price": 130, "category": "روايات فانتازيا", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    ]
if "cart" not in st.session_state: st.session_state.cart = []
if "comments" not in st.session_state: st.session_state.comments = {}

# تحميل الأوردرات من جيت هاب عند أول تشغيل لضمان عدم اختفائها مع الريفريش
if "orders" not in st.session_state: 
    st.session_state.orders = load_orders_from_github()


# ==================== [ شاشة تسجيل الدخول الإلزامية والمخفية للأدمن ] ====================
if not st.session_state.logged_in:
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">مرحباً بك! برجاء تسجيل الدخول أولاً لتصفح المتجر وحجز الكتب</div>', unsafe_allow_html=True)
    
    col_login, _ = st.columns([2, 1])
    with col_login:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # حقل إدخال الاسم (وهو نفس الحقل السري للأدمن)
        reg_name = st.text_input("👤 اسمك بالكامل:")
        
        # الخدعة السرية: لو كتبت admin_login هيفتحلك باسورد الأدمن
        if reg_name.strip() == "admin_login":
            st.info("🔐 تم اكتشاف محاولة دخول للإدارة.")
            admin_pass = st.text_input("🔑 كلمة مرور الأدمن السري:", type="password")
            if st.button("دخول الإدارة 🔐"):
                if admin_pass == "admin123":
                    st.session_state.user_role = "admin"
                    st.session_state.logged_in = True
                    st.success("تم تفعيل صلاحيات الأدمن الرئيسي بنجاح!")
                    st.rerun()
                else:
                    st.error("كلمة المرور خاطئة!")
        else:
            # لو اسم عادي، يكمل تسجيل دخول للمستخدم الطبيعي
            reg_phone = st.text_input("📞 رقم الواتساب الخاص بك (مهم للمتابعة):")
            if st.button("دخول المتجر 🛒"):
                if reg_name.strip() and reg_phone.strip():
                    st.session_state.user_info["name"] = reg_name
                    st.session_state.user_info["whatsapp"] = reg_phone
                    st.session_state.user_role = "user"
                    st.session_state.logged_in = True
                    st.success(f"مرحباً بك يا {reg_name}! تم الحفظ وجاري تحويلك للمتجر...")
                    st.rerun()
                else:
                    st.error("من فضلك اكتب الاسم ورقم الواتساب بشكل صحيح!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ==================== [ بعد تسجيل الدخول بنجاح ] ====================
st.sidebar.markdown(f"### 👋 مرحباً، {st.session_state.user_info['name'] if st.session_state.user_role == 'user' else 'المدير المسؤول'}")

page_options = ["🔐 لوحة الإدارة", "🛒 المتجر الإلكتروني"] if st.session_state.user_role == "admin" else ["🛒 المتجر الإلكتروني"]
menu = st.sidebar.selectbox("🧭 انتقل إلى:", page_options)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.session_state.user_info = {"name": "", "whatsapp": ""}
    st.session_state.cart = []
    st.rerun()

# ==================== صفحة المتجر ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">عالمك الخاص لأجمل الكتب والروايات الحقيقية والنيون</div>', unsafe_allow_html=True)

    search_query = st.text_input("🔍 ابحث عن اسم رواية أو مؤلف:")
    
    filtered_books = [b for b in st.session_state.books if search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()]

    cols = st.columns(3)
    for index, book in enumerate(filtered_books):
        with cols[index % 3]:
            st.markdown(f"""
            <div class="book-card">
                <div>
                    <img src="{book['image']}" class="book-img">
                    <div class="book-title">{book['title']}</div>
                    <div class="book-author">تأليف: {book['author']}</div>
                    <div class="book-price">{book['price']} جنيه</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"أضف للسلة 🛒", key=f"add_{book['id']}"):
                st.session_state.cart.append(book)
                st.toast(f"تم إضافة {book['title']} للسلة!")

    st.markdown("---")
    st.markdown('<div class="neon-subtitle" style="text-align: right;">🛒 سلة المشتريات الخاصة بك</div>', unsafe_allow_html=True)
    
    if len(st.session_state.cart) != 0:
        total_price = sum(item['price'] for item in st.session_state.cart)
        book_names = [item['title'] for item in st.session_state.cart]
        st.success(f"لديك **{len(st.session_state.cart)}** كتب في السلة | الإجمالي: **{total_price} جنيه**")
        
        st.markdown('<div class="deposit-warning">⚠️ تنبيه هام: لإتمام شحن الكتب المحجوزة، يجب دفع (عربون) عبر الواتساب لتأكيد الحجز!</div>', unsafe_allow_html=True)
        
        with st.form("checkout_form"):
            address = st.text_input("🏠 عنوان الشحن بالتفصيل")
            submit_order = st.form_submit_button("تأكيد الطلب وحجز الكتب 🚚")
            
            if submit_order and address.strip():
                order_data = {
                    "books": book_names, "total_price": total_price,
                    "name": st.session_state.user_info["name"], "phone": st.session_state.user_info["whatsapp"],
                    "address": address
                }
                # حفظ الأوردر في GitHub وفي الـ Session State معاً
                save_order_to_github(order_data)
                st.session_state.orders.append(order_data)
                st.session_state.cart = [] 
                st.success("🎉 تم تسجيل طلبك بنجاح! تواصل معنا عبر الواتساب لإرسال العربون وتأكيد الشحن!")
                st.rerun()

# ==================== صفحة الإدارة ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة تحكم المدير المسؤول")
    
    tab1, tab2 = st.tabs(["📦 الأوردرات الواردة (محفوظة دائماً)", "➕ إضافة كتاب جديد"])
    
    with tab1:
        # هنا الأوردرات هتفضل موجودة حتى لو عملت ريفريش لأنها بتتسحب من GitHub
        if len(st.session_state.orders) == 0:
            st.info("لا توجد طلبات جديدة حالياً.")
        else:
            for i, order in enumerate(st.session_state.orders):
                with st.expander(f"الأوردر رقم {i+1} - من العميل: {order['name']}"):
                    st.write(f"**🟢 واتساب العميل:** {order['phone']}")
                    st.write(f"**🏠 العنوان:** {order['address']}")
                    st.write(f"**📚 الكتب المحجوزة:** {', '.join(order['books'])}")
                    st.write(f"**💰 الحساب الكلي:** {order['total_price']} جنيه")

    with tab2:
        with st.form("add_book", clear_on_submit=True):
            t = st.text_input("اسم الكتاب")
            a = st.text_input("اسم المؤلف")
            p = st.number_input("السعر", min_value=1, step=5)
            img = st.file_uploader("صورة الغلاف", type=["png", "jpg", "jpeg"])
            if st.form_submit_button("إضافة") and t and img:
                base64_img = base64.b64encode(img.getvalue()).decode()
                src = f"data:image/{img.type.split('/')[-1]};base64,{base64_img}"
                st.session_state.books.append({"id": f"b{len(st.session_state.books)+1}", "title": t, "author": a, "price": p, "category": "عام", "image": src, "rating": 5.0})
                st.success("تم الإضافة!")
                st.rerun()

# زر الواتساب العائم
whatsapp_url = "https://wa.me/201149243249?text=أهلاً%20World%20of%20Books%20لقد%20قمت%20بعمل%20حجز%20وأريد%20تأكيد%20دفع%20العربون"
st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">💬 تواصل وتأكيد دفع العربون</a>', unsafe_allow_html=True)
