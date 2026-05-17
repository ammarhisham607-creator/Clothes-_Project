import streamlit as st
import pandas as pd
from github import Github
import io
import datetime
import re
from PIL import Image

# ==================== [ 1. إعدادات الصفحة ] ====================
st.set_page_config(page_title="SAWA Shop", layout="wide")

# ==================== [ 2. الديكور النيون والبرق (CSS) ] ====================
premium_ui_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #020205 0%, #080711 40%, #12021c 100%) !important;
        font-family: 'Cairo', sans-serif !important;
        color: #f8fafc !important;
    }

    h1 {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700 !important;
        text-align: center;
        color: #fff !important;
        text-shadow: 0 0 7px #fff, 0 0 10px #fff, 0 0 21px #a855f7, 0 0 42px #a855f7, 0 0 82px #a855f7;
        animation: blink 2s infinite alternate;
        margin-bottom: 20px !important;
    }

    @keyframes blink {
        0%, 18%, 22%, 25%, 53%, 57%, 100% {
            text-shadow: 0 0 4px #fff, 0 0 11px #fff, 0 0 19px #ec4899, 0 0 40px #ec4899, 0 0 80px #ec4899;
        }
        20%, 24%, 55% { text-shadow: none; }
    }

    h2, h3, h4 { 
        font-family: 'Cairo', sans-serif !important;
        text-align: center; 
        color: #e2e8f0 !important;
        text-shadow: 0 0 5px rgba(168, 85, 247, 0.5);
    }

    div.stTextInput > div > div > input, 
    div.stSelectbox > div > div > div, 
    div.stNumberInput > div > div > input,
    div.stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.02) !important;
        color: #ffffff !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-family: 'Cairo', sans-serif !important;
        transition: all 0.4s ease-in-out;
    }

    div.stTextInput > div > div > input:focus, 
    div.stSelectbox > div > div > div:focus,
    div.stTextArea > div > div > textarea:focus {
        border-color: #ec4899 !important;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.6) !important;
        background: rgba(236, 72, 153, 0.05) !important;
    }

    div[data-testid="stForm"] {
        background: rgba(15, 10, 25, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 24px !important;
        padding: 30px !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(168, 85, 247, 0.1) !important;
        backdrop-filter: blur(10px);
    }

    div.stButton > button {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.4), 0 0 30px rgba(139, 92, 246, 0.2) !important;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.8), 0 0 50px rgba(139, 92, 246, 0.6) !important;
    }

    .whatsapp-btn button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
        box-shadow: 0 0 15px rgba(56, 239, 125, 0.4) !important;
    }
    .whatsapp-btn button:hover {
        box-shadow: 0 0 30px rgba(56, 239, 125, 0.9) !important;
    }

    [data-testid="stMetricValue"] {
        color: #38ef7d !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(56, 239, 125, 0.5);
    }
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 18px !important;
    }
