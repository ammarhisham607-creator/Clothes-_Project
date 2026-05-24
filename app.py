import streamlit as st
import pandas as pd
from github import Github
import io
import json
import datetime
import re
from PIL import Image

# ==================== [ 1. إعدادات الصفحة ] ====================
st.set_page_config(page_title="SAWA Shop", layout="wide")

# ==================== [ 2. الديكور النيون المتغير والخرابيش (Cyberpunk) ] ====================
premium_ui_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية بخطوط وخرابيش شبكية (Cyberpunk Scratches) */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(2,2,5,0.95) 0%, rgba(18,2,28,0.95) 100%),
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.03) 10px, rgba(255,255,255,0.03) 11px),
            repeating-linear-gradient(-45deg, transparent, transparent 10px, rgba(255,255,255,0.03) 10px, rgba(255,255,255,0.03) 11px) !important;
        background-attachment: fixed !important;
        font-family: 'Cairo', sans-serif !important;
        color: #f8fafc !important;
    }

    /* نيون بألوان متغيرة (أحمر، أخضر، أصفر، أزرق، وردي) وبيطفي وينور */
    h1 {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 900 !important;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 25px !important;
        text-transform: uppercase;
        animation: rgb-neon-glitch 4s infinite alternate;
    }

    @keyframes rgb-neon-glitch {
        0%   { text-shadow: 0 0 5px #fff, 0 0 10px #ff003c, 0 0 20px #ff003c, 0 0 40px #ff003c; }
        20%  { text-shadow: 0 0 5px #fff, 0 0 10px #ff003c, 0 0 20px #ff003c, 0 0 40px #ff003c; }
        21%  { text-shadow: none; } /* خربشة أو طفية سريعة */
        22%  { text-shadow: 0 0 5px #fff, 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 40px #00ff00; }
        40%  { text-shadow: 0 0 5px #fff, 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 40px #00ff00; }
        50%  { text-shadow: 0 0 5px #fff, 0 0 10px #fcee0a, 0 0 20px #fcee0a, 0 0 40px #fcee0a; }
        70%  { text-shadow: 0 0 5px #fff, 0 0 10px #00e5ff, 0 0 20px #00e5ff, 0 0 40px #00e5ff; }
        71%  { text-shadow: none; } /* طفية سريعة تانية */
        72%  { text-shadow: 0 0 5px #fff, 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px #a855f7; }
        100% { text-shadow: 0 0 5px #fff, 0 0 10px #a855f7, 0 0 20px #a855f7, 0 0 40px #a855f7; }
    }

    h2, h3, h4 { 
        font-family: 'Cairo', sans-serif !important;
        text-align: center; 
        color: #e2e8f0 !important;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
    }

    /* الخانات شكلها زجاجي ومتين */
    div.stTextInput > div > div > input, 
    div.stSelectbox > div > div > div, 
    div.stNumberInput > div > div > input,
    div.stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-family: 'Cairo', sans-serif !important;
    }

    div.stTextInput > div > div > input:focus, 
    div.stSelectbox > div > div > div:focus,
    div.stTextArea > div > div > textarea:focus {
        border-color: #00e5ff !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4) !important;
    }

    /* أزرار الإرسال */
    div.stButton > button {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important; /* شكل حاد يدي طابع جيمنج */
        padding: 12px 30px !important;
        box-shadow: 0 0 15px rgba(236, 72, 153, 0.4) !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.8) !important;
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
    if repo is None: return pd.DataFrame(columns=default_cols)
    try:
        contents = repo.get_contents("orders.csv")
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        if "نوع المنتج" in df.columns: df = df.rename(columns={"نوع المنتج": "النوع"})
        for col in default_cols:
            if col not in df.columns: df[col] = "غير محدد"
        return df
    except:
        return pd.DataFrame(columns=default_cols)

# دالة قراءة الإعدادات
@st.cache_data(ttl=5)
def load_settings_from_github():
    default_settings = {
        "types": ["تيشيرت صيفي قطن", "هودي شتوي", "سويت شيرت"],
        "colors": ["أسود", "أبيض", "رمادي"]
    }
    if repo is None: return default_settings
    try:
        contents = repo.get_contents("settings.json")
        return json.loads(contents.decoded_content.decode('utf-8'))
    except:
        return default_settings

def save_settings_to_github(settings_dict):
    if repo is None: return False
    try:
        settings_json = json.dumps(settings_dict, ensure_ascii=False, indent=4)
        try:
            contents = repo.get_contents("settings.json")
            repo.update_file(contents.path, "Update settings", settings_json, contents.sha)
        except:
            repo.create_file("settings.json", "Create settings", settings_json)
        st.cache_data.clear()
        return True
    except:
        return False

# ==================== [ 4. تهيئة الذاكرة اللحظية (عشان التحديثات تظهر فوراً) ] ====================
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "customer"

if "settings" not in st.session_state:
    st.session_state["settings"] = load_settings_from_github()

df_orders = load_orders_from_github()

# ==================== [ 5. الشفرة السرية (الباب الخلفي للإدارة) ] ====================
with st.sidebar:
    if st.session_state["user_role"] == "customer":
        st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        with st.expander("⚙️"):
            admin_name = st.text_input("U", label_visibility="collapsed", placeholder="User")
            admin_pass = st.text_input("P", type="password", label_visibility="collapsed", placeholder="Pass")
            if st.button(">>", key="secret_login"):
                sec_user = st.secrets.get("ADMIN_USERNAME", "admin")
                sec_pass = st.secrets.get("ADMIN_PASSWORD", "sawa2026")
                if admin_name == sec_user and admin_pass == sec_pass:
                    st.session_state["user_role"] = "admin"
                    st.rerun()
                else:
                    st.error("خطأ")
    else:
        if st.button("⬅️ خروج من الإدارة"):
            st.session_state["user_role"] = "customer"
            st.rerun()

# ==================== [ 6. صفحة المتجر (الواجهة الرئيسية) ] ====================
if st.session_state["user_role"] == "customer":
    st.title("🛍️ متجر SAWA SHOP")
    st.subheader("صمم قطعتك الفريدة ودع الباقي للمصنع")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسمك بالكامل:")
        phone = st.text_input("رقم الواتساب:")
        # بتقرأ هنا من الـ Session State عشان تظهر أي لون أو قسم جديد في ثانية!
        item_type = st.selectbox("نوع المنتج:", st.session_state["settings"]["types"])
        color = st.selectbox("لون القماش:", st.session_state["settings"]["colors"])
        size = st.selectbox("المقاس:", ["S", "M", "L", "XL", "XXL", "3XL", "4XL"])
        qty = st.number_input("الكمية المطلوبة:", min_value=1, step=1)
        details = st.text_area("ملاحظات خاصة بالطباعة (اختياري):")
    
    with col2:
        st.markdown("**📸 ارفع لوحة تصميمك هنا:**")
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="معاينة التصميم", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("إرسال وتأكيد الأوردر 🚀"):
            if name and phone and uploaded_file:
                try:
                    img = Image.open(uploaded_file)
                    img.verify() 
                    is_valid_image = True
                except:
                    is_valid_image = False
                
                if not is_valid_image:
                    st.error("الملف المرفوع تالف أو ليس صورة صالحة!")
                else:
                    clean_name = sanitize_text(name)
                    clean_phone = sanitize_text(phone)
                    clean_details = sanitize_text(details)
                    
                    time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_extension = uploaded_file.name.split(".")[-1]
                    github_img_path = f"customer_designs/{time_str}_{clean_phone}.{file_extension}"
                    
                    with st.spinner("جاري تأمين ورفع الأوردر..."):
                        img_success = upload_to_github(uploaded_file.getvalue(), github_img_path, f"Order: {clean_name}")
                    
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
                        
                        st.success("تم إرسال أوردرك وتصميمك بنجاح! 🎉")
                        st.balloons()
            else:
                st.error("برجاء إدخال الاسم، رقم الواتساب، ورفع التصميم أولاً!")

    with btn_col2:
        whatsapp_html = """
        <a href="https://wa.me/201149243249?text=مرحباً%20SAWA%20Shop،%20أريد%20الاستفسار" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%); color: white; text-align: center; font-weight: bold; font-family: 'Cairo', sans-serif; border-radius: 5px; padding: 12px; margin-top: 2px; box-shadow: 0 0 15px rgba(56, 239, 125, 0.4); cursor: pointer; transition: 0.3s; width: 100%;">
                💬 تواصل معنا عبر الواتساب
            </div>
        </a>
        """
        st.markdown(whatsapp_html, unsafe_allow_html=True)

# ==================== [ 7. غرفة التحكم والإدارة (الكنترول) ] ====================
elif st.session_state["user_role"] == "admin":
    st.title("📊 غرفة تحكم SAWA SHOP")
    
    tab1, tab2 = st.tabs(["📋 متابعة الأوردرات والداش بورد", "⚙️ التحكم وإضافة الأقسام/الألوان"])
    
    with tab1:
        if not df_orders.empty:
            df_orders['الكمية'] = pd.to_numeric(df_orders['الكمية'], errors='coerce').fillna(1)
            total_orders = len(df_orders)
            total_pieces = int(df_orders['الكمية'].sum())
            
            st.markdown("### 📈 إحصائيات سريعة")
            stat_col1, stat_col2 = st.columns(2)
            stat_col1.metric("📦 الأوردرات المستلمة", f"{total_orders} أوردر")
            stat_col2.metric("👕 القطع المطلوب طباعتها", f"{total_pieces} قطعة")
                
            st.divider()
            st.markdown("#### 📄 جدول الطلبات التفصيلي")
            st.dataframe(df_orders, use_container_width=True)
            
            st.divider()
            st.markdown("### 🖼️ تصاميم العملاء الجاهزة للطباعة")
            for idx, row in df_orders.iterrows():
                with st.container():
                    col_txt, col_img = st.columns([2, 1])
                    with col_txt:
                        st.write(f"👤 **العميل:** {row['الاسم']} | 📞 **واتساب:** {row['الموبايل']}")
                        st.write(f"👕 **الطلب:** {row['النوع']} | لون {row['اللون']} | مقاس {row['المقاس']} | عدد {row['الكمية']}")
                        st.write(f"📝 **الملاحظات:** {row['ملاحظات']}")
                        st.write(f"📅 **الوقت:** {row['التاريخ']}")
                        st.markdown(f"[📥 تحميل الصورة الأصلية]({row['رابط_التصميم']})")
                    with col_img:
                        st.image(row['رابط_التصميم'], width=150)
                    st.markdown("<hr style='border:1px solid #00e5ff; opacity:0.3;'>", unsafe_allow_html=True)
        else:
            st.info("لا توجد أوردرات مسجلة حتى الآن.")

    with tab2:
        st.markdown("### ➕ تحديث المتجر (يظهر للزبون فوراً)")
        col_type, col_color = st.columns(2)
        
        with col_type:
            st.markdown("#### إضافة قسم جديد")
            new_type = st.text_input("اسم المنتج الجديد (مثال: مج، كاب):")
            if st.button("إضافة القسم للمتجر"):
                if new_type and new_type not in st.session_state["settings"]["types"]:
                    # تحديث الذاكرة اللحظية
                    st.session_state["settings"]["types"].append(new_type)
                    # حفظ في جيت هاب في الخلفية
                    save_settings_to_github(st.session_state["settings"])
                    st.success(f"تم إضافة '{new_type}' بنجاح!")
                    st.rerun()
                    
        with col_color:
            st.markdown("#### إضافة لون جديد")
            new_color = st.text_input("اسم اللون الجديد (مثال: كحلي، أحمر):")
            if st.button("إضافة اللون للمتجر"):
                if new_color and new_color not in st.session_state["settings"]["colors"]:
                    # تحديث الذاكرة اللحظية
                    st.session_state["settings"]["colors"].append(new_color)
                    # حفظ في جيت هاب في الخلفية
                    save_settings_to_github(st.session_state["settings"])
                    st.success(f"تم إضافة لون '{new_color}' بنجاح!")
                    st.rerun()
                    
        st.divider()
        st.markdown("### 🖼️ خزانة الصور السريعة (لرفع أي صورة)")
        st.write("ارفع أي صورة هنا عشان تاخد الرابط بتاعها تستخدمه كإعلان أو تبعته للزبون.")
        admin_upload = st.file_uploader("اختر صورة للرفع:", type=["png", "jpg", "jpeg"])
        if st.button("رفع الصورة للخزنة 🚀"):
            if admin_upload:
                time_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                admin_img_path = f"store_assets/img_{time_str}.{admin_upload.name.split('.')[-1]}"
                with st.spinner("جاري الرفع..."):
                    upload_to_github(admin_upload.getvalue(), admin_img_path, "Admin uploaded image")
                    img_url = f"https://raw.githubusercontent.com/{st.secrets['GITHUB_REPO']}/main/{admin_img_path}"
                    st.success("تم الرفع بنجاح! الرابط جاهز للنسخ:")
                    st.code(img_url)
