import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop", page_icon="👕", layout="wide")

# 2. تهيئة مخزن البيانات المؤقت (بيتحفظ طول ما الموقع شغال)
if 'orders' not in st.session_state:
    st.session_state.orders = []

# القائمة الجانبية
page = st.sidebar.radio("انتقل إلى:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة الشاملة"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن":
    st.title("🛍️ SAWA Shop - اطلب الآن")
    st.write("أهلاً بك في متجرنا! صمم تيشيرتك المفضل.")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("الاسم بالكامل")
            phone = st.text_input("رقم الموبايل (واتساب)")
            color = st.selectbox("اختار لون التيشيرت", ["أبيض", "أسود", "رمادي", "كحلي"])
            
        with col2:
            size = st.select_slider("المقاس", options=["S", "M", "L", "XL", "XXL"])
            qty = st.number_input("الكمية", min_value=1, value=1)
            notes = st.text_area("ملاحظات خاصة بالتصميم")

    if st.button("تأكيد الطلب 🚀"):
        if name and phone:
            # إضافة الأوردر للذاكرة
            st.session_state.orders.append({
                "الاسم": name,
                "الموبايل": phone,
                "اللون": color,
                "المقاس": size,
                "الكمية": qty,
                "الحالة": "جديد 🆕"
            })
            st.success(f"ألف مبروك يا {name}! طلبك وصل للإدارة.")
            st.balloons()
        else:
            st.warning("من فضلك اكتب اسمك ورقم موبايلك")

# --- صفحة الإدارة الاحترافية ---
else:
    st.title("📊 لوحة تحكم SAWA Shop")
    
    # 1. ملخص سريع (Metrics)
    total_orders = len(st.session_state.orders)
    total_pieces = sum(item['الكمية'] for item in st.session_state.orders)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الطلبات", f"{total_orders} أوردر")
    c2.metric("إجمالي القطع", f"{total_pieces} قطعة")
    # افتراض ربح 100 جنيه في القطعة
    c3.metric("الأرباح المتوقعة", f"{total_pieces * 100} ج.م")

    st.divider()

    # 2. عرض وإدارة الجدول
    st.subheader("📋 قائمة الطلبات الحالية")
    if total_orders > 0:
        df = pd.DataFrame(st.session_state.orders)
        
        # جدول تفاعلي يتيح لك تعديل الحالة أو البيانات
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        if st.button("حفظ التعديلات"):
            st.session_state.orders = edited_df.to_dict('records')
            st.success("تم تحديث البيانات بنجاح!")
            
        if st.button("مسح كل البيانات 🗑️"):
            st.session_state.orders = []
            st.rerun()
    else:
        st.info("لا توجد طلبات مسجلة حتى الآن.")

    st.divider()

    # 3. تحليل سريع للمخزن (Charts بسيطة)
    if total_orders > 0:
        st.subheader("📈 تحليل الطلبات")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("الألوان المطلوبة")
            st.bar_chart(df['اللون'].value_counts())
        with col_b:
            st.write("المقاسات المطلوبة")
            st.bar_chart(df['المقاس'].value_counts())
