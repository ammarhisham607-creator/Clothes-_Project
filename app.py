import streamlit as st
import pandas as pd
from github import Github
from PIL import Image
import io
import datetime

# إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop", layout="wide")

# الاتصال بـ GitHub
try:
    g = Github(st.secrets["GITHUB_TOKEN"])
    repo = g.get_repo(st.secrets["GITHUB_REPO"])
except:
    st.error("فيه مشكلة في مفاتيح اتصال GitHub في الـ Secrets!")

# دالة لرفع الملفات لـ GitHub
def upload_to_github(file_bytes, file_path, commit_message):
    try:
        # لو الملف موجود قبل كده بنحدثه، لو مش موجود بنعمله جديد
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(contents.path, commit_message, file_bytes, contents.sha)
        except:
            repo.create_file(file_path, commit_message, file_bytes)
        return True
    except Exception as e:
        st.error(f"خطأ أثناء الحفظ على جيت هاب: {e}")
        return False

# دالة لقراءة الأوردرات من GitHub
def load_orders_from_github():
    try:
        contents = repo.get_contents("orders.csv")
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        return df
    except:
        # لو الملف مش موجود نرجع جدول فاضي بالعامدة اللي محتاجينها
        return pd.DataFrame(columns=["الاسم", "الموبايل", "اللون", "المقاس", "الكمية", "رابط_التصميم", "التاريخ"])

# --- صفحة الزبائن ---
st.title("🛍️ متجر SAWA Shop")
page = sidebar_entry = st.sidebar.radio("القائمة", ["متجر الزبائن", "لوحة الإدارة"])

if page == "متجر الزبائن":
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("الاسم بالكامل")
        phone = st.text_input("رقم الواتساب")
        color = st.selectbox("اللون", ["أسود", "أبيض", "رمادي"])
        size = st.selectbox("المقاس", ["M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية", min_value=1, step=1)
    
    with col2:
        uploaded_file = st.file_uploader("ارفع تصميمك هنا (صورة)", type=["png", "jpg", "jpeg"])
    
    if st.button("تأكيد الأوردر 🚀"):
        if name and phone and uploaded_file:
            time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = uploaded_file.name.split(".")[-1]
            github_img_path = f"customer_designs/{time_str}_{phone}.{file_extension}"
            
            # 1. ارفع الصورة على جيت هاب
            with st.spinner("جاري رفع التصميم..."):
                img_success = upload_to_github(uploaded_file.getvalue(), github_img_path, f"Upload design for {name}")
            
            if img_success:
                # 2. سجل الأوردر في ملف الـ CSV
                df_orders = load_orders_from_github()
                img_url = f"https://raw.githubusercontent.com/{st.secrets['GITHUB_REPO']}/main/{github_img_path}"
                
                new_row = {
                    "الاسم": name, "الموبايل": phone, "اللون": color, 
                    "المقاس": size, "الكمية": qty, "رابط_التصميم": img_url,
                    "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                df_orders = pd.concat([df_orders, pd.DataFrame([new_row])], ignore_index=True)
                
                # حفظ الملف المحدث على جيت هاب
                csv_buffer = io.StringIO()
                df_orders.to_csv(csv_buffer, index=False)
                upload_to_github(csv_buffer.getvalue().encode('utf-8'), "orders.csv", f"Add order for {name}")
                
                st.success("تم تسجيل أوردرك بنجاح وحفظه!")
                st.balloons()
        else:
            st.error("برجاء كتابة البيانات ورفع الصورة أولاً!")

# --- صفحة الإدارة ---
else:
    st.header("📊 لوحة إدارة الطلبات")
    df_orders = load_orders_from_github()
    
    if not df_orders.empty:
        st.dataframe(df_orders, use_container_width=True)
        
        st.subheader("🖼️ استعراض تصاميم الزبائن للأوردرات")
        for idx, row in df_orders.iterrows():
            st.write(f"**الزبون:** {row['الاسم']} | **موبايل:** {row['الموبايل']}")
            st.image(row['رابط_التصميم'], width=200)
            st.markdown(f"[فتح الصورة بحجمها الأصلي]({row['رابط_التصميم']})")
            st.divider()
    else:
        st.info("لا توجد أوردرات مسجلة حتى الآن.")
