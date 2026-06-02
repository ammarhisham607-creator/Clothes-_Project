import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="World of Books", page_icon="📚", layout="wide")

# 2. كود الديكور والنيون وزرار الواتساب (CSS)
neon_style = """
<style>
.stApp {
    background: linear-gradient(rgba(15, 15, 26, 0.9), rgba(15, 15, 26, 0.95)), 
                url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600');
    background-size: cover; background-position: center; background-attachment: fixed; direction: rtl;
}
.neon-title { color: #fff; text-align: center; font-size: 3.5rem; font-weight: bold; text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff; margin-bottom: 5px; padding-top: 20px; }
.neon-subtitle { color: #ff007f; text-align: center; font-size: 1.5rem; text-shadow: 0 0 5px #ff007f, 0 0 10px #ff007f; margin-bottom: 40px; }
.book-card { background: rgba(25, 25, 40, 0.65); border: 2px solid #ff007f; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(255, 0, 127, 0.3); transition: all 0.3s ease; }
.book-card:hover { transform: translateY(-10px); box-shadow: 0 0 25px rgba(255, 0, 127, 0.8); }
.book-title { color: #fff; font-size: 1.4rem; font-weight: bold; text-shadow: 0 0 5px #fff; margin-top: 15px; }
.book-author { color: #00f3ff; font-size: 1rem; text-shadow: 0 0 3px #00f3ff; }
.book-category { color: #f1c40f; font-size: 0.9rem; margin-bottom: 10px; }
.book-price { color: #39ff14; font-size: 1.3rem; font-weight: bold; text-shadow: 0 0 5px #39ff14; }
div.stButton > button { background-color: transparent !important; color: #00f3ff !important; border: 2px solid #00f3ff !important; border-radius: 8px !important; font-weight: bold !important; box-shadow: 0 0 10px rgba(0, 243, 255, 0.4) !important; text-shadow: 0 0 5px #00f3ff !important; width: 100%; }
div.stButton > button:hover { background-color: #00f3ff !important; color: #121212 !important; box-shadow: 0 0 25px #00f3ff !important; }
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; font-size: 16px; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# 3. إعداد الذاكرة للسلة والأوردرات
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []

# 4. القائمة الجانبية
menu = st.sidebar.selectbox("اختار الصفحة", ["🛒 المتجر الإلكتروني", "🔐 لوحة الإدارة"])

# قاعدة بيانات الكتب (تم إضافة التصنيف)
books = [
    {"id": "b1", "title": "رواية الخيميائي", "author": "باولو كويلو", "price": 150, "category": "روايات مترجمة", "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400"},
    {"id": "b2", "title": "أرض زيكولا", "author": "عمرو عبد الحميد", "price": 180, "category": "فانتازيا", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400"},
    {"id": "b3", "title": "فن اللامبالاة", "author": "مارك مانسون", "price": 120, "category": "تنمية ذاتية", "image": "https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=400"},
    {"id": "b4", "title": "يوتوبيا", "author": "أحمد خالد توفيق", "price": 100, "category": "خيال علمي ورعب", "image": "https://images.unsplash.com/photo-1614165936126-2ed18e471b3b?q=80&w=400"}
]

# ==================== صفحة المتجر ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">عالمك الخاص لأجمل الكتب والروايات النيون</div>', unsafe_allow_html=True)

    # شريط البحث والفلترة
    col_search, col_filter = st.columns(2)
    with col_search:
        search_query = st.text_input("🔍 ابحث عن اسم رواية أو مؤلف:")
    with col_filter:
        categories = ["الكل"] + list(set([book["category"] for book in books]))
        selected_category = st.selectbox("📂 تصنيف الكتب:", categories)

    # تطبيق البحث والفلترة على قائمة الكتب
    filtered_books = []
    for book in books:
        match_category = (selected_category == "الكل") or (book["category"] == selected_category)
        match_search = search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()
        
        if match_category and match_search:
            filtered_books.append(book)

    # عرض الكتب المفلترة
    if not filtered_books:
        st.warning("عفواً، لا يوجد كتب تطابق بحثك حالياً.")
    else:
        # تقسيم الكتب لصفوف (كل صف 3 كتب)
        cols = st.columns(3)
        for index, book in enumerate(filtered_books):
            with cols[index % 3]:
                st.markdown(f"""
                <div class="book-card">
                    <img src="{book['image']}" style="width:100%; height:250px; object-fit:cover; border-radius:10px; border: 1px solid #ff007f;">
                    <div class="book-title">{book['title']}</div>
                    <div class="book-author">تأليف: {book['author']}</div>
                    <div class="book-category">[{book['category']}]</div>
                    <div class="book-price">{book['price']} جنيه</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                # زر الإضافة للسلة
                if st.button(f"أضف للسلة 🛒", key=book['id']):
                    st.session_state.cart.append(book)
                    st.toast(f"تم إضافة {book['title']} للسلة بنجاح!")

    # ==================== قسم عربة التسوق ====================
    st.markdown("---")
    st.markdown('<div class="neon-subtitle" style="text-align: right;">🛒 سلة المشتريات الخاصة بك</div>', unsafe_allow_html=True)
    
    if len(st.session_state.cart) == 0:
        st.info("السلة فارغة حالياً. تصفح الكتب وأضف ما يعجبك!")
    else:
        # حساب الإجمالي
        total_price = sum(item['price'] for item in st.session_state.cart)
        book_names = [item['title'] for item in st.session_state.cart]
        
        st.success(f"لديك **{len(st.session_state.cart)}** كتب في السلة | الإجمالي المطلوب: **{total_price} جنيه**")
        st.write("الكتب المختارة: " + "، ".join(book_names))
        
        # فورم الدفع والشحن
        with st.form("checkout_form"):
            st.write("✍️ **أكمل بياناتك لتأكيد الطلب:**")
            name = st.text_input("اسمك بالكامل")
            phone = st.text_input("رقم تليفونك")
            address = st.text_input("عنوان الشحن بالتفصيل")
            submit_order = st.form_submit_button("تأكيد الطلب شحن 🚚")
            
            if submit_order:
                if name and phone and address:
                    new_order = {
                        "books": book_names,
                        "total_price": total_price,
                        "name": name,
                        "phone": phone,
                        "address": address
                    }
                    # لاحظ: هنا بتضيف الأوردر للذاكرة، تقدر تعدل السطر ده عشان يبعت البيانات لملف الـ GitHub بتاعك
                    st.session_state.orders.append(new_order)
                    st.session_state.cart = [] # تفريغ السلة بعد الطلب
                    st.success("تم إرسال طلبك بنجاح! جاري التجهيز للشحن 🎉")
                else:
                    st.error("من فضلك املأ كل البيانات عشان نقدر نوصلك الأوردر.")

        # زر لتفريغ السلة لو العميل غير رأيه
        if st.button("🗑️ إفراغ السلة"):
            st.session_state.cart = []
            st.rerun()

# ==================== صفحة الإدارة ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة تحكم المسؤول")
    password = st.text_input("ادخل كلمة سر المدير لرؤية الطلبات", type="password")
    
    if password == "admin123":
        st.success("أهلاً بك يا مدير الموقع! إليك الطلبات الحالية:")
        
        if len(st.session_state.orders) == 0:
            st.info("مفيش أي أوردرات جديدة حالياً.")
        else:
            for i, order in enumerate(st.session_state.orders):
                with st.expander(f"📦 أوردر رقم {i+1} - بإجمالي {order['total_price']} جنيه"):
                    st.write(f"**اسم العميل:** {order['name']}")
                    st.write(f"**رقم الهاتف:** {order['phone']}")
                    st.write(f"**العنوان:** {order['address']}")
                    st.write(f"**الكتب المطلوبة:** {', '.join(order['books'])}")
                    st.write(f"**الإجمالي:** {order['total_price']} جنيه")
    elif password != "":
        st.error("كلمة السر خطأ!")

# زرار الواتساب الثابت
whatsapp_url = "https://wa.me/201149243249?text=أهلاً%20World%20of%20Books%20عايز%20استفسر%20عن%20رواية"
st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">💬 تواصل واتساب</a>', unsafe_allow_html=True)
