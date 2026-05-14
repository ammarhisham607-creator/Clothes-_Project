import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop", page_icon="👕", layout="wide")

# 2. تهيئة الذاكرة لتخزين الطلبات (لو مش موجودة)
if 'orders_list' not in st.session_state:
    st.session_state.orders_list = []

# القائمة الجانبية للتنقل
page = st.sidebar.selectbox("اختار الصفحة", ["متجر الزبائن (SAWA Shop)", "لوحة تحكم الإدارة"])

# --- الصفحة الأولى: متجر الزبائن ---
if page == "متجر الزبائن (SAWA Shop)":
    st.title("🛍️ SAWA Shop - اطلب تيشيرتك الآن")
    
    col1, col2 = st.columns(2)
    with col1:
        color = st.selectbox("اختار لون التيشيرت", ["أبيض", "أسود", "رمادي", "كحلي"])
        size = st.select_slider("اختار المقاس", options=["S", "M", "L", "XL", "XXL"])
        design = st.file_uploader("ارفع الصورة اللي عايز تطبعها", type=['png', 'jpg', 'jpeg'])
        
    with col2:
        customer_name = st.text_input("اسمك بالكامل")
        phone_number = st.text_input("رقم الموبايل")
        quantity = st.number_input("عدد القطع", min_value=1, value=1)

    if st.button("إرسال الأوردر"):
        if customer_name and phone_number:
            # إضافة البيانات للذاكرة عشان تظهر للإدارة
            new_order = {
                "الاسم": customer_name,
                "الموبايل": phone_number,
                "اللون": color,
                "المقاس": size,
                "الكمية": quantity,
                "الحالة": "قيد التنفيذ"
            }
            st.session_state.orders_list.append(new_order)
            
            st.success(f"شكراً يا {customer_name}! تم إرسال طلبك للإدارة بنجاح.")
            st.balloons()
        else:
            st.warning("من فضلك اكتب الاسم ورقم الموبايل")

# --- الصفحة الثانية: لوحة الإدارة ---
else:
    st.title("📊 لوحة تحكم SAWA Shop")
    
    # عرض الطلبات الواردة من الزبائن
    st.header("📥 الطلبات الجديدة (من صفحة الزبائن)")
    
    if len(st.session_state.orders_list) > 0:
        # تحويل القائمة لجدول منظم
        df = pd.DataFrame(st.session_state.orders_list)
        st.table(df)
        
        if st.button("مسح جميع الطلبات"):
            st.session_state.orders_list = []
            st.rerun()
    else:
        st.info("لا توجد طلبات جديدة حالياً.")

    st.divider()
    
    # إعدادات المخزن (الحسابات اللي عملناها قبل كدة)
    st.header("📦 إدارة التكاليف والمخزن")
    cost_plain = st.sidebar.number_input("سعر التيشرت السادة", value=150.0)
    cost_printing = st.sidebar.number_input("تكلفة الطباعة", value=50.0)
    
    selling_price = st.number_input("سعر البيع الافتراضي", value=300.0)
    
    if len(st.session_state.orders_list) > 0:
        total_revenue = len(st.session_state.orders_list) * selling_price
        total_cost = len(st.session_state.orders_list) * (cost_plain + cost_printing)
        st.metric("إجمالي أرباح الطلبات الحالية", f"{total_revenue - total_cost} EGP")
