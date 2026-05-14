import streamlit as st 
import pandas as pd
from datetime import datetime

#اعدادات واجهة الموقع
st.set_page_config(page _title="ادارة الملابس-SAWA Shop", layout="wide")
# لتحسين المظهر CSS تصميم بسيط ب ال
st.markdown(f"""
<style>
.main { background-color:#f5f7f9; }
.stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box.shadow: 0 2px 4px rgba(0,0,0,0.05)}
</style>
""", unsafe_index=True)
st.title("(SAWA Shop)نظام ادارة مبيعات الملابس")
st.write(f"14/5/2026: {datetime.now().strftime('%Y-%m-%d')}")
# --- الجزء الجانبى: ادخال التكاليف والمخزن---
st.sidebar.header("اعدادات المخزن والتكاليف")
cost_plain = st.sidebar.number_input("سعر التيشيرت سادة (من المصنع)", min_value=0.0; value=150.0, step=5.0)
cost_printing = st.sidebar.number_input("تكلفة الطباعة والخامات ", min_value=0.0; value=50.0, step=5.0)
initial_stock = st.sidebar.number_input("الكمية المتوفرة حاليا بالسوق", min_value=0, value=50)
alert_limit = st.sidebar.slider("5 ,20 ,1"حد تنبيه النواقص)
# --- الجزء الرئيسى: تسجيل الاوردر---
st.header("تسجيل أوردر جديد")
with st.container():
    col1, col2, col3, = st.columns(3)
    with col1:
        customer_name = st.text_input("اسم الزبون")
        with col2:
            selling_price = st.number_input("سعر البيع للزبون", min_value=0.0, value=300.0, step=10.0)
            with col3:
                quantity_sold = st.number_input("عدد القطع المطلوبة", min_value=1, value=1) 
                design_file = st.file_uploader("ارفع صورة التصميم المطلوبة",type=['png', 'jpg', 'jpeg'])

 #--- الحسابات المنطقية---
 total_cost_per_piece = cost_plain + cost_printing
 profit_perpiece = selling_price - total_cost_per_piece
 total_profit = profit_per_piece * quantity_sold
 remaining_stock = initial_stock - quantity_sold

 # --- عرض التقارير والنتائج---
 st.markdown("---")
 st.subheader("ملخص الأرباح والمخزن")
 m1, m2, m3 = st.columns(3)

m1.metric("صافى الربح الاجمالى", f"{total_profit}ج.م.", f"{ profit_per_piece}للقطعة")
m2.metric("التكلفة الاجمالية للقطع", f"{total_cost_per_piece * quantity_sold}ج.م.")
m3.metric("المخزون المتبقى", f"{remaining_stock}القطعة")

#--- نظام التنبيه الذكى---
if remaining_stock <=alert_limit:
    st.error(f" تنبيه هام : المخزون وصل ل5 قطع اطلب من المصنع فورا{remaining_stock}")
elif remaining_stock <= alert_limit +5:
    st.warning("ملاحظة: المخزون بدأ يقل جهز الطلبية الجاية")

# زر حفظ البيانات (للعرض فقط فى هذه النسخة)
if st.button("حفظ واتمام الأوردر"):
    if customer_name:
        st.success(f" تم حفظ أوردر الزبون بنجاح!({customer_name})")
if design_file:
    st.image(design_file, caption=f"{customer_name}",width=300)
else:
    st.error("من فضلك أدخل اسم الزبون أولا.")