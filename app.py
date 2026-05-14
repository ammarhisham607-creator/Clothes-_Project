import streamlit as st

# 1. إعدادات المتصفح ومحركات البحث
st.set_page_config(
    page_title="SAWA Shop - Clothing Management",
    page_icon="👕",
    layout="wide"
)

# 2. واجهة الموقع الرئيسية
st.title("👕 SAWA Shop Dashboard")
st.subheader("نظام إدارة مبيعات الملابس")

# 3. القائمة الجانبية (Sidebar)
st.sidebar.header("📦 Inventory Settings")
cost_plain = st.sidebar.number_input("سعر التيشرت السادة", min_value=0.0, value=150.0)
cost_printing = st.sidebar.number_input("تكلفة الطباعة", min_value=0.0, value=50.0)
initial_stock = st.sidebar.number_input("الكمية المتوفرة", min_value=0, value=50)
alert_limit = st.sidebar.slider("تنبيه النواقص", 1, 20, 5)

# 4. تسجيل الطلبات (Orders)
st.header("🛒 Create New Order")
col1, col2, col3 = st.columns(3)

with col1:
    customer_name = st.text_input("اسم الزبون")
with col2:
    selling_price = st.number_input("سعر البيع", min_value=0.0, value=300.0)
with col3:
    quantity_sold = st.number_input("الكمية", min_value=1, value=1)

design_file = st.file_uploader("ارفع صورة التصميم", type=['png', 'jpg', 'jpeg'])

# 5. الحسابات التلقائية
total_cost_per_piece = cost_plain + cost_printing
profit_per_piece = selling_price - total_cost_per_piece
total_profit = profit_per_piece * quantity_sold
remaining_stock = initial_stock - quantity_sold

# 6. عرض النتائج والتقارير
st.divider()
st.subheader("📊 Profit & Stock Summary")

m1, m2, m3 = st.columns(3)
m1.metric("Net Profit (صافي الربح)", f"{total_profit} EGP")
m2.metric("Total Cost (التكلفة)", f"{total_cost_per_piece * quantity_sold} EGP")
m3.metric("Remaining Stock (المخزن)", f"{remaining_stock} pcs")

# نظام التنبيهات
if remaining_stock <= alert_limit:
    st.error(f"🚨 Warning: Stock is low! ({remaining_stock} pcs left)")

# زر الحفظ
if st.button("Save Order"):
    if customer_name:
        st.success(f"Order for {customer_name} has been saved to SAWA Shop system!")
        if design_file:
            st.image(design_file, caption=f"Design for {customer_name}", width=300)
    else:
        st.warning("Please enter customer name")
