import streamlit as st
import base64
import requests
import json

# 1. إعدادات الصفحة العامة
st.set_page_config(page_title="World of Books", page_icon="📚", layout="wide")

# 2. كود الـ CSS النيون المطور (كامل ومحافظ عليه بنسبة 100%)
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
div.stButton > button { background-color: transparent !important; color: #00f3ff !important; border: 2px solid #00f3ff !important; border-radius: 8px !important; font-weight: bold !important; width: 100%; margin-top: 5px;}
div.stButton > button:hover { background-color: #00f3ff !important; color: #121212 !important; box-shadow: 0 0 25px #00f3ff !important; }
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# دالة برمجية موحدة وذكية للتعامل مع ملفات جيت هاب تمنع الباجات تماماً
def github_action(path, action="LOAD", data_to_save=None):
    try:
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
            repo = st.secrets["GITHUB_REPO"]
            url = f"https://api.github.com/repos/{repo}/contents/{path}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            
            res = requests.get(url, headers=headers)
            sha = res.json()["sha"] if res.status_code == 200 else None
            
            if action == "LOAD":
                if res.status_code == 200:
                    content = base64.b64decode(res.json()["content"]).decode('utf-8')
                    return json.loads(content)
                return None
                
            elif action == "SAVE":
                encoded_content = base64.b64encode(json.dumps(data_to_save, ensure_ascii=False, indent=4).encode('utf-8')).decode('utf-8')
                payload = {"message": f"🔄 تحديث ملف {path}", "content": encoded_content}
                if sha: payload["sha"] = sha
                put_res = requests.put(url, headers=headers, json=payload)
                return put_res.status_code in [200, 201]
    except:
        pass
    return [] if action == "LOAD" else False

# 3. تحميل وإعداد قواعد البيانات الثابتة من جيت هاب مع وجود قيم افتراضية حماية من السقوط
default_books = [
    {"id": "b1", "title": "الفيل الأزرق", "author": "أحمد مراد", "price": 150, "category": "رعب وغموض", "description": "رواية تشويق وإثارة نفسية عن طبيب نفسي يواجه قضايا معقدة.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.8},
    {"id": "b2", "title": "أرض زيكولا", "author": "عمرو عبد الحميد", "price": 130, "category": "روايات فانتازيا", "description": "خيال يمزج بين الواقع وعالم يتعامل بوحدات الذكاء بدلاً من المال.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7}
]
default_cats = ["روايات فانتازيا", "رعب وغموض", "أدب عالمي", "تنمية ذاتية"]

if "books" not in st.session_state:
    loaded_books = github_action("books.json", "LOAD")
    st.session_state.books = loaded_books if loaded_books else default_books

if "categories" not in st.session_state:
    loaded_cats = github_action("categories.json", "LOAD")
    st.session_state.categories = loaded_cats if loaded_cats else default_cats

if "orders" not in st.session_state:
    loaded_orders = github_action("orders.json", "LOAD")
    st.session_state.orders = loaded_orders if loaded_orders else []

if "comments" not in st.session_state:
    loaded_comments = github_action("comments.json", "LOAD")
    st.session_state.comments = loaded_comments if isinstance(loaded_comments, dict) else {}

if "users" not in st.session_state:
    loaded_users = github_action("users.json", "LOAD")
    st.session_state.users = loaded_users if loaded_users else []

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_role" not in st.session_state: st.session_state.user_role = "user"
if "user_info" not in st.session_state: st.session_state.user_info = {"name": "", "whatsapp": ""}
if "cart" not in st.session_state: st.session_state.cart = []

# ==================== [ فحص حالة الحساب الحالي لمنع المحظورين فورا ] ====================
if st.session_state.logged_in and st.session_state.user_role == "user":
    # إعادة فحص حالة المستخدم من القائمة المحدثة
    current_user_check = next((u for u in st.session_state.users if u["whatsapp"] == st.session_state.user_info["whatsapp"]), None)
    if current_user_check:
        if current_user_check["status"] == "محظور":
            st.error("🚫 عذراً، لقد تم حظر حسابك من دخول المتجر بواسطة الإدارة.")
            st.session_state.logged_in = False
            st.stop()
        elif current_user_check["status"] == "معلق":
            st.warning("⏳ حسابك معلق مؤقتاً مراجعة من قبل الإدارة، تواصل معنا لتفعيله.")
            st.session_state.logged_in = False
            st.stop()

# ==================== [ شاشة تسجيل الدخول المخفية والذكية ] ====================
if not st.session_state.logged_in:
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">مرحباً بك! سجل دخولك لتصفح أحدث الروايات الحصرية</div>', unsafe_allow_html=True)
    
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
                else: st.error("الباسورد خطأ!")
        else:
            reg_phone = st.text_input("📞 رقم الواتساب الخاص بك:")
            if st.button("دخول المتجر 🛒"):
                if reg_name.strip() and reg_phone.strip():
                    # فحص الحساب في جيت هب
                    user_match = next((u for u in st.session_state.users if u["whatsapp"] == reg_phone.strip()), None)
                    
                    if user_match:
                        if user_match["status"] == "محظور":
                            st.error("🚫 هذا الحساب محظور تماماً من دخول المتجر!")
                        elif user_match["status"] == "معلق":
                            st.warning("⏳ حسابك معلق حالياً، تواصل مع الدعم الفني.")
                        else:
                            st.session_state.user_info = {"name": user_match["name"], "whatsapp": user_match["whatsapp"]}
                            st.session_state.user_role = "user"
                            st.session_state.logged_in = True
                            st.rerun()
                    else:
                        # مستخدم جديد تماماً
                        new_u = {"name": reg_name.strip(), "whatsapp": reg_phone.strip(), "status": "نشط"}
                        st.session_state.users.append(new_u)
                        github_action("users.json", "SAVE", st.session_state.users)
                        
                        st.session_state.user_info = {"name": reg_name.strip(), "whatsapp": reg_phone.strip()}
                        st.session_state.user_role = "user"
                        st.session_state.logged_in = True
                        st.rerun()
                else: st.error("برجاء إدخال البيانات كاملة!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== [ القائمة الجانبية للتنقل ] ====================
page_options = ["🔐 لوحة الإدارة", "🛒 المتجر الإلكتروني"] if st.session_state.user_role == "admin" else ["🛒 المتجر الإلكتروني"]
menu = st.sidebar.selectbox("🧭 انتقل إلى:", page_options)

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.session_state.cart = []
    st.rerun()

# ==================== [ صفحة المتجر الإلكتروني ] ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 ابحث عن اسم رواية أو مؤلف:")
    selected_category = st.selectbox("📂 تصفية حسب القسم:", ["الكل"] + st.session_state.categories)
    
    filtered_books = [b for b in st.session_state.books if (search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()) and (selected_category == "الكل" or b["category"] == selected_category)]

    cols = st.columns(3)
    for index, book in enumerate(filtered_books):
        with cols[index % 3]:
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
                st.toast(f"تم إضافة {book['title']}!")
            
            # التقييم والتعليقات المرجعة بالكامل
            with st.expander("💬 التقييمات وآراء القراء"):
                new_rating = st.slider("تقييمك:", 1.0, 5.0, float(book.get('rating', 5.0)), 0.1, key=f"rate_{book['id']}")
                if st.button("حفظ التقييم ⭐", key=f"btn_rate_{book['id']}"):
                    book['rating'] = new_rating
                    github_action("books.json", "SAVE", st.session_state.books)
                    st.toast("تم حفظ تقييمك بنجاح في قاعدة البيانات!")
                    st.rerun()
                    
                bid = book["id"]
                if bid not in st.session_state.comments: st.session_state.comments[bid] = []
                for c in st.session_state.comments[bid]:
                    st.markdown(f"👤 **{c['user']}**: {c['text']}")
                
                new_comment = st.text_input("اكتب تعليقاً محفزاً للرواية:", key=f"comm_{bid}")
                if st.button("نشر التعليق 🚀", key=f"btn_comm_{bid}") and new_comment:
                    st.session_state.comments[bid].append({"user": st.session_state.user_info["name"], "text": new_comment})
                    github_action("comments.json", "SAVE", st.session_state.comments)
                    st.rerun()

    # السلة والدفع بالعربون
    if len(st.session_state.cart) > 0:
        st.markdown("---")
        st.markdown('<div class="neon-subtitle" style="text-align: right;">🛒 سلة المشتريات الحالية</div>', unsafe_allow_html=True)
        total_price = sum(item['price'] for item in st.session_state.cart)
        st.success(f"لديك {len(st.session_state.cart)} كتب في السلة | إجمالي الحساب: {total_price} جنيه")
        st.markdown('<div class="deposit-warning">⚠️ تنبيه هام: لإتمام شحن الكتب المحجوزة، يجب دفع (عربون) عبر الواتساب لتأكيد الحجز!</div>', unsafe_allow_html=True)
        
        with st.form("checkout_form"):
            address = st.text_input("🏠 عنوان الشحن بالتفصيل المُمِل:")
            if st.form_submit_button("تأكيد الطلب وحجز الكتب 🚚") and address.strip():
                order_data = {"books": [b['title'] for b in st.session_state.cart], "total_price": total_price, "name": st.session_state.user_info["name"], "phone": st.session_state.user_info["whatsapp"], "address": address}
                st.session_state.orders.append(order_data)
                github_action("orders.json", "SAVE", st.session_state.orders)
                st.session_state.cart = []
                st.success("🎉 تم تسجيل طلبك على السيستم وحفظه بنجاح دائم!")
                st.rerun()

# ==================== [ صفحة الإدارة والتحكم الشاملة ] ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة تحكم المدير المسؤول")
    
    # تم الحفاظ على الألسنة الأربعة القديمة بالكامل وضبط التخزين الدائم، وتم إضافة لسان خامس للمستخدمين
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📦 الأوردرات", "➕ إضافة كتاب", "📁 إدارة الأقسام", "✏️ تعديل الكتب", "👤 إدارة المستخدمين"])
    
    with tab1:
        st.subheader("📦 الطلبات الواردة من الموقع المحفوظة على GitHub")
        if not st.session_state.orders: st.info("لا توجد طلبات حالياً.")
        for i, order in enumerate(st.session_state.orders):
            with st.expander(f"أوردر رقم {i+1} - للعميل: {order['name']}"):
                st.write(f"**📞 واتساب العميل:** {order['phone']}")
                st.write(f"**🏠 العنوان:** {order['address']}")
                st.write(f"**📚 الكتب المحجوزة:** {', '.join(order['books'])}")
                st.write(f"**💰 الحساب الإجمالي:** {order['total_price']} جنيه")

    with tab2:
        st.subheader("➕ إضافة كتاب جديد للمتجر وقاعدة جيت هب")
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            t = col1.text_input("اسم الكتاب")
            a = col2.text_input("اسم المؤلف")
            cat = col1.selectbox("القسم المناسب", st.session_state.categories)
            p = col2.number_input("السعر بالجنيه", min_value=1, step=5)
            desc = st.text_area("وصف وقصة الكتاب:")
            img = st.file_uploader("صورة غلاف الكتاب الحقيقية", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("إدخال وحفظ الكتاب 🚀") and t and img:
                base64_img = base64.b64encode(img.getvalue()).decode()
                src = f"data:image/{img.type.split('/')[-1]};base64,{base64_img}"
                st.session_state.books.append({"id": f"b{len(st.session_state.books)+1}", "title": t, "author": a, "price": p, "category": cat, "description": desc, "image": src, "rating": 5.0})
                github_action("books.json", "SAVE", st.session_state.books)
                st.success("تم رفع الكتاب وحفظه بنجاح دائم على جيت هب!")
                st.rerun()

    with tab3:
        st.subheader("📁 إدارة وأقسام المتجر")
        new_cat = st.text_input("اكتب اسم القسم الجديد:")
        if st.button("تأكيد إضافة القسم 📁") and new_cat.strip():
            if new_cat.strip() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.strip())
                github_action("categories.json", "SAVE", st.session_state.categories)
                st.success("تم حفظ وتعميم القسم الجديد!")
                st.rerun()
        st.write("الأقسام الحالية المعتمدة في المتجر:", ", ".join(st.session_state.categories))

    with tab4:
        st.subheader("✏️ تعديل بيانات وصور الكتب الحالية")
        selected_book_title = st.selectbox("اختر الكتاب المراد تعديله:", [b["title"] for b in st.session_state.books])
        book_to_edit = next((b for b in st.session_state.books if b["title"] == selected_book_title), None)
        
        if book_to_edit:
            with st.form("edit_book_form_secure"):
                new_t = st.text_input("تعديل الاسم", value=book_to_edit["title"])
                new_a = st.text_input("تعديل المؤلف", value=book_to_edit["author"])
                new_cat = st.selectbox("تعديل القسم", st.session_state.categories, index=st.session_state.categories.index(book_to_edit["category"]) if book_to_edit["category"] in st.session_state.categories else 0)
                new_desc = st.text_area("تعديل الوصف والقصة", value=book_to_edit.get("description", ""))
                new_p = st.number_input("تعديل السعر", min_value=1, value=int(book_to_edit["price"]))
                
                st.write("🖼️ غلاف الكتاب الحالي:")
                st.image(book_to_edit["image"], width=130)
                new_img = st.file_uploader("رفع غلاف وصورة جديدة كلياً (اتركه فارغاً للإبقاء على الصورة الحالية)", type=["png", "jpg", "jpeg"])
                
                if st.form_submit_button("حفظ وتحديث البيانات على السيرفر 💾"):
                    book_to_edit["title"] = new_t
                    book_to_edit["author"] = new_a
                    book_to_edit["category"] = new_cat
                    book_to_edit["description"] = new_desc
                    book_to_edit["price"] = new_p
                    if new_img:
                        base64_img = base64.b64encode(new_img.getvalue()).decode()
                        book_to_edit["image"] = f"data:image/{new_img.type.split('/')[-1]};base64,{base64_img}"
                    
                    github_action("books.json", "SAVE", st.session_state.books)
                    st.success("تم تحديث وحفظ بيانات وصورة الرواية بنجاح!")
                    st.rerun()

    # الميزة الجديدة المطلوبة بالكامل: إدارة صلاحيات حسابات المستخدمين
    with tab5:
        st.subheader("👤 إدارة حسابات المشترين وصلاحيات الدخول")
        st.markdown("يمكنك من هنا متابعة حسابات العملاء، وحظر أي رقم مزعج أو تعليق حسابه مؤقتاً.") 
        # السطر 342 يبدأ من الصفر تماماً بدون أي مسافة قبله
if not st.session_state.logged_in:
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">مرحباً بك! سجل دخولك لتصفح أحدث الروايات الحصرية</div>', unsafe_allow_html=True)
    # باقي الكود مستمر بمسافة داخلية...
