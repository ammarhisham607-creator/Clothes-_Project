import streamlit as st
import base64
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="World of Books", page_icon="📚", layout="wide")

# 2. كود الديكور والـ CSS المطور لمنع انكماش وتداخل الكلام
neon_style = """
<style>
/* خلفية الموقع العامة */
.stApp {
    background: linear-gradient(rgba(15, 15, 26, 0.95), rgba(15, 15, 26, 0.98)), 
                url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600');
    background-size: cover; background-position: center; background-attachment: fixed;
}

/* 🛠️ الحل الجذري لمشكلة الكلام المفرود بالطول: توجيه المحتوى بأمان دون كسر أعمدة Streamlit */
.main .block-container, [data-testid="stSidebarUserContent"] {
    direction: rtl !important;
    text-align: right !important;
}

/* ضبط عناصر المدخلات والقوائم لتأخذ العرض بالكامل وتمنع الانكماش */
.stTextInput width, .stSelectbox width, .stNumberInput width {
    width: 100% !important;
}

/* 🌟 تأثير نيون نابض (ينور ويطفي) للعنوان الرئيسي 🌟 */
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

/* كروت الكتب وضمان ثبات أبعادها */
.book-card { 
    background: rgba(25, 25, 40, 0.85); border: 2px solid #ff007f; border-radius: 15px; 
    padding: 25px; text-align: center; box-shadow: 0 0 15px rgba(255, 0, 127, 0.2); 
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 500px; margin-bottom: 30px;
    width: 100% !important;
}
.book-img { width: 100%; height: 260px; object-fit: cover; border-radius: 10px; border: 1px solid #ff007f; margin-bottom: 15px; }

/* تباعد مريح للاسطر العربية */
.book-title { color: #fff; font-size: 1.4rem; font-weight: bold; line-height: 1.6 !important; margin: 10px 0 !important; }
.book-author { color: #00f3ff; font-size: 1.05rem; line-height: 1.5 !important; margin-bottom: 8px !important; }
.book-category { color: #f1c40f; font-size: 0.9rem; margin-bottom: 15px !important; display: block; }
.book-price { color: #39ff14; font-size: 1.4rem; font-weight: bold; text-shadow: 0 0 5px #39ff14; margin-top: auto; padding-top: 10px; }

/* أزرار المتجر */
div.stButton > button { background-color: transparent !important; color: #00f3ff !important; border: 2px solid #00f3ff !important; border-radius: 8px !important; font-weight: bold !important; width: 100%; margin-top: 10px;}
div.stButton > button:hover { background-color: #00f3ff !important; color: #121212 !important; box-shadow: 0 0 25px #00f3ff !important; }

/* زرار واتساب */
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; font-size: 16px; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# 3. دالة جيت هاب لرفع وحفظ الأوردرات
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
        if sha:
            payload["sha"] = sha
            
        put_response = requests.put(url, headers=headers, json=payload)
        return put_response.status_code in [200, 201]
    except Exception as e:
        return False

# 4. إعداد هياكل البيانات في الذاكرة
if "categories" not in st.session_state:
    st.session_state.categories = ["روايات مترجمة", "فانتازيا", "تنمية ذاتية", "خيال علمي ورعب"]

if "books" not in st.session_state:
    st.session_state.books = [
        {"id": "b1", "title": "رواية الخيميائي", "author": "باولو كويلو", "price": 150, "category": "روايات مترجمة", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400"},
        {"id": "b2", "title": "أرض زيكولا", "author": "عمرو عبد الحميد", "price": 180, "category": "فانتازيا", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400"},
        {"id": "b3", "title": "فن اللامبالاة", "author": "مارك مانسون", "price": 120, "category": "تنمية ذاتية", "image": "https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=400"}
    ]

if "cart" not in st.session_state: st.session_state.cart = []
if "orders" not in st.session_state: st.session_state.orders = []
if "comments" not in st.session_state: st.session_state.comments = {}

# 5. 🔐 نظام حماية وإخفاء لوحة التحكم
st.sidebar.markdown("### 🧭 القائمة الرئيسية")
page_options = ["🛒 المتجر الإلكتروني"]

st.sidebar.markdown("---")
admin_password = st.sidebar.text_input("🔑 دخول الإدارة (حقل سري)", type="password")

if admin_password == "admin123":
    page_options.append("🔐 لوحة الإدارة")
    st.sidebar.success("تم تفعيل صلاحيات الإدارة بنجاح!")

menu = st.sidebar.selectbox("اختار الصفحة المعروضة:", page_options)

# ==================== صفحة المتجر ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">عالمك الخاص لأجمل الكتب والروايات النيون</div>', unsafe_allow_html=True)

    col_search, col_filter = st.columns(2)
    with col_search:
        search_query = st.text_input("🔍 ابحث عن اسم رواية أو مؤلف:")
    with col_filter:
        categories_filter = ["الكل"] + st.session_state.categories
        selected_category = st.selectbox("📂 تصنيف الكتب:", categories_filter)

    filtered_books = [b for b in st.session_state.books if ((selected_category == "الكل" or b["category"] == selected_category) and (search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()))]

    if not filtered_books:
        st.warning("عفواً، لا يوجد كتب تطابق بحثك حالياً.")
    else:
        cols = st.columns(3)
        for index, book in enumerate(filtered_books):
            with cols[index % 3]:
                st.markdown(f"""
                <div class="book-card">
                    <div>
                        <img src="{book['image']}" class="book-img">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">تأليف: {book['author']}</div>
                        <div class="book-category">[{book['category']}]</div>
                    </div>
                    <div class="book-price">{book['price']} جنيه</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"أضف للسلة 🛒", key=f"add_{book['id']}"):
                    st.session_state.cart.append(book)
                    st.toast(f"تم إضافة {book['title']} للسلة!")

                with st.expander("💬 آراء القراء والتعليقات"):
                    book_comments = st.session_state.comments.get(book['id'], [])
                    if not book_comments:
                        st.caption("لا توجد تعليقات بعد.")
                    for comment in book_comments:
                        st.markdown(f"• <span style='color:#00f3ff;'>{comment}</span>", unsafe_allow_html=True)
                    
                    new_comment = st.text_input("اكتب رأيك هنا:", key=f"in_{book['id']}", placeholder="رأيك في الرواية...")
                    if st.button("نشر الرأي", key=f"pub_{book['id']}"):
                        if new_comment:
                            st.session_state.comments.setdefault(book['id'], []).append(new_comment)
                            st.rerun()

    st.markdown("---")
    st.markdown('<div class="neon-subtitle" style="text-align: right;">🛒 سلة المشتريات الخاصة بك</div>', unsafe_allow_html=True)
    
    if len(st.session_state.cart) != 0:
        total_price = sum(item['price'] for item in st.session_state.cart)
        book_names = [item['title'] for item in st.session_state.cart]
        st.success(f"لديك **{len(st.session_state.cart)}** كتب في السلة | الإجمالي: **{total_price} جنيه**")
        
        with st.form("checkout_form"):
            name = st.text_input("اسمك بالكامل")
            phone = st.text_input("رقم تليفونك")
            address = st.text_input("عنوان الشحن بالتفصيل")
            submit_order = st.form_submit_button("تأكيد الطلب وشحن 🚚")
            
            if submit_order:
                if name and phone and address:
                    order_data = {"books": book_names, "total_price": total_price, "name": name, "phone": phone, "address": address}
                    git_saved = save_order_to_github(order_data)
                    st.session_state.orders.append(order_data)
                    st.session_state.cart = [] 
                    if git_saved:
                        st.success("تم إرسال طلبك وحفظه على السيرفر الآمن بنجاح! 🎉")
                    else:
                        st.success("تم تسجيل طلبك بنجاح وجاري المراجعة!")
                    st.rerun()
                else:
                    st.error("من فضلك املأ كل البيانات.")

