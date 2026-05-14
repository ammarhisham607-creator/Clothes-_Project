import streamlit as st
import pandas as pd
from PIL import Image

# 1. إعدادات الصفحة والديكور العام
st.set_page_config(page_title="SAWA Shop | البراند بتاعك", page_icon="👕", layout="wide")

# كود CSS لتجميل الواجهة
st.markdown("""
    <style>
    /* تغيير لون الخلفية والعناوين */
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #1e1e1e;
        font-family: 'Cairo', sans-serif;
        text-align: right;
    }
    
    /* تجميل القائمة الجانبية */
    .stSidebar {
        background-color: #ffffff !important;
        border-right: 2px solid #eeeeee;
    }
    
    /* تجميل الزراير */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #000000;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #00ffcc;
        border: none;
    }

    /* كروت العرض */
    .css-1r6il73 {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة البيانات (Session State)
if 'orders' not in st.session_state: st.session_state.orders = []
if 'categories' not in st.session_state: st.session_state.categories = ["جيم 💪", "حيوانات 🦁"]
if 'catalog_images' not in st.session_state: st.session_state.catalog_images = {}
if 'tshirt_colors' not in st.session_state: st.session_state.tshirt_colors = ["أبيض", "أسود", "رمادي", "كحلي"]

# القائمة الجانبية مع لوجو نصي
st.sidebar.markdown("<h1 style='text-align: center; color: #000;'>SAWA Shop</h1>", unsafe_allow_html=True)
page = st.sidebar.radio("القائمة:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن":
    st.markdown("<h1 style='text-align: center;'>👕 صمم تيشيرتك مع سوا شوب</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>أعلى جودة طباعة وأفضل خامات القطن</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        st.subheader("📝 تفاصيل الأوردر")
        with st.container():
            name = st.text_input("الاسم بالكامل")
            phone = st.text_input("رقم الواتساب")
            color = st.selectbox("اختار لون التيشيرت", st.session_state.tshirt_colors)
            size = st.select_slider("المقاس المناسب", options=["S", "M", "L", "XL", "XXL"])
            qty = st.number_input("عدد القطع", min_value=1, step=1)

    with col2:
        st.subheader("🖼️ اختيار التصميم")
        source = st.radio("حابب تختار إيه؟", ["من كتالوج البراند", "ارفع صورتي الخاصة"], horizontal=True)
        
        final_design = None
        if source == "من كتالوج البراند":
            cat_choice = st.selectbox("اختار القسم", st.session_state.categories)
            if cat_choice in st.session_state.catalog_images and st.session_state.catalog_images[cat_choice]:
                img_list = st.session_state.catalog_images[cat_choice]
                selected_idx = st.slider("قلب في التصاميم", 1, len(img_list)) - 1
                st.image(img_list[selected_idx], use_column_width=True, caption=f"تصميم رقم {selected_idx + 1}")
                final_design = f"كتالوج: {cat_choice} #{selected_idx+1}"
            else:
                st.info("القسم ده لسه ملوش صور، تقدر ترفع صورتك الخاصة حالياً.")
        else:
            final_design = st.file_uploader("ارفع صورتك (PNG/JPG)", type=['png', 'jpg', 'jpeg'])

    st.divider()
    if st.button("إرسال الطلب الآن ✨"):
        if name and phone and final_design:
            st.session_state.orders.append({
                "الاسم": name, "الموبايل": phone, "اللون": color, 
                "المقاس": size, "الكمية": qty, "التصميم": final_design, "الحالة": "جديد"
            })
            st.success(f"يا {name}، أوردرك وصل وسنتواصل معك عبر الواتساب!")
            st.balloons()
        else:
            st.error("كمل البيانات الأول عشان الأوردر يوصل صح!")

# --- صفحة الإدارة ---
else:
    st.markdown("<h1>📊 لوحة التحكم والإدارة</h1>", unsafe_allow_html=True)
    
    # بطاقات إحصائية سريعة
    t_orders = len(st.session_state.orders)
    t_pcs = sum(item['الكمية'] for item in st.session_state.orders)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div style='background:#fff; padding:20px; border-radius:10px; text-align:center; border-bottom: 5px solid #000;'><h3>الطلبات</h3><h2>{t_orders}</h2></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div style='background:#fff; padding:20px; border-radius:10px; text-align:center; border-bottom: 5px solid #00ffcc;'><h3>إجمالي القطع</h3><h2>{t_pcs}</h2></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div style='background:#fff; padding:20px; border-radius:10px; text-align:center; border-bottom: 5px solid #ffcc00;'><h3>الأرباح</h3><h2>{t_pcs * 100} ج.م</h2></div>", unsafe_allow_html=True)

    st.divider()
    
    tab_orders, tab_edit = st.tabs(["📥 إدارة الطلبات", "🖼️ تحديث الكتالوج والألوان"])
    
    with tab_orders:
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            st.data_editor(df, use_container_width=True)
            if st.button("مسح كل البيانات (تصفير اليوم)"):
                st.session_state.orders = []
                st.rerun()
        else:
            st.info("مفيش أوردرات جديدة.")

    with tab_edit:
        c_a, c_b = st.columns(2)
        with c_a:
            st.subheader("ألوان التيشرتات")
            for c in st.session_state.tshirt_colors:
                st.write(f"- {c}")
            new_c = st.text_input("لون جديد")
            if st.button("إضافة اللون"): 
                st.session_state.tshirt_colors.append(new_c)
                st.rerun()
        
        with c_b:
            st.subheader("صور الكتالوج")
            target = st.selectbox("اختار القسم", st.session_state.categories)
            up_files = st.file_uploader("ارفع صور الأقسام", accept_multiple_files=True)
            if st.button("حفظ الصور"):
                if target not in st.session_state.catalog_images: st.session_state.catalog_images[target] = []
                for f in up_files:
                    st.session_state.catalog_images[target].append(Image.open(f))
                st.success("تم التحديث!")
