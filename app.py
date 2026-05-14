import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop", page_icon="👕", layout="wide")

# 2. رابط الشيت بتاعك (تأكد إنه "Anyone with the link can edit")
# ملحوظة: لازم الرابط ينتهي بـ /export?format=csv عشان يشتغل صح
sheet_id = "حط_هنا_الـ_ID_بتاع_الملف_فقط" 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# 3. تهيئة البيانات (عشان لو الشيت لسه فاضي الموقع ميعلقش)
if 'temp_orders' not in st.session_state:
    st.session_state.temp_orders = []

# القائمة الجانبية
page = st.sidebar.radio("انتقل إلى:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة"])

# --- صفحة الزبائن ---
if page == "🛍️ متجر الزبائن":
    st.title("🛍️ SAWA Shop - اطلب الآن")
    with st.form("customer_form"):
        name = st.text_input("الاسم بالكامل")
        phone = st.text_input("رقم الموبايل")
        color = st.selectbox("اللون", ["أبيض", "أسود", "رمادي", "كحلي"])
        size = st.selectbox("المقاس", ["S", "M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية", min_value=1, value=1)
        submit = st.form_submit_button("إرسال الأوردر")

        if submit:
            if name and phone:
                # بنحفظ الأوردر في ذاكرة الموقع مؤقتاً لتفادي الايرور
                st.session_state.temp_orders.append({
                    "الاسم": name, "الموبايل": phone, "اللون": color, 
                    "المقاس": size, "الكمية": qty, "الحالة": "جديد"
                })
                st.success("تم استلام طلبك بنجاح!")
                st.info("سيتم مراجعة الطلب من قبل الإدارة فوراً.")
            else:
                st.warning("برجاء إكمال البيانات")

# --- صفحة الإدارة ---
else:
    st.title("📊 إدارة أوردرات SAWA Shop")
    
    if st.session_state.temp_orders:
        df = pd.DataFrame(st.session_state.temp_orders)
        st.subheader("📥 الطلبات الجديدة")
        edited_df = st.data_editor(df, use_container_width=True)
        
        # زرار "تنزيل" البيانات كملف إكسيل يدوي عشان تضمن إنها معاك
        csv = edited_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("تحميل الطلبات كملف Excel (CSV)", data=csv, file_name='sawa_orders.csv')
    else:
        st.info("لا توجد طلبات جديدة حالياً.")
