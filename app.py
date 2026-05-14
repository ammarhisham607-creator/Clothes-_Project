import streamlit as st

# 1. إعدادات الصفحة والهوية الجديدة
st.set_page_config(page_title="SAWA Shop", page_icon="👕", layout="wide")

# القائمة الجانبية للتنقل بين الصفحات
page = st.sidebar.selectbox("اختار الصفحة", ["متجر الزبائن (SAWA Shop)", "لوحة تحكم الإدارة"])

# --- الصفحة الأولى: متجر الزبائن ---
if page == "متجر الزبائن (SAWA Shop)":
    st.title("🛍️ SAWA Shop - اطلب تيشيرتك الآن")
    st.write("صمم تيشيرتك المفضل بخطوات بسيطة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        color = st.selectbox("اختار لون التيشيرت", ["أبيض", "أسود", "رمادي", "كحلي"])
        size = st.select_slider("اختار المقاس", options=["S", "M", "L", "XL", "XXL"])
        design = st.file_uploader("ارفع الصورة اللي عايز تطبعها", type=['png', 'jpg', 'jpeg'])
        
    with col2:
        customer_name = st.text_input("اسمك بالكامل")
        phone_number = st.text_input("رقم الموبايل (واتساب)")
        notes = st.text_area("أي ملاحظات إضافية؟")

    if st.button("إرسال الأوردر"):
        if customer_name and phone_number and design:
            st.success(f"شكراً يا {customer_name}! تم استلام طلبك.")
            st.balloons()
            
            # زر إرسال للواتساب (تعديل رقمك هنا)
            whatsapp_msg = f"أوردر جديد من SAWA Shop:%0Aالاسم: {customer_name}%0Aاللون: {color}%0Aالمقاس: {size}%0Aالموبايل: {phone_number}"
            # استبدل 201000000000 برقمك الحقيقي يبدأ بكود الدولة
            wa_url = f"https://wa.me/201234567890?text={whatsapp_msg}" 
            st.markdown(f'[اضغط هنا لتأكيد الأوردر عبر واتساب]({wa_url})')
        else:
            st.warning("من فضلك كمل البيانات وارفع التصميم")

# --- الصفحة الثانية: لوحة الإدارة (نفس الكود السابق) ---
else:
    st.title("📊 SAWA Shop Dashboard (Management)")
    
    st.sidebar.header("📦 Inventory Settings")
    cost_plain = st.sidebar.number_input("سعر التيشرت السادة", min_value=0.0, value=150.0)
    cost_printing = st.sidebar.number_input("تكلفة الطباعة", min_value=0.0, value=50.0)
    initial_stock = st.sidebar.number_input("الكمية المتوفرة", min_value=0, value=50)
    
    st.header("🛒 تسجيل أوردر داخلي")
    # باقي حساباتك القديمة هنا..
    selling_price = st.number_input("سعر البيع", min_value=0.0, value=300.0)
    quantity = st.number_input("الكمية", min_value=1, value=1)
    
    profit = (selling_price - (cost_plain + cost_printing)) * quantity
    st.metric("صافي الربح المتوقع", f"{profit} EGP")
