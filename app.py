import streamlit as st
import pandas as pd
from PIL import Image
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop", page_icon="👕", layout="wide")

# 2. تهيئة البيانات بشكل سليم
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'categories' not in st.session_state:
    st.session_state.categories = ["جيم 💪", "حيوانات 🦁"]
if 'catalog_images' not in st.session_state:
    st.session_state.catalog_images = {cat: [] for cat in st.session_state.categories}
if 'tshirt_colors' not in st.session_state:
    st.session_state.tshirt_colors = ["أبيض", "أسود", "رمادي", "كحلي"]

# 3. وظيفة معالجة الصور (تصغير وتقليل جودة لسرعة الموقع)
def process_and_save(uploaded_file):
    try:
        img = Image.open(uploaded_file)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        # تصغير الصورة لحجم معقول جداً
        img.thumbnail((400, 400))
        return img
    except Exception as e:
        st.error(f"خطأ في معالجة الصورة: {e}")
        return None

# القائمة الجانبية
page = st.sidebar.radio("انتقل إلى:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن":
    st.markdown("<h1 style='text-align: right;'>SAWA Shop - متجر الزبائن</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("الاسم")
        phone = st.text_input("الموبايل")
        color = st.selectbox("لون التيشيرت", st.session_state.tshirt_colors)
        size = st.selectbox("المقاس", ["S", "M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية", min_value=1)

    with col2:
        source = st.radio("اختر التصميم من:", ["الكتالوج", "رفع خاص"])
        final_design = None
        
        if source == "الكتالوج":
            cat = st.selectbox("القسم", st.session_state.categories)
            imgs = st.session_state.catalog_images.get(cat, [])
            if imgs:
                idx = st.select_slider("اختر صورة التصميم", options=range(len(imgs)), format_func=lambda x: f"صورة {x+1}")
                st.image(imgs[idx], width=200)
                final_design = f"قسم {cat} - صورة {idx+1}"
            else:
                st.warning("هذا القسم لا يحتوي على صور.")
        else:
            up = st.file_uploader("ارفع صورتك", type=['jpg', 'jpeg', 'png'])
            if up: final_design = "تصميم خاص مرفوع"

    if st.button("تأكيد الطلب ✨"):
        if name and phone and final_design:
            st.session_state.orders.append({
                "الاسم": name, "الموبايل": phone, "اللون": color, 
                "المقاس": size, "الكمية": qty, "التصميم": final_design, "الحالة": "جديد"
            })
            st.success("تم إرسال الأوردر بنجاح!")
            st.balloons()

# --- صفحة الإدارة ---
else:
    st.title("⚙️ لوحة الإدارة")
    t1, t2 = st.tabs(["📥 الأوردرات", "🎨 إضافة محتوى"])
    
    with t1:
        if st.session_state.orders:
            st.table(pd.DataFrame(st.session_state.orders))
            if st.button("مسح كل الأوردرات"):
                st.session_state.orders = []
                st.rerun()
        else:
            st.info("لا توجد أوردرات.")

    with t2:
        st.subheader("رفع صور للكتالوج")
        target_cat = st.selectbox("اختار القسم", st.session_state.categories)
        files = st.file_uploader("اختار الصور لرفعها", accept_multiple_files=True, type=['jpg', 'png', 'jpeg'])
        
        if st.button("تأكيد رفع الصور"):
            if files:
                # التأكد من وجود المفتاح في القاموس لتجنب الايرور
                if target_cat not in st.session_state.catalog_images:
                    st.session_state.catalog_images[target_cat] = []
                
                for f in files:
                    processed_img = process_and_save(f)
                    if processed_img:
                        st.session_state.catalog_images[target_cat].append(processed_img)
                st.success(f"تم إضافة {len(files)} صور لقسم {target_cat} بنجاح!")
            else:
                st.error("يرجى اختيار ملفات أولاً.")
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            new_col = st.text_input("أضف لون جديد")
            if st.button("حفظ اللون"):
                st.session_state.tshirt_colors.append(new_col)
                st.rerun()
        with c2:
            new_c = st.text_input("أضف قسم جديد")
            if st.button("حفظ القسم"):
                st.session_state.categories.append(new_c)
                st.session_state.catalog_images[new_c] = [] # تجهيز القسم لاستقبال صور
                st.rerun()