# ==================== صفحة الإدارة المخفية ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة تحكم المدير المسؤول")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📦 الأوردرات الواردة", "➕ إضافة كتاب", "📂 إضافة قسم", "✏️ تعديل أسماء الكتب"])
    
    with tab1:
        if len(st.session_state.orders) == 0:
            st.info("لا توجد طلبات جديدة حالياً.")
        else:
            for i, order in enumerate(st.session_state.orders):
                with st.expander(f"الأوردر رقم {i+1} - من: {order['name']}"):
                    st.write(f"**الهاتف:** {order['phone']} | **العنوان:** {order['address']}")
                    st.write(f"**الكتب:** {', '.join(order['books'])}")
                    st.write(f"**الحساب الكلي:** {order['total_price']} جنيه")

    with tab2:
        st.subheader("إضافة كتاب جديد")
        with st.form("add_book", clear_on_submit=True):
            t = st.text_input("اسم الكتاب")
            a = st.text_input("اسم المؤلف")
            c = st.selectbox("اختار القسم", st.session_state.categories)
            p = st.number_input("السعر", min_value=1, step=5)
            img = st.file_uploader("صورة الغلاف", type=["png", "jpg", "jpeg"])
            if st.form_submit_button("إضافة"):
                if t and a and img:
                    base64_img = base64.b64encode(img.getvalue()).decode()
                    src = f"data:image/{img.type.split('/')[-1]};base64,{base64_img}"
                    st.session_state.books.append({"id": f"b{len(st.session_state.books)+1}", "title": t, "author": a, "price": p, "category": c, "image": src})
                    st.success(f"تم إضافة {t}")
                    st.rerun()

    with tab3:
        st.subheader("إضافة قسم جديد")
        with st.form("add_cat", clear_on_submit=True):
            nc = st.text_input("اسم القسم")
            if st.form_submit_button("حفظ القسم") and nc:
                st.session_state.categories.append(nc)
                st.success("تم إضافة القسم الجديد")
                st.rerun()

    with tab4:
        st.subheader("تعديل وتحديث بيانات الكتب الموجودة")
        if not st.session_state.books:
            st.info("لا توجد كتب لتعديلها.")
        else:
            book_to_edit = st.selectbox("اختار الكتاب المراد تعديله:", st.session_state.books, format_func=lambda x: x["title"])
            
            with st.form("edit_book_form"):
                updated_title = st.text_input("تعديل اسم الكتاب:", value=book_to_edit["title"])
                updated_author = st.text_input("تعديل اسم المؤلف:", value=book_to_edit["author"])
                updated_price = st.number_input("تعديل السعر:", value=book_to_edit["price"], min_value=1)
                
                if st.form_submit_button("💾 حفظ التعديلات الجديدة"):
                    book_to_edit["title"] = updated_title
                    book_to_edit["author"] = updated_author
                    book_to_edit["price"] = updated_price
                    st.success("تم تحديث بيانات الكتاب بنجاح بالمتجر!")
                    st.rerun()

# زرار الواتساب
whatsapp_url = "https://wa.me/201149243249?text=أهلاً%20World%20of%20Books%20عايز%20استفسر%20عن%20رواية"
st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">💬 تواصل واتساب</a>', unsafe_allow_html=True)
