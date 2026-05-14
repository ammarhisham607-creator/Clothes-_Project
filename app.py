import streamlit as st

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="ادارة الملابس-SAWA Shop", layout="wide")

st.title("👕 نظام إدارة مبيعات الملابس (SAWA Shop)")
st.write("مرحباً بك في لوحة تحكم متجرك")

# 2. القائمة الجانبية لإدخال التكاليف
st.sidebar.header("📦 إعدادات المخزن والتكاليف")
cost_plain = st.sidebar.number_input("سعر التيشرت السادة (من المصنع)", min_value=0.0, value=150.0)
cost_printing = st.sidebar.number_input("تكلفة الطباعة", min_value=0.0, value=50.0)
initial_stock = st.sidebar.number_input("الكمية المتوفرة حالياً", min_value=0, value=50)
alert_limit = st.sidebar.slider("حد تنبيه النواقص", 1, 20, 5)

# 3. خانات تسجيل الأوردر الجديد
st.header("🛒 تسجيل أوردر جديد")
col1, col2, col3 = st.columns(3)

with col1:
    customer_name = st.text_input("اسم الزبون")
with col2:
    selling_price = st.number_input("سعر البيع للزبون", min_value=0.0, value=300.0)
with col3:
    quantity_sold = st.number_input("عدد القطع في الأوردر", min_value=1, value=1)

design_file = st.file_uploader("ارفع صورة التصميم (اختياري)", type=['png', 'jpg', 'jpeg'])

# 4. العمليات الحسابية (تأكد أنها تبدأ من أول السطر تماماً)
total_cost_per_piece = cost_plain + cost_printing
profit_per_piece = selling_price - total_cost_per_piece
total_profit = profit_per_piece * quantity_sold
remaining_stock = initial_stock - quantity_sold

# 5. عرض النتائج النهائية
st.markdown("---")
st.subheader("📊 ملخص الأرباح والمخزن")

m1, m2, m3 = st.columns(3)
m1.metric("صافي الربح الإجمالي", f"{total_profit} ج.م")
m2.metric("التكلفة الإجمالية", f"{total_cost_per_piece * quantity_sold} ج.م")
m3.metric("المخزون المتبقي", f"{remaining_stock} قطعة")

# عرض التنبيهات لو المخزن نقص
if remaining_stock <= alert_limit:
    st.error(f"🚨 تنبيه: المخزون وصل لـ {remaining_stock} قطع. اطلب من المصنع!")

# زر الحفظ وعرض صورة التصميم
if st.button("حفظ الأوردر"):
    if customer_name:
        st.success(f"تم تسجيل أوردر الزبون: {customer_name}")
        if design_file:
            st.image(design_file, caption="تصميم الأوردر", width=300)
    else:
        st.warning("من فضلك اكتب اسم الزبون")
