import streamlit as st
import base64

# 1. إعدادات الصفحة
st.set_page_config(page_title="World of Books", page_icon="📚", layout="wide")

# 2. كود الديكور والنيون المتحرك (CSS)
neon_style = """
<style>
/* خلفية الموقع */
.stApp {
    background: linear-gradient(rgba(15, 15, 26, 0.9), rgba(15, 15, 26, 0.95)), 
                url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600');
    background-size: cover; background-position: center; background-attachment: fixed; direction: rtl;
}

/* 🌟 إضافة تأثير النيون اللي بينور ويطفي (Blink / Pulse) 🌟 */
@keyframes neon-pulse {
    0% { text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff; opacity: 1; }
    50% { text-shadow: 0 0 2px #00f3ff, 0 0 5px #00f3ff; opacity: 0.8; }
    100% { text-shadow: 0 0 5px #00f3ff, 0 0 10px #00f3ff, 0 0 20px #00f3ff; opacity: 1; }
}

.neon-title { 
    color: #fff; text-align: center; font-size: 3.5rem; font-weight: bold; 
    margin-bottom: 5px; padding-top: 20px;
    animation: neon-pulse 2s infinite; /* تشغيل الحركة */
}

.neon-subtitle { color: #ff007f; text-align: center; font-size: 1.5rem; text-shadow: 0 0 5px #ff007f, 0 0 10px #ff007f; margin-bottom: 40px; }

/* 🛠️ تظبيط مقاسات الكروت عشان الكلام مايدخلش في بعضه 🛠️ */
.book-card { 
    background: rgba(25, 25, 40, 0.65); border: 2px solid #ff007f; border-radius: 15px; 
    padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(255, 0, 127, 0.3); 
    transition: all 0.3s ease;
    display: flex; flex-direction: column; justify-content: space-between; /* توزيع المسافات صح */
    height: 100%; min-height: 420px; margin-bottom: 20px;
}
.book-card:hover { transform: translateY(-10px); box-shadow: 0 0 25px rgba(255, 0, 127, 0.8); }
.book-img { width: 100%; height: 250px; object-fit: cover; border-radius: 10px; border: 1px solid #ff007f; margin-bottom: 15px; }
.book-title { color: #fff; font-size: 1.4rem; font-weight: bold; text-shadow: 0 0 5px #fff; line-height: 1.3; margin-bottom: 10px;}
.book-author { color: #00f3ff; font-size: 1rem; text-shadow: 0 0 3px #00f3ff; margin-bottom: 5px;}
.book-category { color: #f1c40f; font-size: 0.9rem; margin-bottom: 15px; }
.book-price { color: #39ff14; font-size: 1.4rem; font-weight: bold; text-shadow: 0 0 5px #39ff14; margin-top: auto; } /* margin-top: auto يخلي السعر دايماً تحت */

div.stButton > button { background-color: transparent !important; color: #00f3ff !important; border: 2px solid #00f3ff !important; border-radius: 8px !important; font-weight: bold !important; box-shadow: 0 0 10px rgba(0, 243, 255, 0.4) !important; text-shadow: 0 0 5px #00f3ff !important; width: 100%; margin-top: 10px;}
div.stButton > button:hover { background-color: #00f3ff !important; color: #121212 !important; box-shadow: 0 0 25px #00f3ff !important; }

/* زرار الواتساب */
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; font-size: 16px; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# 3. إعداد الذاكرة (Books, Categories, Cart, Orders)
if "categories" not in st.session_state:
    st.session_state.categories = ["روايات مترجمة", "فانتازيا", "تنمية ذاتية", "خيال علمي ورعب"]

if "books" not in st.session_state:
    st.session_state.books = [
        {"id": "b1", "title": "رواية الخيميائي", "author": "باولو كويلو", "price": 150, "category": "روايات مترجمة", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400"},
        {"id": "b2", "title": "أرض زيكولا", "author": "عمرو عبد الحميد", "price": 180, "category": "فانتازيا", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400"},
        {"id": "b3", "title": "فن اللامبالاة", "author": "مارك مانسون", "price": 120, "category": "تنمية ذاتية", "image": "https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=400"}
    ]

if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []

# 4. القائمة الجانبية
menu = st.sidebar.selectbox("اختار الصفحة", ["🛒 المتجر الإلكتروني", "🔐 لوحة الإدارة"])

# ==================== صفحة المتجر ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">عالمك الخاص لأجمل الكتب والروايات النيون</div>', unsafe_allow_html=True)

    # شريط البحث والفلترة
    col_search, col_filter = st.columns(2)
    with col_search:
        search_query = st.text_input("🔍 ابحث عن اسم رواية أو مؤلف:")
    with col_filter:
        categories_filter = ["الكل"] + st.session_state.categories
        selected_category = st.selectbox("📂 تصنيف الكتب:", categories_filter)

    # فلترة الكتب
    filtered_books = []
    for book in st.session_state.books:
        match_category = (selected_category == "الكل") or (book["category"] == selected_category)
        match_search = search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()
        if match_category and match_search:
            filtered_books.append(book)

    # عرض الكتب
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
                
                if st.button(f"أضف للسلة 🛒", key=f"btn_{book['id']}"):
                    st.session_state.cart.append(book)
                    st.toast(f"تم إضافة {book['title']} للسلة بنجاح!")

    # ==================== قسم عربة التسوق ====================
    st.markdown("---")
    st.markdown('<div class="neon-subtitle" style="text-align: right;">🛒 سلة المشتريات الخاصة بك</div>', unsafe_allow_html=True)
    
    if len(st.session_state.cart) == 0:
        st.info("السلة فارغة حالياً. تصفح الكتب وأضف ما يعجبك!")
    else:
        total_price = sum(item['price'] for item in st.session_state.cart)
        book_names = [item['title'] for item in st.session_state.cart]
        
        st.success(f"لديك **{len(st.session_state.cart)}** كتب في السلة | الإجمالي: **{total_price} جنيه**")
        
        with st.form("checkout_form"):
            st.write("✍️ **أكمل بياناتك لتأكيد الطلب:**")
            name = st.text_input("اسمك بالكامل")
            phone = st.text_input("رقم تليفونك")
            address = st.text_input("عنوان الشحن بالتفصيل")
            submit_order = st.form_submit_button("تأكيد الطلب شحن 🚚")
            
            if submit_order:
                if name and phone and address:
                    new_order = {"books": book_names, "total_price": total_price, "name": name, "phone": phone, "address": address}
                    st.session_state.orders.append(new_order)
                    st.session_state.cart = [] 
                    st.success("تم إرسال طلبك بنجاح! جاري التجهيز للشحن 🎉")
                else:
                    st.error("من فضلك املأ كل البيانات.")

        if st.button("🗑️ إفراغ السلة"):
            st.session_state.cart = []
            st.rerun()

# ==================== صفحة الإدارة ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة تحكم المسؤول")
    password = st.text_input("ادخل كلمة السر", type="password")
    
    if password == "admin123":
        # تقسيم لوحة الإدارة لتبويبات (Tabs) لتنظيم الشغل
        tab1, tab2, tab3 = st.tabs(["📦 الأوردرات الجديدة", "➕ إضافة كتاب جديد", "📂 إضافة قسم جديد"])
        
        # التبويب الأول: الأوردرات
        with tab1:
            if len(st.session_state.orders) == 0:
                st.info("مفيش أي أوردرات جديدة حالياً.")
            else:
                for i, order in enumerate(st.session_state.orders):
                    with st.expander(f"📦 أوردر رقم {i+1} - {order['name']}"):
                        st.write(f"**رقم الهاتف:** {order['phone']} | **العنوان:** {order['address']}")
                        st.write(f"**الكتب المطلوبة:** {', '.join(order['books'])}")
                        st.write(f"**الإجمالي:** {order['total_price']} جنيه")

        # التبويب الثاني: إضافة كتاب
        with tab2:
            st.subheader("إضافة رواية أو كتاب للمتجر")
            with st.form("add_book_form", clear_on_submit=True):
                new_title = st.text_input("اسم الكتاب")
                new_author = st.text_input("اسم المؤلف")
                new_category = st.selectbox("اختار القسم", st.session_state.categories)
                new_price = st.number_input("السعر (بالجنيه)", min_value=1, step=5)
                # رفع الصورة
                uploaded_image = st.file_uploader("ارفع صورة الغلاف (JPG/PNG)", type=["png", "jpg", "jpeg"])
                
                submit_book = st.form_submit_button("✅ إضافة الكتاب للمتجر")
                
                if submit_book:
                    if new_title and new_author and uploaded_image:
                        # تحويل الصورة المرفوعة لصيغة يقدر الـ HTML يقرأها (Base64)
                        bytes_data = uploaded_image.getvalue()
                        base64_img = base64.b64encode(bytes_data).decode()
                        img_src = f"data:image/{uploaded_image.type.split('/')[-1]};base64,{base64_img}"
                        
                        new_book_data = {
                            "id": f"b{len(st.session_state.books) + 1}",
                            "title": new_title,
                            "author": new_author,
                            "price": new_price,
                            "category": new_category,
                            "image": img_src
                        }
                        st.session_state.books.append(new_book_data)
                        st.success(f"تمت إضافة كتاب '{new_title}' بنجاح!")
                    else:
                        st.error("لازم تكتب اسم الكتاب والمؤلف وترفع الصورة!")

        # التبويب الثالث: إضافة قسم
        with tab3:
            st.subheader("إضافة قسم جديد (مثال: تاريخ، رعب، الخ)")
            with st.form("add_category_form", clear_on_submit=True):
                new_cat_name = st.text_input("اسم القسم الجديد")
                submit_cat = st.form_submit_button("✅ حفظ القسم")
                
                if submit_cat:
                    if new_cat_name and new_cat_name not in st.session_state.categories:
                        st.session_state.categories.append(new_cat_name)
                        st.success(f"تم إضافة قسم '{new_cat_name}' وتقدر تختاره دلوقتي وأنت بتضيف أي كتاب جديد.")
                    elif new_cat_name in st.session_state.categories:
                        st.warning("القسم ده موجود بالفعل!")
                    else:
                        st.error("اكتب اسم القسم أولاً.")
    elif password != "":
        st.error("كلمة السر خطأ!")

# زرار الواتساب الثابت
whatsapp_url = "https://wa.me/201149243249?text=أهلاً%20World%20of%20Books%20عايز%20استفسر%20عن%20رواية"
st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">💬 تواصل واتساب</a>', unsafe_allow_html=True)
