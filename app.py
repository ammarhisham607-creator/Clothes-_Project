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
@st.cache_resource
def get_github_repo():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        return g.get_repo(st.secrets["GITHUB_REPO"])
    except Exception as e:
        st.error("تنبيه للإدارة: هناك مشكلة في مفاتيح اتصال GitHub في الـ Secrets!")
        return None

repo = get_github_repo()

# دالة مخصصة لرفع الملفات والصور إلى مستودع GitHub
def upload_to_github(file_bytes, file_path, commit_message):
    if repo is None:
        return False
    try:
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(contents.path, commit_message, file_bytes, contents.sha)
        except:
            repo.create_file(file_path, commit_message, file_bytes)
        # بنمسح الكاش عشان الإدارة تشوف الأوردر الجديد فوراً
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"خطأ أثناء الحفظ على جيت هاب: {e}")
        return False

# دالة ذكية لقراءة سجل الأوردرات الحالي من GitHub (تمنع الريفريش المتكرر وتوفر النت)
@st.cache_data(ttl=60)  # بتعمل كاش وتحدث نفسها كل دقيقة بس أو لو فيه أوردر جديد
def load_orders_from_github():
    if repo is None:
        return pd.DataFrame(columns=["الاسم", "الموبايل", "النوع", "اللون", "المقاس", "الكمية", "ملاحظات", "رابط_التصميم", "التاريخ"])
    try:
        contents = repo.get_contents("orders.csv")
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        return df
    except:
        return pd.DataFrame(columns=["الاسم", "الموبايل", "النوع", "اللون", "المقاس", "الكمية", "ملاحظات", "رابط_التصميم", "التاريخ"])

# تحميل البيانات الأساسية
df_orders = load_orders_from_github()

# --- واجهة نظام الحماية وفصل الصفحات باستخدام Session State لمنع الريفريش المفاجئ ---
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# الواجهة الرئيسية للموقع (تفتح دائماً على متجر الزبائن)
if not st.session_state["admin_logged_in"]:
    st.title("🛍️ متجر SAWA Shop الإلكتروني")
    st.subheader("نفذ تصميمك الخاص على أجود أنواع الملابس")
    st.divider()
    
    st.markdown("### 👕 صمم قطعتك المفضلة واطلب الآن")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسمك الكريم بالكامل:", key="cust_name")
        phone = st.text_input("رقم الواتساب (للتواصل وتأكيد الأوردر):", key="cust_phone")
        
        item_type = st.selectbox("اختر نوع المنتج:", ["تيشيرت صيفي قطن", "هودي شتوي", "سويت شيرت"], key="cust_item")
        color = st.selectbox("اختر لون القماش:", ["أسود", "أبيض", "رمادي"], key="cust_color")
        size = st.selectbox("اختر المقاس المناسب:", ["M", "L", "XL", "XXL"], key="cust_size")
        qty = st.number_input("الكمية المطلوبة:", min_value=1, step=1, key="cust_qty")
        
        details = st.text_area("تفاصيل أو ملاحظات خاصة بالتصميم (مكان الطباعة، تعديل معين):", placeholder="مثال: عايز الطباعة تكون كبيرة في الظهر..", key="cust_details")
    
    with col2:
        uploaded_file = st.file_uploader("ارفع التصميم أو الصورة المراد طباعتها هنا:", type=["png", "jpg", "jpeg"], key="cust_file")
        if uploaded_file is not None:
            st.image(uploaded_file, caption="معاينة التصميم المرفوع", width=250)

    st.markdown("---")
    if st.button("إرسال وتأكيد الأوردر 🚀"):
        if name and phone and uploaded_file:
            time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = uploaded_file.name.split(".")[-1]
            github_img_path = f"customer_designs/{time_str}_{phone}.{file_extension}"
            
            with st.spinner("جاري حفظ وتأمين تصميمك أونلاين..."):
                img_success = upload_to_github(uploaded_file.getvalue(), github_img_path, f"Upload design for {name}")
            
            if img_success:
                img_url = f"https://raw.githubusercontent.com/{st.secrets['GITHUB_REPO']}/main/{github_img_path}"
                
                new_row = {
                    "الاسم": name, "الموبايل": phone, "النوع": item_type, "اللون": color, 
                    "المقاس": size, "الكمية": qty, "ملاحظات": details if details else "لا يوجد", 
                    "رابط_التصميم": img_url, "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                # تحديث الجدول
                df_updated = pd.concat([df_orders, pd.DataFrame([new_row])], ignore_index=True)
                
                csv_buffer = io.StringIO()
                df_updated.to_csv(csv_buffer, index=False)
                upload_to_github(csv_buffer.getvalue().encode('utf-8'), "orders.csv", f"Add order for {name}")
                
                st.success("يا فنان، أوردرك وتصميمك وصلوا لعمار بنجاح! هنتواصل معاك على الواتساب فوراً. 🎉")
                st.balloons()
        else:
            st.error("من فضلك، تأكد من كتابة الاسم ورقم الموبايل ورفع صورة التصميم أولاً!")

    # --- بوابتك السرية للدخول كأدمن ---
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    with st.expander("🔐 تسجيل دخول الإدارة"):
        password = st.text_input("أدخل كلمة السر الخاصة بعمار للوصول للوحة التحكم:", type="password", key="admin_password")
        if st.button("دخول"):
            if password == "sawa2026":
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("كلمة السر خاطئة يا صاحبي!")

# --- لوحة التحكم (لا تفتح إلا بالباسورد الصحيح ومحمية من الريفريش) ---
else:
    st.title("📊 لوحة تحكم وإدارة طلبات SAWA Shop")
    st.subheader("مرحباً بك يا فنان في لوحة التحكم الخاصة بك")
    
    if st.button("⬅️ خروج والعودة لمتجر الزبائن"):
        st.session_state["admin_logged_in"] = False
        st.rerun()
        
    st.divider()
    
    if not df_orders.empty:
        total_orders = len(df_orders)
        total_pieces = pd.to_numeric(df_orders['الكمية']).sum()
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="📈 إجمالي عدد الطلبات المستلمة", value=f"{total_orders} أوردر")
        with stat_col2:
            st.metric(label="👕 إجمالي عدد القطع المطلوب طباعتها", value=f"{total_pieces} قطعة")
            
        st.markdown("#### 📄 جدول تفاصيل الطلبات:")
        st.dataframe(df_orders, use_container_width=True)
        st.divider()
        
        st.markdown("### 🖼️ استعراض وتحميل تصاميم الزبائن للأوردرات")
        for idx, row in df_orders.iterrows():
            with st.container():
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    st.write(f"👤 **العميل:** {row['الاسم']}")
                    st.write(f"📞 **واتساب:** {row['الموبايل']}")
                    st.write(f"🏷️ **النوع:** {row.get('النوع', 'تيشيرت')}")
                    st.write(f"🎨 **المواصفات:** لون {row['اللون']} | مقاس {row['المقاس']} | عدد {row['الكمية']} قطع")
                    st.write(f"📝 **ملاحظات العميل:** {row.get('ملاحظات', 'لا يوجد')}")
                    st.write(f"📅 **التاريخ:** {row['التاريخ']}")
                    st.markdown(f"[📥 تحميل الصورة الأصلية بجودة عالية]({row['رابط_التصميم']})")
                with col_img:
                    st.image(row['رابط_التصميم'], width=180)
                st.divider()
    else:
        st.info("لا توجد أوردرات مسجلة في قاعدة البيانات حتى الآن.")
