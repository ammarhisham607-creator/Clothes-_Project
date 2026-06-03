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
.book-card { 
    background: rgba(25, 25, 40, 0.85); border: 2px solid #ff007f; border-radius: 15px; 
    padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(255, 0, 127, 0.2); 
    display: flex; flex-direction: column; justify-content: space-between;
    height: 100%; margin-bottom: 20px;
}
.book-img { width: 100%; height: 280px; object-fit: cover; border-radius: 10px; border: 1px solid #ff007f; margin-bottom: 15px; }
.book-title { color: #fff; font-size: 1.4rem; font-weight: bold; margin: 5px 0; }
.book-author { color: #00f3ff; font-size: 1.05rem; margin-bottom: 5px; }
.book-category { color: #ff007f; font-size: 0.9rem; font-weight: bold; margin-bottom: 5px; border: 1px solid #ff007f; display: inline-block; padding: 2px 8px; border-radius: 10px;}
.book-desc { color: #a0a0b0; font-size: 0.9rem; margin-bottom: 10px; line-height: 1.4; }
.book-price { color: #39ff14; font-size: 1.4rem; font-weight: bold; text-shadow: 0 0 5px #39ff14; margin-top: 10px; }
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# دوال جيت هاب (مبسطة لتعمل بشكل صحيح في الكود)
def load_orders_from_github():
    try:
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
            repo = st.secrets["GITHUB_REPO"]
            url = f"https://api.github.com/repos/{repo}/contents/orders.json"
            headers = {"Authorization": f"token {token}"}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                content = base64.b64decode(res.json()["content"]).decode('utf-8')
                return json.loads(content)
    except: pass
    return []

def save_order_to_github(new_order):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        url = f"https://api.github.com/repos/{repo}/contents/orders.json"
        headers = {"Authorization": f"token {token}"}
        res = requests.get(url, headers=headers)
        
        current_orders = []
        sha = None
        if res.status_code == 200:
            file_data = res.json()
            sha = file_data["sha"]
            current_orders = json.loads(base64.b64decode(file_data["content"]).decode('utf-8'))
            
        current_orders.append(new_order)
        encoded_content = base64.b64encode(json.dumps(current_orders, ensure_ascii=False, indent=4).encode('utf-8')).decode('utf-8')
        
        payload = {"message": "تسجيل أوردر جديد", "content": encoded_content}
        if sha: payload["sha"] = sha
        requests.put(url, headers=headers, json=payload)
    except: pass

# 3. إعداد متغيرات الجلسة
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_role" not in st.session_state: st.session_state.user_role = "user"
if "user_info" not in st.session_state: st.session_state.user_info = {"name": "", "whatsapp": ""}
if "categories" not in st.session_state: st.session_state.categories = ["روايات فانتازيا", "رعب وغموض", "أدب عالمي", "تنمية ذاتية"]
if "books" not in st.session_state:
    st.session_state.books = [
        {"id": "b1", "title": "الفيل الأزرق", "author": "أحمد مراد", "price": 150, "category": "رعب وغموض", "description": "رواية تشويق وإثارة نفسية عن طبيب نفسي يواجه قضايا معقدة.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.8},
        {"id": "b2", "title": "أرض زيكولا", "author": "عمرو عبد الحميد", "price": 130, "category": "روايات فانتازيا", "description": "خيال يمزج بين الواقع وعالم يتعامل بوحدات الذكاء بدلاً من المال.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    ]
if "cart" not in st.session_state: st.session_state.cart = []
if "comments" not in st.session_state: st.session_state.comments = {}
if "orders" not in st.session_state: st.session_state.orders = load_orders_from_github()

# ==================== شاشة تسجيل الدخول المخفية ====================
if not st.session_state.logged_in:
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    col_login, _ = st.columns([2, 1])
    with col_login:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        reg_name = st.text_input("👤 اسمك بالكامل:")
        
        if reg_name.strip() == "admin_login":
            admin_pass = st.text_input("🔑 كلمة مرور الأدمن السري:", type="password")
            if st.button("دخول الإدارة 🔐"):
                if admin_pass == "admin123":
                    st.session_state.user_role = "admin"
                    st.session_state.logged_in = True
                    st.rerun()
        else:
            reg_phone = st.text_input("📞 رقم الواتساب الخاص بك:")
            if st.button("دخول المتجر 🛒"):
                if reg_name and reg_phone:
                    st.session_state.user_info.update({"name": reg_name, "whatsapp": reg_phone})
                    st.session_state.logged_in = True
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== القائمة الجانبية ====================
page_options = ["🔐 لوحة الإدارة", "🛒 المتجر الإلكتروني"] if st.session_state.user_role == "admin" else ["🛒 المتجر الإلكتروني"]
menu = st.sidebar.selectbox("🧭 انتقل إلى:", page_options)

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.rerun()

# ==================== صفحة المتجر ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 ابحث عن اسم رواية أو مؤلف:")
    selected_category = st.selectbox("📂 تصفية حسب القسم:", ["الكل"] + st.session_state.categories)
    
    filtered_books = [b for b in st.session_state.books if (search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()) and (selected_category == "الكل" or b["category"] == selected_category)]

    cols = st.columns(3)
    for index, book in enumerate(filtered_books):
        with cols[index % 3]:
            # عرض بيانات الكتاب بالتفصيل (صورة، اسم، مؤلف، قسم، وصف، تقييم، سعر)
            st.markdown(f"""
            <div class="book-card">
                <img src="{book['image']}" class="book-img">
                <div class="book-title">{book['title']}</div>
                <div class="book-author">تأليف: {book['author']}</div>
                <div><span class="book-category">{book['category']}</span></div>
                <div class="book-desc">{book.get('description', 'لا يوجد وصف متاح')}</div>
                <div style="color: gold; font-size: 1.1rem; margin-bottom: 5px;">⭐ {book.get('rating', 5.0)}/5.0</div>
                <div class="book-price">{book['price']} جنيه</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("أضف للسلة 🛒", key=f"add_{book['id']}"):
                st.session_state.cart.append(book)
                st.toast("تم الإضافة للسلة!")
            
            # التقييم والتعليقات
            with st.expander("💬 التقييمات والتعليقات"):
                new_rating = st.slider("تقييمك للكتاب:", 1.0, 5.0, float(book.get('rating', 5.0)), 0.1, key=f"rate_{book['id']}")
                if st.button("حفظ التقييم", key=f"btn_rate_{book['id']}"):
                    book['rating'] = new_rating
                    st.toast("تم حفظ تقييمك!")
                    
                if book["id"] not in st.session_state.comments:
                    st.session_state.comments[book["id"]] = []
                for c in st.session_state.comments[book["id"]]:
                    st.markdown(f"**{c['user']}**: {c['text']}")
                
                new_comment = st.text_input("أضف تعليقك:", key=f"comm_{book['id']}")
                if st.button("نشر التعليق", key=f"btn_comm_{book['id']}") and new_comment:
                    st.session_state.comments[book["id"]].append({"user": st.session_state.user_info["name"], "text": new_comment})
                    st.rerun()

    # السلة
    if len(st.session_state.cart) > 0:
        st.markdown("---")
        total_price = sum(item['price'] for item in st.session_state.cart)
        st.success(f"🛒 لديك {len(st.session_state.cart)} كتب | الإجمالي: {total_price} جنيه")
        with st.form("checkout"):
            address = st.text_input("🏠 عنوان الشحن بالتفصيل")
            if st.form_submit_button("تأكيد الطلب 🚚") and address:
                order_data = {"books": [b['title'] for b in st.session_state.cart], "total_price": total_price, "name": st.session_state.user_info["name"], "phone": st.session_state.user_info["whatsapp"], "address": address}
                save_order_to_github(order_data)
                st.session_state.orders.append(order_data)
                st.session_state.cart = []
                st.success("تم تأكيد الطلب!")
                st.rerun()

# ==================== صفحة الإدارة ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة التحكم الشاملة")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📦 الأوردرات", "➕ إضافة كتاب", "📁 إدارة الأقسام", "✏️ تعديل الكتب"])
    
    with tab1:
        if not st.session_state.orders: st.info("لا توجد طلبات.")
        for i, order in enumerate(st.session_state.orders):
            with st.expander(f"أوردر {i+1} - {order['name']}"):
                st.write(f"📞 واتساب: {order['phone']} | 🏠 العنوان: {order['address']}")
                st.write(f"📚 الكتب: {', '.join(order['books'])} | 💰 السعر: {order['total_price']} ج")

    with tab2:
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            t = col1.text_input("اسم الكتاب")
            a = col2.text_input("اسم المؤلف")
            cat = col1.selectbox("القسم", st.session_state.categories)
            p = col2.number_input("السعر", min_value=1)
            desc = st.text_area("وصف الكتاب")
            img = st.file_uploader("صورة الغلاف", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("إضافة الكتاب") and t and img:
                base64_img = base64.b64encode(img.getvalue()).decode()
                src = f"data:image/{img.type.split('/')[-1]};base64,{base64_img}"
                st.session_state.books.append({"id": f"b{len(st.session_state.books)+1}", "title": t, "author": a, "price": p, "category": cat, "description": desc, "image": src, "rating": 5.0})
                st.success("تم الإضافة!")
                st.rerun()

    with tab3:
        st.subheader("إضافة أو تعديل الأقسام")
        new_cat = st.text_input("اسم القسم الجديد:")
        if st.button("إضافة القسم") and new_cat:
            if new_cat not in st.session_state.categories:
                st.session_state.categories.append(new_cat)
                st.success("تم إضافة القسم!")
                st.rerun()
        st.write("الأقسام الحالية:", ", ".join(st.session_state.categories))

    with tab4:
        st.subheader("تعديل بيانات وصورة الكتاب")
        selected_book_title = st.selectbox("اختر الكتاب لتعديله", [b["title"] for b in st.session_state.books])
        
        # البحث عن الكتاب المختار
        book_to_edit = next((b for b in st.session_state.books if b["title"] == selected_book_title), None)
        
        if book_to_edit:
            with st.form("edit_book_form"):
                new_t = st.text_input("الاسم", value=book_to_edit["title"])
                new_a = st.text_input("المؤلف", value=book_to_edit["author"])
                new_cat = st.selectbox("القسم", st.session_state.categories, index=st.session_state.categories.index(book_to_edit["category"]) if book_to_edit["category"] in st.session_state.categories else 0)
                new_desc = st.text_area("الوصف", value=book_to_edit.get("description", ""))
                new_p = st.number_input("السعر", min_value=1, value=int(book_to_edit["price"]))
                
                st.write("صورة الغلاف الحالية:")
                st.image(book_to_edit["image"], width=150)
                new_img = st.file_uploader("رفع صورة جديدة (اتركه فارغاً للاحتفاظ بالصورة الحالية)", type=["png", "jpg", "jpeg"])
                
                if st.form_submit_button("حفظ التعديلات"):
                    book_to_edit["title"] = new_t
                    book_to_edit["author"] = new_a
                    book_to_edit["category"] = new_cat
                    book_to_edit["description"] = new_desc
                    book_to_edit["price"] = new_p
                    
                    if new_img:  # لو تم رفع صورة جديدة
                        base64_img = base64.b64encode(new_img.getvalue()).decode()
                        book_to_edit["image"] = f"data:image/{new_img.type.split('/')[-1]};base64,{base64_img}"
                    
                    st.success("تم تحديث بيانات الكتاب بنجاح!")
                    st.rerun()

# زر الواتساب العائم
whatsapp_url = "https://wa.me/201149243249?text=أهلاً"
st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">💬 تواصل معنا</a>', unsafe_allow_html=True)
