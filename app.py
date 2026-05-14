import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop - Professional", page_icon="👕", layout="wide")

# 2. تهيئة البيانات في الذاكرة (لأننا لسه ما فعلناش الشيت)
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'categories' not in st.session_state:
    st.session_state.categories = {"جيم 💪": [], "حيوانات 🦁": [], "ألعاب 🎮": []}
if 'tshirt_colors' not in st.session_state:
    st.session_state.tshirt_colors = ["أبيض", "أسود", "رمادي", "كحلي"]

# القائمة الجانبية
page = st.sidebar.radio("انتقل إلى:", ["🛍️ متجر الزبائن (اطلب الآن)", "⚙️ لوحة الإدارة الذكية"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن (اطلب الآن)":
    st.title("🛍️ SAWA Shop - صمم تيشيرتك")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ بيانات الطلب")
        name = st.text_input("اسمك")
        phone = st.text_input("رقم الواتساب")
        color = st.selectbox("اختار لون التيشيرت", st.session_state.tshirt_colors)
        size = st.select_slider("المقاس", options=["S", "M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية", min_value=1, value=1)

    with col2:
        st.subheader("2️⃣ اختر التصميم")
        choice = st.radio("مصدر الصورة:", ["ارفع صورتي الخاصة", "اختر من تصاميم SAWA Shop"])
        
        selected_design = None
        if choice == "ارفع صورتي الخاصة":
            selected_design = st.file_uploader("ارفع صورتك هنا", type=['png', 'jpg'])
        else:
            cat = st.selectbox("اختار القسم", list(st.session_state.categories.keys()))
            st.info(f"عرض تصاميم قسم: {cat}")
            # هنا يمكنك وضع روابط لصور جاهزة مستقبلاً
            st.write("سيتم عرض الصور المتاحة هنا فور إضافتها من الإدارة")
            selected_design = f"تصميم جاهز من قسم {cat}"

    if st.button("تأكيد وطلب الأوردر 🚀"):
        if name and phone:
            st.session_state.orders.append({
                "الاسم": name, "الموبايل": phone, "اللون": color, 
                "المقاس": size, "الكمية": qty, "التصميم": selected_design, "الحالة": "جديد"
            })
            st.success("تم استلام طلبك بنجاح!")
            st.balloons()

# --- صفحة الإدارة ---
else:
    st.title("⚙️ لوحة إدارة SAWA Shop الشاملة")
    
    # تبويبات داخل صفحة الإدارة لتنظيم الشغل
    tab1, tab2, tab3 = st.tabs(["📥 الطلبات الواردة", "🎨 إدارة المنتجات", "📊 التقارير"])
    
    with tab1:
        st.subheader("إدارة الطلبات الحالية")
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
            if st.button("حفظ التحديثات"):
                st.session_state.orders = edited_df.to_dict('records')
                st.success("تم الحفظ!")
        else:
            st.info("لا توجد طلبات.")

    with tab2:
        st.subheader("تخصيص المتجر")
        
        # إضافة لون جديد
        col_a, col_b = st.columns(2)
        with col_a:
            new_color = st.text_input("إضافة لون تيشيرت جديد")
            if st.button("إضافة اللون"):
                if new_color and new_color not in st.session_state.tshirt_colors:
                    st.session_state.tshirt_colors.append(new_color)
                    st.success(f"تم إضافة لون: {new_color}")
        
        # إضافة قسم صور جديد
        with col_b:
            new_cat = st.text_input("إضافة اسم قسم تصاميم جديد")
            if st.button("إضافة القسم"):
                if new_cat and new_cat not in st.session_state.categories:
                    st.session_state.categories[new_cat] = []
                    st.success(f"تم إضافة قسم: {new_cat}")

    with tab3:
        st.subheader("نظرة عامة على الأرباح")
        total_p = sum(item['الكمية'] for item in st.session_state.orders)
        st.metric("إجمالي القطع المطلوبة", total_p)
        st.metric("صافي الربح المتوقع (100ج/قطعة)", f"{total_p * 100} ج.م")
