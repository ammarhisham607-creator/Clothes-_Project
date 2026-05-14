import streamlit as st
import pandas as pd
from PIL import Image
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop", page_icon="👕", layout="wide")

# كود CSS خفيف جداً عشان ميهنجش المتصفح
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #000; color: white; }
    h1, h2, h3 { text-align: right; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظيفة لتصغير حجم الصور (عشان الموقع ميهنجش)
def process_image(uploaded_file):
    img = Image.open(uploaded_file)
    # تحويل الصورة لـ RGB إذا كانت PNG بشفافية لتجنب المشاكل
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    # تصغير الحجم بحد أقصى 500 بكسل
    img.thumbnail((500, 500))
    return img

# 3. تهيئة البيانات
if 'orders' not in st.session_state: st.session_state.orders = []
if 'categories' not in st.session_state: st.session_state.categories = ["جيم 💪", "حيوانات 🦁"]
if 'catalog_images' not in st.session_state: st.session_state.catalog_images = {cat: [] for cat in st.session_state.categories}
if 'tshirt_colors' not in st.session_state: st.session_state.tshirt_colors = ["أبيض", "أسود", "رمادي", "كحلي"]

# 4. القائمة الجانبية
page = st.sidebar.radio("القائمة:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن":
    st.markdown("<h1 style='text-align: center;'>SAWA Shop</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.subheader("📝 تفاصيل الطلب")
        name = st.text_input("الاسم")
        phone = st.text_input("الموبايل")
        color = st.selectbox("اللون", st.session_state.tshirt_colors)
        size = st.select_slider("المقاس", options=["S", "M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية", min_value=1, step=1)

    with col2:
        st.subheader("🖼️ التصميم")
        source = st.radio("المصدر:", ["من الكتالوج", "رفع صورة خاصة"], horizontal=True)
        
        design_data = None
        if source == "من الكتالوج":
            cat = st.selectbox("القسم", st.session_state.categories)
            imgs = st.session_state.catalog_images.get(cat, [])
            if imgs:
                idx = st.slider("اختر التصميم", 1, len(imgs)) - 1
                st.image(imgs[idx], use_container_width=True)
                design_data = f"Catalog: {cat} #{idx+1}"
            else:
                st.info("القسم فارغ")
        else:
            up_file = st.file_uploader("ارفع صورتك", type=['jpg', 'png'])
            if up_file:
                design_data = "Custom Design Uploaded"

    if st.button("إرسال الأوردر ✨"):
        if name and phone and design_data:
            st.session_state.orders.append({
                "الاسم": name, "الموبايل": phone, "اللون": color, 
                "المقاس": size, "الكمية": qty, "التصميم": design_data, "الحالة": "جديد"
            })
            st.success("تم الإرسال!")
            st.balloons()

# --- صفحة الإدارة ---
else:
    st.title("⚙️ الإدارة")
    
    tab1, tab2 = st.tabs(["📥 الأوردرات", "🎨 التعديلات"])
    
    with tab1:
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            st.data_editor(df, use_container_width=True)
            if st.button("مسح البيانات"):
                st.session_state.orders = []
                st.rerun()
        else:
            st.info("لا توجد طلبات")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            new_c = st.text_input("إضافة لون")
            if st.button("حفظ اللون"):
                st.session_state.tshirt_colors.append(new_c); st.rerun()
                
            new_cat = st.text_input("إضافة قسم")
            if st.button("حفظ القسم"):
                st.session_state.categories.append(new_cat)
                st.session_state.catalog_images[new_cat] = []
                st.rerun()
        
        with c2:
            st.subheader("رفع صور للكتالوج")
            target = st.selectbox("للقسم:", st.session_state.categories)
            files = st.file_uploader("اختر الصور", accept_multiple_files=True)
            if st.button("رفع الصور"):
                if files:
                    for f in files:
                        processed = process_image(f)
                        st.session_state.catalog_images[target].append(processed)
                    st.success("تم الرفع")
