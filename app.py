import streamlit as st
import pandas as pd
from github import Github
import io
import datetime
import re  # مكتبة الفلترة الأمنية للنصوص
from PIL import Image # مكتبة التحقق من سلامة الصور

# 1. إعدادات الصفحة
st.set_page_config(page_title="SAWA Shop - Secured", layout="wide")

# الديكور وحماية الواجهة
premium_ui_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #070a13 0%, #0f0e26 50%, #1d072b 100%);
        color: #f1f5f9 !important;
    }
    h1 {
        color: #ffffff !important;
        text-align: center;
        background: linear-gradient(90deg, #ca8a04, #ec4899, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h2, h3, h4 { text-align: center; color: #e2e8f0 !important; }
    
    .whatsapp-btn button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        padding: 14px !important;
        box-shadow: 0 8px 20px rgba(56, 239, 125, 0.2) !important;
        width: 100%;
    }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
    }
</style>
"""
st.markdown(premium_ui_css, unsafe_allow_html=True)

# دالة فلترة النصوص وتأمينها ضد حيل الـ CSV Injection
def sanitize_text(text):
    if not isinstance(text, str):
        return str(text)
    # إزالة أي علامات بدء المعادلات لمنع الاختراق عبر ملفات الإكسل
    if text.startswith(('=', '+', '-', '@')):
        text = "'" + text
    # إزالة الرموز غير المرغوبة للحفاظ على نظافة السجل
    return re.sub(r'[<>"{};]', '', text)

# الاتصال بـ GitHub
@st.cache_resource
def get_github_repo():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        return g.get_repo(st.secrets["GITHUB_REPO"])
    except:
        return None

repo = get_github_repo()

def upload_to_github(file_bytes, file_path, commit_message):
    if repo is None: return False
    try:
        try:
            contents = repo.get_contents(file_path)
            repo.update_file(contents.path, commit_message, file_bytes, contents.sha)
        except:
            repo.create_file(file_path, commit_message, file_bytes)
        st.cache_data.clear()
        return True
    except:
        return False

@st.cache_data(ttl=5)
def load_orders_from_github():
    default_cols = ["الاسم", "الموبايل", "النوع", "اللون", "المقاس", "الكمية", "ملاحظات", "رابط_التصميم", "التاريخ"]
    if repo is None:
        return pd.DataFrame(columns=default_cols)
    try:
        contents = repo.get_contents("orders.csv")
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        if "نوع المنتج" in df.columns:
            df = df.rename(columns={"نوع المنتج": "النوع"})
        for col in default_cols:
            if col not in df.columns:
                df[col] = "غير محدد"
        return df
    except:
        return pd.DataFrame(columns=default_cols)

df_orders = load_orders_from_github()

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

# ==================== [ شاشة تسجيل الدخول ] ====================
if st.session_state["user_role"] is None:
    st.title("🛍️ نظام متجر SAWA SHOP")
    st.subheader("يرجى اختيار نوع الحساب للمتابعة")
    
    col_login1, col_login2 = st.columns(2)
    
    with col_login1:
        with st.form(key="customer_login_form"):
            st.markdown("### 👕 قسم المستخدم (الزبائن)")
            st.write("اضغط هنا للدخول لصفحة طلب وتصميم الملابس.")
            if st.form_submit_button("الدخول كـ مستخدم"):
                st.session_state["user_role"] = "customer"
                st.rerun()
        
    with col_login2:
        with st.form(key="admin_login_form"):
            st.markdown("### 🔐 لوحة الإدارة (المؤمنة)")
            st.write("خاص بمدير الموقع لمتابعة الطلبات.")
            admin_name = st.text_input("اسم المستخدم:")
            admin_pass = st.text_input("كلمة المرور:", type="password")
            if st.form_submit_button("تسجيل الدخول كـ أدمن"):
                # استدعاء البيانات بأمان من الـ Secrets السري
                sec_user = st.secrets.get("ADMIN_USERNAME", "admin")
                sec_pass = st.secrets.get("ADMIN_PASSWORD", "sawa2026")
                
                if admin_name == sec_user and admin_pass == sec_pass:
                    st.session_state["user_role"] = "admin"
                    st.rerun()
                else:
                    st.error("البيانات غير صحيحة.")

# ==================== [ صفحة المستخدم ] ====================
elif st.session_state["user_role"] == "customer":
    st.title("🛍️ متجر SAWA SHOP الإلكتروني")
    
    if st.sidebar.button("⬅️ تسجيل الخروج"):
        st.session_state["user_role"] = None
        st.rerun()
        
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسمك بالكامل:")
        phone = st.text_input("رقم الواتساب:")
        item_type = st.selectbox("نوع المنتج:", ["تيشيرت صيفي قطن", "هودي شتوي", "سويت شيرت"])
        color = st.selectbox("لون القماش:", ["أسود", "أبيض", "رمادي"])
        size = st.selectbox("المقاس:", ["M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية المطلوبة:", min_value=1, step=1)
        details = st.text_area("ملاحظات خاصة بالطباعة:")
    
    with col2:
        st.markdown("**📸 ارفع لوحة تصميمك هنا:**")
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="معاينة التصميم", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("إرسال وتأكيد الأوردر للمصنع 🚀"):
            if name and phone and uploaded_file:
                # 🛡️ الفحص الأمني الأول: التحقق أن الملف صورة حقيقية مش ملف خبيث متخفي
                try:
                    img = Image.open(uploaded_file)
                    img.verify() # التأكد من سلامة ملف الصورة داخلياً
                    is_valid_image = True
                except:
                    is_valid_image = False
                
                if not is_valid_image:
                    st.error("عذراً، الملف المرفوع تالف أو ليس صورة صالحة للطباعة!")
                else:
                    # 🛡️ الفحص الأمني الثاني: تنظيف المدخلات النصية من أي حقن معادلات ضار
                    clean_name = sanitize_text(name)
                    clean_phone = sanitize_text(phone)
                    clean_details = sanitize_text(details)
                    
                    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_file.name.split(".")[-1]
                    github_img_path = f"customer_designs/{time_str}_{clean_phone}.{file_extension}"
                    
                    with st.spinner("جاري الإرسال بأمان..."):
                        img_success = upload_to_github(uploaded_file.getvalue(), github_img_path, f"Upload design for {clean_name}")
                    
                    if img_success:
                        img_url = f"https://raw.githubusercontent.com/{st.secrets['GITHUB_REPO']}/main/{github_img_path}"
                        
                        new_row = {
                            "الاسم": clean_name, "الموبايل": clean_phone, "النوع": item_type, "اللون": color, 
                            "المقاس": size, "الكمية": qty, "ملاحظات": clean_details if clean_details else "لا يوجد", 
                            "رابط_التصميم": img_url, "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        
                        df_updated = pd.concat([df_orders, pd.DataFrame([new_row])], ignore_index=True)
                        csv_buffer = io.StringIO()
                        df_updated.to_csv(csv_buffer, index=False)
                        upload_to_github(csv_buffer.getvalue().encode('utf-8'), "orders.csv", f"Add order for {clean_name}")
                        
                        st.success("تم إرسال أوردرك وتصميمك بنجاح وبأمان كامل! 🎉")
                        st.balloons()
            else:
                st.error("برجاء ملء البيانات ورفع التصميم أولاً!")

    with btn_col2:
        st.markdown('<div class="whatsapp-btn">', unsafe_allow_html=True)
        whatsapp_url = f"https://wa.me/201149243249?text=مرحباً%20SAWA%20Shop،%20أريد%20الاستفسار%20عن%20تفاصيل%20الطباعة"
        if st.button("💬 تواصل معنا عبر الواتساب"):
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{whatsapp_url}\'" />', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== [ صفحة الإدارة / الداش بورد ] ====================
elif st.session_state["user_role"] == "admin":
    st.title("📊 داش بورد إدارة SAWA SHOP")
    
    if st.sidebar.button("⬅️ تسجيل الخروج"):
        st.session_state["user_role"] = None
        st.rerun()
        
    st.divider()
    
    if not df_orders.empty:
        df_orders['الكمية'] = pd.to_numeric(df_orders['الكمية'], errors='coerce').fillna(1)
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="📈 إجمالي الأوردرات المستلمة", value=f"{len(df_orders)} أوردر")
        with stat_col2:
            st.metric(label="👕 إجمالي القطع المطلوبة", value=f"{int(df_orders['الكمية'].sum())} قطعة")
            
        st.divider()
        
        st.markdown("### 📊 تحليل المبيعات والألوان")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎨 الألوان الأكثر طلباً:")
            color_counts = df_orders.groupby('اللون')['الكمية'].sum()
            st.bar_chart(color_counts)
            
        with chart_col2:
            st.markdown("#### 👕 المنتجات الأكثر مبيعاً:")
            type_counts = df_orders.groupby('النوع')['الكمية'].sum()
            st.bar_chart(type_counts)
            
        st.divider()
        
        st.markdown("#### 📄 السجل التفصيلي للطلبات:")
        st.dataframe(df_orders, use_container_width=True)
        st.divider()
        
        st.markdown("### 🖼️ تصاميم العملاء الجاهزة للتنزيل والطباعة")
        for idx, row in df_orders.iterrows():
            with st.container():
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    st.write(f"👤 **العميل:** {row['الاسم']} | 📞 **الموبايل:** {row['الموبايل']}")
                    st.write(f"👕 **الطلب:** {row['النوع']} | {row['اللون']} | مقاس {row['المقاس']} | عدد {row['الكمية']} قطع")
                    st.write(f"📝 **ملاحظات:** {row['ملاحظات']}")
                    st.write(f"📅 **التاريخ:** {row['التاريخ']}")
                    st.markdown(f"[📥 تحميل الصورة بجودة عالية للماكينة]({row['رابط_التصميم']})")
                with col_img:
                    st.image(row['رابط_التصميم'], width=150)
                st.divider()
    else:
        st.info("لا توجد أوردرات مسجلة حتى الآن.")
