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

# 3. كود الديكور الخارق - متوافق تماماً مع الموبايل والكمبيوتر (Responsive CSS)
responsive_premium_css = """
<style>
    /* إعدادات الخلفية الفخمة المتدرجة لكل الشاشات */
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111026 50%, #220b2e 100%);
        color: #f1f5f9 !important;
    }

    /* ضبط الخطوط والعناوين لتكون متناسقة على الموبايل والكمبيوتر */
    h1 {
        font-size: clamp(1.8rem, 4vw, 3rem) !important;
        color: #ffffff !important;
        text-align: center;
        background: linear-gradient(90deg, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px !important;
    }
    h3 {
        font-size: clamp(1.2rem, 2.5vw, 1.8rem) !important;
        color: #cbd5e1 !important;
        text-align: center;
        margin-bottom: 25px !important;
    }

    /* تحويل الخانات لبطاقات زجاجية مضيئة ومناسبة للمس بالصابع على الموبايل */
    div.stTextInput > div > div > input, 
    div.stSelectbox > div > div > div, 
    div.stNumberInput > div > div > input,
    div.stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: clamp(8px, 2vw, 14px) !important;
        font-size: clamp(14px, 1.5vw, 16px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* تأثير النيون المتوهج عند التفاعل أو الكتابة */
    div.stTextInput > div > div > input:focus, 
    div.stSelectbox > div > div > div:focus,
    div.stTextArea > div > div > textarea:focus {
        border-color: #ec4899 !important;
        box-shadow: 0 0 20px rgba(236, 72, 153, 0.4) !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }

    /* تصميم زرار "تأكيد الأوردر" الخارق */
    div.stButton > button {
        background: linear-gradient(90deg, #ca8a04 0%, #e11d48 50%, #9333ea 100%) !important;
        background-size: 200% auto !important;
        color: white !important;
        font-weight: bold !important;
        font-size: clamp(16px, 2vw, 20px) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: clamp(12px, 2.5vw, 18px) !important;
        box-shadow: 0 10px 25px rgba(225, 29, 72, 0.3) !important;
        transition: all 0.4s ease;
        width: 100%;
        text-transform: uppercase;
        animation: pulseGlow 2s infinite;
    }

    /* تأثير تحريك الماوس وحركة النبض للزرار */
    div.stButton > button:hover {
        background-position: right center !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(225, 29, 72, 0.6) !important;
    }
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(225, 29, 72, 0); }
        100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
    }

    /* تعديل مربع رفع الملفات ليكون شيك ومريح على الموبايل */
    div.stFileUploader section {
        background: rgba(168, 85, 247, 0.03) !important;
        border: 2px dashed rgba(168, 85, 247, 0.3) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        transition: border-color 0.3s ease;
    }
    div.stFileUploader section:hover {
        border-color: #ec4899 !important;
    }

    /* كود خاص لضبط الاستجابة على الشاشات الصغيرة (الموبايلات) */
    @media (max-width: 768px) {
        .stColumns [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 20px;
        }
        div.stButton > button {
            padding: 15px !important; /* تكبير الزرار على الموبايل لسهولة الضغط */
        }
    }
</style>
"""
st.markdown(responsive_premium_css, unsafe_allow_html=True)

# 4. الاتصال بـ GitHub بأمان عبر الـ Secrets
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
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"خطأ أثناء الحفظ على جيت هاب: {e}")
        return False

# دالة ذكية لقراءة سجل الأوردرات الحالي من GitHub
@st.cache_data(ttl=60)
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

# نظام الحماية وفصل الصفحات باستخدام Session State
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# الواجهة الرئيسية للموقع (تفتح دائماً على متجر الزبائن)
if not st.session_state["admin_logged_in"]:
    st.title("🛍️ SAWA SHOP")
    st.subheader("صمم قطعتك الفريدة.. ونحن نرفعها للواقع")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسمك بالكامل:")
        phone = st.text_input("رقم الواتساب (لتأكيد الأوردر):")
        
        item_type = st.selectbox("نوع المنتج:", ["تيشيرت صيفي قطن", "هودي شتوي", "سويت شيرت"])
        color = st.selectbox("لون القماش:", ["أسود", "أبيض", "رمادي"])
        size = st.selectbox("المقاس:", ["M", "L", "XL", "XXL"])
        qty = st.number_input("الكمية المطلوبة:", min_value=1, step=1)
        
        details = st.text_area("هل لديك أي ملاحظات خاصة بالتصميم؟", placeholder="مثال: محتاج الطباعة في منتصف الصدر بالظبط...")
    
    with col2:
        st.markdown("<p style='font-weight: bold; font-size: 16px; margin-bottom:5px;'>📸 ارفع لوحة تصميمك هنا:</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="معاينة التصميم المرفوع", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("إرسال وتأكيد الأوردر الآن 🚀"):
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
                
                df_updated = pd.concat([df_orders, pd.DataFrame([new_row])], ignore_index=True)
                
                csv_buffer = io.StringIO()
                df_updated.to_csv(csv_buffer, index=False)
                upload_to_github(csv_buffer.getvalue().encode('utf-8'), "orders.csv", f"Add order for {name}")
                
                st.success("يا فنان، أوردرك وتصميمك وصلوا لعمار بنجاح! هنتواصل معاك على الواتساب فوراً. 🎉")
                st.balloons()
        else:
            st.error("من فضلك، تأكد من كتابة الاسم ورقم الموبايل ورفع صورة التصميم أولاً!")

    # بوابتك السرية للإدارة بأسفل الصفحة
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    with st.expander("🔐 لوحة تحكم الإدارة"):
        password = st.text_input("كلمة المرور السرية:", type="password")
        if st.button("دخول"):
            if password == "sawa2026":
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("كلمة السر خاطئة!")

# --- لوحة التحكم المتطابقة مع الديكور الجديد ---
else:
    st.title("📊 لوحة تحكم وإدارة طلبات SAWA Shop")
    
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
