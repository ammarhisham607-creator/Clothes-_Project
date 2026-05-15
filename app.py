import streamlit as st
import pandas as pd
from github import Github
from PIL import Image
import io
import datetime

# 1. إعدادات الصفحة واسم المتجر في محرك البحث
st.set_page_config(page_title="SAWA Shop - متجر ملابس وتصاميم مطبوعة", layout="wide")

# 2. كود التحقق التلقائي الخاص بجوجل (SEO)
if "GOOGLE_VERIFICATION" in st.secrets:
    st.markdown(st.secrets["GOOGLE_VERIFICATION"], unsafe_allow_html=True)

# 3. الاتصال بـ GitHub بأمان عبر الـ Secrets
try:
    g = Github(st.secrets["GITHUB_TOKEN"])
    repo = g.get_repo(st.secrets["GITHUB_REPO"])
except Exception as e:
    st.error("تنبيه للإدارة: هناك مشكلة في مفاتيح اتصال GitHub في الـ Secrets!")

# دالة مخصصة لرفع الملفات والصور إلى مستودع GitHub
def upload_to_github(file_bytes, file_path, commit_message):
    try:
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(contents.path, commit_message, file_bytes, contents.sha)
        except:
            repo.create_file(file_path, commit_message, file_bytes)
        return True
    except Exception as e:
        st.error(f"خطأ أثناء الحفظ على جيت هاب: {e}")
        return False

# دالة لقراءة سجل الأوردرات الحالي من GitHub
def load_orders_from_github():
    try:
        contents = repo.get_contents("orders.csv")
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        return df
    except:
        return pd.DataFrame(columns=["الاسم", "الموبايل", "اللون", "المقاس", "الكمية", "رابط_التصميم", "التاريخ"])

# --- واجهة موقع SAWA Shop --- [cite: user_summary]
st.title("🛍️ متجر SAWA Shop الإلكتروني") 
st.subheader("تصاميم ملابس مخصصة وعصرية") 
st.divider()

# القائمة الجانبية للتنقل
page = st.sidebar.radio("انتقل إلى:", ["متجر الزبائن (طلب أوردر)", "لوحة الإدارة (خاص بعمار)"])

# --- القسم الأول: متجر الزبائن ---
if page == "متجر الزبائن (طلب أوردر)":
    st.markdown("### 👕 صمم تيشيرتك بنفسك واطلب الآن")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسمك الكريم بالكامل:")
        phone = st.text_input("رقم الواتساب (للتواصل وتأكيد الأوردر):")
        color = st.selectbox("اختر لون التيشيرت:", ["أسود", "أبيض", "رمادي"]) [cite: user_summary]
        size = st.selectbox("اختر المقاس المناسب:", ["M", "L", "XL", "XXL"]) [cite: user_summary]
        qty = st.number_input("الكمية المطلوبة:", min_value=1, step=1)
    
    with col2:
        uploaded_file = st.file_uploader("ارفع التصميم أو الصورة المراد طباعتها هنا:", type=["png", "jpg", "jpeg"]) [cite: user_summary]
        if uploaded_file is not None:
            st.image(uploaded_file, caption="معاينة التصميم المرفوع", width=250)

    st.markdown("---")
    if st.button("إرسال وتأكيد الأوردر للمصنع 🚀"):
        if name and phone and uploaded_file:
            time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = uploaded_file.name.split(".")[-1]
            github_img_path = f"customer_designs/{time_str}_{phone}.{file_extension}"
            
            with st.spinner("جاري حفظ وتأمين تصميمك أونلاين..."):
                img_success = upload_to_github(uploaded_file.getvalue(), github_img_path, f"Upload design for {name}")
            
            if img_success:
                df_orders = load_orders_from_github()
                img_url = f"https://raw.githubusercontent.com/{st.secrets['GITHUB_REPO']}/main/{github_img_path}"
                
                new_row = {
                    "الاسم": name, "الموبايل": phone, "اللون": color, 
                    "المقاس": size, "الكمية": qty, "رابط_التصميم": img_url,
                    "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                df_orders = pd.concat([df_orders, pd.DataFrame([new_row])], ignore_index=True)
                
                csv_buffer = io.StringIO()
                df_orders.to_csv(csv_buffer, index=False)
                upload_to_github(csv_buffer.getvalue().encode('utf-8'), "orders.csv", f"Add order for {name}")
                
                st.success("يا فنان، أوردرك وتصميمك وصلوا لنا بنجاح! هنتواصل معاك على الواتساب فوراً. 🎉")
                st.balloons()
        else:
            st.error("من فضلك، تأكد من كتابة الاسم ورقم الموبايل ورفع صورة التصميم أولاً!")

# --- القسم الثاني: لوحة الإدارة ---
else:
    st.markdown("### 📊 لوحة تحكم وإدارة طلبات SAWA Shop") [cite: user_summary]
    df_orders = load_orders_from_github()
    
    if not df_orders.empty:
        st.dataframe(df_orders, use_container_width=True)
        st.divider()
        st.markdown("### 🖼️ استعراض وتحميل تصاميم الزبائن للأوردرات")
        
        for idx, row in df_orders.iterrows():
            with st.container():
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    st.write(f"👤 **العميل:** {row['الاسم']}")
                    st.write(f"📞 **واتساب:** {row['الموبايل']}")
                    st.write(f"🎨 **المواصفات:** لون {row['اللون']} | مقاس {row['المقاس']} | عدد {row['الكمية']} قطع")
                    st.write(f"📅 **التاريخ:** {row['التاريخ']}")
                    st.markdown(f"[📥 تحميل الصورة الأصلية بجودة عالية]({row['رابط_التصميم']})")
                with col_img:
                    st.image(row['رابط_التصميم'], width=180)
                st.divider()
    else:
        st.info("لا توجد أوردرات مسجلة في قاعدة البيانات حتى الآن.")