</style>
"""
st.markdown(premium_ui_css, unsafe_allow_html=True)

# ==================== [ 3. دوال الحماية والاتصال بـ GitHub ] ====================
def sanitize_text(text):
    if not isinstance(text, str): return str(text)
    if text.startswith(('=', '+', '-', '@')): text = "'" + text
    return re.sub(r'[<>"{};]', '', text)

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

# ==================== [ 4. شاشة تسجيل الدخول ] ====================
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
            st.markdown("### 🔐 لوحة الإدارة")
            admin_name = st.text_input("اسم المستخدم:")
            admin_pass = st.text_input("كلمة المرور:", type="password")
            if st.form_submit_button("تسجيل الدخول كـ أدمن"):
                sec_user = st.secrets.get("ADMIN_USERNAME", "admin")
                sec_pass = st.secrets.get("ADMIN_PASSWORD", "sawa2026")
                if admin_name == sec_user and admin_pass == sec_pass:
                    st.session_state["user_role"] = "admin"
                    st.rerun()
                else:
                    st.error("البيانات غير صحيحة.")

# ==================== [ 5. صفحة المستخدم (الزبون) ] ====================
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
                try:
                    img = Image.open(uploaded_file)
                    img.verify() 
                    is_valid_image = True
                except:
                    is_valid_image = False
                
                if not is_valid_image:
                    st.error("عذراً، الملف المرفوع تالف أو ليس صورة صالحة للطباعة!")
                else:
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

# ==================== [ 6. صفحة الإدارة / الداش بورد المتطورة ] ====================
elif st.session_state["user_role"] == "admin":
    st.title("📊 داش بورد القيادة - SAWA SHOP")
    
    if st.sidebar.button("⬅️ تسجيل الخروج"):
        st.session_state["user_role"] = None
        st.rerun()
        
    st.divider()
    
    if not df_orders.empty:
        df_orders['الكمية'] = pd.to_numeric(df_orders['الكمية'], errors='coerce').fillna(1)
        total_orders = len(df_orders)
        total_pieces = int(df_orders['الكمية'].sum())
        
        # --- المؤشرات الأساسية ---
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="📈 الأوردرات المستلمة", value=f"{total_orders} أوردر")
        with stat_col2:
            st.metric(label="👕 القطع المطلوب طباعتها", value=f"{total_pieces} قطعة")
            
        st.divider()
        
        # --- [الإضافة الجديدة 1] حاسبة الأرباح والتكاليف ---
        st.markdown("### 💰 حاسبة التكاليف والأرباح")
        cost_col, sell_col, profit_col = st.columns(3)
        with cost_col:
            cost = st.number_input("متوسط التكلفة للقطعة (جنية):", value=150, step=10)
        with sell_col:
            sell = st.number_input("متوسط سعر البيع (جنية):", value=300, step=10)
        with profit_col:
            total_profit = (sell - cost) * total_pieces
            st.metric(label="💸 إجمالي الأرباح المتوقعة", value=f"{total_profit} ج.م")

        # --- [الإضافة الجديدة 2] نظام تنبيه المخزون ---
        st.markdown("### 📦 تنبيهات المخزون التلقائية")
        top_item = df_orders.groupby('النوع')['الكمية'].sum().idxmax()
        top_color = df_orders.groupby('اللون')['الكمية'].sum().idxmax()
        st.warning(f"⚠️ **خلي بالك:** أكثر منتج مطلوب هو ({top_item} - لون {top_color}). تأكد من توفر خاماته في المصنع!")
            
        st.divider()
        
        # --- التحليلات البيانية ---
        st.markdown("### 📊 تحليل المبيعات")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("#### 🎨 الألوان الأكثر طلباً:")
            st.bar_chart(df_orders.groupby('اللون')['الكمية'].sum())
        with chart_col2:
            st.markdown("#### 👕 المنتجات الأكثر مبيعاً:")
            st.bar_chart(df_orders.groupby('النوع')['الكمية'].sum())
            
        st.divider()
        
        # --- [الإضافة الجديدة 3] السجل وتنزيل البيانات ---
        st.markdown("### 📄 السجل التفصيلي للطلبات")
        st.dataframe(df_orders, use_container_width=True)
        
        csv_download = df_orders.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 تنزيل سجل الأوردرات (Excel/CSV)", data=csv_download, file_name='Sawa_Orders.csv', mime='text/csv')
        
        st.divider()
        
        # --- تصاميم العملاء ---
        st.markdown("### 🖼️ تصاميم العملاء الجاهزة للطباعة")
        for idx, row in df_orders.iterrows():
            with st.container():
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    st.write(f"👤 **العميل:** {row['الاسم']} | 📞 **الموبايل:** {row['الموبايل']}")
                    st.write(f"👕 **الطلب:** {row['النوع']} | {row['اللون']} | مقاس {row['المقاس']} | عدد {row['الكمية']} قطع")
                    st.write(f"📝 **ملاحظات:** {row['ملاحظات']}")
                    st.write(f"📅 **التاريخ:** {row['التاريخ']}")
                    st.markdown(f"[📥 تحميل الصورة بجودة عالية للمطبعة]({row['رابط_التصميم']})")
                with col_img:
                    st.image(row['رابط_التصميم'], width=150)
                st.markdown("<hr style='border:1px solid #a855f7; opacity:0.3;'>", unsafe_allow_html=True)
    else:
        st.info("لا توجد أوردرات مسجلة حتى الآن.")
