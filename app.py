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

# 3. حقن كود الديكور الـ CSS السحري لتحويل مظهر الموقع تماماً
custom_css = """
<style>
    /* تغيير خلفية الموقع بالكامل لون داكن فاخر */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Cairo', sans-serif;
    }
    
    /* تصميم الهيدر والعناوين */
    h1 {
        color: #FFD700 !important; /* اللون الذهبي للبراند */
        text-align: center;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    h3 {
        color: #E0E0E0 !important;
        text-align: center;
    }
    
    /* تعديل شكل بطاقات إدخال البيانات */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1F2633 !important;
        color: #FFFFFF !important;
        border: 1px solid #3A4750 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* تدليع شكل زرار إرسال الأوردر وتأكيده */
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FF8C00) !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        width: 100% !important;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3) !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    /* تأثير حركي عند مرور الماوس على الزرار */
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.6) !important;
        background: linear-gradient(45deg, #FF8C00, #FFD700) !important;
    }
    
    /* تنسيق جدول البيانات للإدارة */
    .stDataFrame {
        background-color: #1F2633 !important;
        border-radius: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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

# دالة لقراءة سجل الأوردرات الحالي من GitHub
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

# نظام إدارة الصفحات المسجل في المتصفح
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# --- الواجهة الرئيسية للموقع (متجر الزبائن) ---
if not st.session_state["admin_logged_in"]:
    st.title("👑 متجر SAWA Shop الإلكتروني")
    st.subheader("صمم قطعتك الفريدة بأعلى جودة طباعة خامات عالمية")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # حطيت البيانات جوه حاوية أنيقة
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 اسمك الكريم بالكامل:", key="cust_name")
            phone = st.text_input("📞 رقم الواتساب (لتأكيد الأوردر):", key="cust_phone")
            item_type = st.selectbox("👕 اختر نوع المنتج:", ["تيشيرت صيفي قطن", "هودي شتوي", "سويت شيرت"], key="cust_item")
            color = st.selectbox("🎨 اختر لون القماش:", ["أسود", "أبيض", "رمادي"], key="cust_color")
            size = st.selectbox("📏 اختر المقاس المناسب:", ["M", "L", "XL", "XXL"], key="cust_size")
            qty = st.number_input("🔢 الكمية المطلوبة:", min_value=1, step=1, key="cust_qty")
            details = st.text_area("📝 تفاصيل أو ملاحظات خاصة بالتصميم:", placeholder="مثال: عايز الطباعة تكون كبيرة في الظهر..", key="cust_details")
        
        with col2:
            st.markdown("<p style='text-align: center; font-weight: bold;'>🖼️ ارفع تصميمك هنا</p>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="cust_file")
            if uploaded_file is not None:
                st.image(uploaded_file, caption="معاينة التصميم المرفوع", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("تأكيد وإرسال الأوردر للمصنع 🚀"):
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
                
                st.success("يا فنان، أوردرك وتصميمك وصلوا لعمار بنجاح! هنتواصل معاك فوراً. 🎉")
                st.balloons()
        else:
            st.error("من فضلك، تأكد من كتابة الاسم ورقم الموبايل ورفع صورة التصميم أولاً!")

    # بوابة الدخول السرية للإدارة
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    with st.expander("🔐 تسجيل دخول الإدارة"):
        password = st.text_input("أدخل كلمة السر الخاصة بعمار:", type="password", key="admin_password")
        if st.button("دخول"):
            if password == "sawa2026":
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("كلمة السر خاطئة يا صاحبي!")

# --- لوحة التحكم (خاصة بعمار) ---
else:
    st.title("📊 لوحة إدارة طلبات SAWA Shop")
    if st.button("⬅️ خروج والعودة للمتجر"):
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
