import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop Portal", page_icon="👕", layout="wide")

# 2. ربط جوجل شيت (ضع رابط ملفك هنا)
url = "رابط_ملف_الإكسيل_هنا"
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. القائمة الجانبية
page = st.sidebar.radio("انتقل إلى:", ["🛍️ متجر الزبائن", "⚙️ لوحة الإدارة (داتا حقيقية)"])

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
                # قراءة البيانات الحالية
                existing_data = conn.read(spreadsheet=url)
                # إضافة الأوردر الجديد
                new_order = pd.DataFrame([{"الاسم": name, "الموبايل": phone, "اللون": color, "المقاس": size, "الكمية": qty, "الحالة": "جديد"}])
                updated_df = pd.concat([existing_data, new_order], ignore_index=True)
                # تحديث الشيت
                conn.update(spreadsheet=url, data=updated_df)
                st.success("تم تسجيل طلبك وحفظه في الإكسيل بنجاح!")
            else:
                st.warning("برجاء إكمال البيانات")

# --- صفحة الإدارة ---
else:
    st.title("📊 إدارة أوردرات SAWA Shop (Google Sheets)")
    
    # قراءة البيانات مباشرة من الشيت
    df = conn.read(spreadsheet=url)
    
    if not df.empty:
        st.write("جميع الطلبات المحفوظة في الإكسيل:")
        # محرر بيانات تفاعلي (أي تعديل هنا وتدوس حفظ هيسمع في الإكسيل)
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
        
        if st.button("حفظ التعديلات في الإكسيل"):
            conn.update(spreadsheet=url, data=edited_df)
            st.success("تم تحديث ملف الإكسيل بنجاح!")
    else:
        st.info("لا توجد بيانات في ملف الإكسيل حالياً.")
