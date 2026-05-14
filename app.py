import streamlit as st
import pandas as pd
from PIL import Image

# 1. إعدادات الصفحة والديكور العام
st.set_page_config(page_title="SAWA Shop Portal", page_icon="👕", layout="wide")

# كود CSS محسن لتجنب الأخطاء وتجميل الواجهة
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #000000;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #00ffcc;
    }
    /* تنسيق الكروت الإحصائية */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة مخزن البيانات (Session State) لضمان عدم حدوث خطأ "KeyError"
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'categories' not in st.session_state:
    st.session_state.categories = ["جيم 💪", "حيوانات 🦁", "منوعات ✨"]
if 'catalog_images' not in st.session_state:
    st.session_state.catalog_images = {cat: [] for cat in st.session_state.categories}
if 'tshirt_colors' not in st.session_state:
    st.session_state.tshirt_colors = ["أبيض", "أسود", "رمادي", "كحلي"]

# 3. القائمة الجانبية للتنقل
st.sidebar.markdown("<h2 style='text-align: center;'>SAWA Shop</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("القائمة:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن":
    st.markdown("<h1 style='text-align: center;'>👕 صمم تيشيرتك مع سوا شوب</h1>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📝 بيانات الطلب")
        cust_name = st.text_input("الاسم بالكامل")
        cust_phone = st.text_input("رقم الموبايل")
        cust_color = st.selectbox("اختار لون التيشيرت", st.session_state.tshirt_colors)
        cust_size = st.select_slider("المقاس", options=["S", "M", "L", "XL", "XXL"])
        cust_qty = st.number_input("الكمية", min_value=1, step=1)

    with col2:
        st.subheader("🖼️ اختيار التصميم")
        choice = st.radio("مصدر الصورة:", ["من كتالوج البراند", "ارفع صورتي الخاصة"], horizontal=True)
        
        selected_design_info = None
        if choice == "من كتالوج البراند":
            selected_cat = st.selectbox("اختار القسم", st.session_state.categories)
            images_in_cat = st.session_state.catalog_images.get(selected_cat, [])
            
            if images_in_cat:
                img_idx = st.slider("تصفح التصاميم", 1, len(images_in_cat)) - 1
                st.image(images_in_cat[img_idx], use_container_width=True)
                selected_design_info = f"تصميم من كتالوج {selected_cat} رقم {img_idx + 1}"
            else:
                st.info("هذا القسم فارغ حالياً، يمكنك رفع صورتك الخاصة.")
        else:
            selected_design_info = st.file_uploader("ارفع التصميم الخاص بك", type=['png', 'jpg', 'jpeg'])

    if st.button("إرسال الطلب الآن ✨"):
        if cust_name and cust_phone and selected_design_info:
            new_order = {
                "الاسم": cust_name,
                "الموبايل": cust_phone,
                "اللون": cust_color,
                "المقاس": cust_size,
                "الكمية": cust_qty,
                "التصميم": str(selected_design_info),
                "الحالة": "جديد"
            }
            st.session_state.orders.append(new_order)
            st.success("تم استلام طلبك بنجاح!")
            st.balloons()
        else:
            st.error("برجاء إكمال الاسم، الهاتف، والتصميم.")

# --- صفحة الإدارة ---
else:
    st.markdown("<h1>📊 لوحة التحكم</h1>", unsafe_allow_html=True)
    
    # بطاقات الإحصائيات (Metrics)
    total_orders = len(st.session_state.orders)
    total_qty = sum(o['الكمية'] for o in st.session_state.orders)
    
    m1, m2, m3 = st.columns(3)
    m1.markdown(f"<div class='metric-card'><h3>عدد الطلبات</h3><h2>{total_orders}</h2></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-card'><h3>إجمالي القطع</h3><h2>{total_qty}</h2></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-card'><h3>الأرباح المتوقعة</h3><h2>{total_qty * 100} ج.م</h2></div>", unsafe_allow_html=True)

    st.divider()
    
    tab_manage, tab_settings = st.tabs(["📥 إدارة الطلبات", "⚙️ إعدادات المتجر"])
    
    with tab_manage:
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            edited_df = st.data_editor(df, use_container_width=True)
            if st.button("حفظ التعديلات"):
                st.session_state.orders = edited_df.to_dict('records')
                st.success("تم التحديث!")
        else:
            st.info("لا توجد طلبات حالياً.")

    with tab_settings:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("تخصيص الألوان")
            new_color = st.text_input("أضف لون جديد")
            if st.button("إضافة اللون"):
                if new_color: st.session_state.tshirt_colors.append(new_color); st.rerun()
            
            st.subheader("إضافة قسم صور")
            new_cat = st.text_input("أضف قسم جديد")
            if st.button("إضافة القسم"):
                if new_cat: 
                    st.session_state.categories.append(new_cat)
                    st.session_state.catalog_images[new_cat] = []
                    st.rerun()
        
        with c2:
            st.subheader("رفع صور للكتالوج")
            target_cat = st.selectbox("اختار القسم لرفع الصور إليه", st.session_state.categories)
            files = st.file_uploader("اختار الصور", accept_multiple_files=True)
            if st.button("حفظ الصور في القسم"):
                if files:
                    for f in files:
                        st.session_state.catalog_images[target_cat].append(Image.open(f))
                    st.success(f"تم رفع {len(files)} صورة بنجاح!")
