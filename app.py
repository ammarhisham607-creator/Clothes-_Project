import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات واجهة الموقع
st.set_page_config(page_title="متجر عمار أوكا - إدارة الملابس", layout="wide")

# تصميم بسيط بالـ CSS لتحسين المظهر
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_index=True)

st.title("👕 نظام إدارة مبيعات الملابس (عمار أوكا)")
st.write(f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")

# --- الجزء الجانبي: إدخال التكاليف والمخزن ---
st.sidebar.header("📦 إعدادات المخزن والتكاليف")
cost_plain = st.sidebar.number_input("سعر التيشرت السادة (من المصنع)", min_value=0.0, value=150.0, step=5.0)
cost_printing = st.sidebar.number_input("تكلفة الطباعة والخامات", min_value=0.0, value=50.0, step=5.0)
initial_stock = st.sidebar.number_input("الكمية المتوفرة حالياً بالسوق", min_value=0, value=50)
alert_limit = st.sidebar.slider("حد تنبيه النواقص", 1, 20, 5)

# --- الجزء الرئيسي: تسجيل الأوردر ---
st.header("🛒 تسجيل أوردر جديد")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        customer_name = st.text_input("اسم الزبون")
    with col2:
        selling_price = st.number_input("سعر البيع للزبون", min_value=0.0, value=300.0, step=10.0)
    with col3:
        quantity_sold = st.number_input("عدد القطع في الأوردر", min_value=1, value=1)

    design_file = st.file_uploader("ارفع صورة التصميم المطلوبة", type=['png', 'jpg', 'jpeg'])

# --- الحسابات المنطقية ---
total_cost_per_piece = cost_plain + cost_printing
profit_per_piece = selling_price - total_cost_per_piece
total_profit = profit_per_piece * quantity_sold
remaining_stock = initial_stock - quantity_sold

# --- عرض النتائج والتقارير ---
st.markdown("---")
st.subheader("📊 ملخص الأرباح والمخزن")
m1, m2, m3 = st.columns(3)

m1.metric("صافي الربح الإجمالي", f"{total_profit} ج.م", f"{profit_per_piece} للقطعة")
m2.metric("التكلفة الإجمالية للقطع", f"{total_cost_per_piece * quantity_sold} ج.م")
m3.metric("المخزون المتبقي", f"{remaining_stock} قطعة")

# نظام التنبيه الذكي للمخزن
if remaining_stock <= alert_limit:
    st.error(f"🚨 تنبيه هام: المخزون وصل لـ {remaining_stock} قطع. اطلب من المصنع فوراً!")
elif remaining_stock <= alert_limit + 5:
    st.warning("⚠️ ملاحظة: المخزون بدأ يقل، جهز الطلبية الجاية.")

# زر حفظ البيانات (للعرض فقط في هذه النسخة)
if st.button("حفظ وإتمام الأوردر"):
    if customer_name:
        st.success(f"تم حفظ أوردر الزبون ({customer_name}) بنجاح!")
        if design_file:
            st.image(design_file, caption=f"تصميم أوردر {customer_name}", width=300)
    else:
        st.error("من فضلك ادخل اسم الزبون أولاً.")
