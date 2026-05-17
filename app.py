import streamlit as st
import pandas as pd
from github import Github
from PIL import Image
import io
import datetime

# 1. إعدادات الصفحة واسم المتجر في محرك البحث
st.set_page_config(page_title="SAWA Shop - نظام إدارة المتجر", layout="wide")

# 2. كود التحقق التلقائي الخاص بجوجل (SEO)
if "GOOGLE_VERIFICATION" in st.secrets:
    st.markdown(st.secrets["GOOGLE_VERIFICATION"], unsafe_allow_html=True)

# 3. كود الديكور الخارق المطور (Responsive & Interactive UI)
premium_ui_css = """
<style>
    /* إعدادات الخلفية الفخمة */
    .stApp {
        background: linear-gradient(135deg, #070a13 0%, #0f0e26 50%, #1d072b 100%);
        color: #f1f5f9 !important;
    }

    /* العناوين المضيئة */
    h1 {
        font-size: clamp(2rem, 5vw, 3.5rem) !important;
        color: #ffffff !important;
        text-align: center;
        background: linear-gradient(90deg, #ca8a04, #ec4899, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px !important;
    }
    h2, h3, h4 {
        color: #e2e8f0 !important;
        text-align: center;
    }

    /* كروت زجاجية مضيئة للخانات (Glassmorphism) */
    div.stTextInput > div > div > input, 
    div.stSelectbox > div > div > div, 
    div.stNumberInput > div > div > input,
    div.stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 12px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* توهج النيون عند الكتابة */
    div.stTextInput > div > div > input:focus, 
    div.stSelectbox > div > div > div:focus,
    div.stTextArea > div > div > textarea:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* تصميم الأزرار - زرار الإرسال */
    .send-btn button, div.stButton > button {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        box-shadow: 0 8px 20px rgba(236, 72, 153, 0.3) !important;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(236, 72, 153, 0.5) !important;
    }

    /* تصميم زرار الواتساب الاحترافي الأخضر */
    .whatsapp-btn button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        padding: 14px !important;
        box-shadow: 0 8px 20px rgba(56, 239, 125, 0.2) !important;
        transition: all 0.3s ease;
        width: 100%;
    }
    .whatsapp-btn button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(56, 239, 125, 0.5) !important;
    }

    /* تعديل شكل الفورم الزجاجي لمنع أخطاء الريفرش */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
    }

    [data-testid="stMetricValue"] {
        color: #a855f7 !important;
        font-weight: bold !important;
    }
</style>
"""
st.markdown(premium_ui_css, unsafe_allow_html=True)

# 4. الاتصال بـ GitHub بأمان عبر الـ Secrets
@st.cache_resource
def get_github_repo():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        return g.get_repo(st.secrets["GITHUB_REPO"])
    except:
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
    except:
        return False

# دالة ذكية لقراءة سجل الأوردرات الحالي من GitHub
@st.cache_data(ttl=5)
def load_orders_from_github():
    default_cols = ["الاسم", "الموبايل", "النوع", "اللون", "المقاس", "الكمية", "ملاحظات", "رابط_التصميم", "التاريخ"]
    if repo is None:
        return pd.DataFrame(columns=default_cols)
    try:
        contents = repo.get_contents("orders.csv")
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        
        # حماية إضافية: لو الملف القديم فيه أسامي أعمدة قديمة، بنوحدها هنا أوتوماتيك
        if "نوع المنتج" in df.columns and "النوع" not in df.columns:
            df = df.rename(columns={"نوع المنتج": "النوع"})
            
        # التأكد من وجود كل الأعمدة المطلوبة عشان ميتكررش أي KeyError
        for col in default_cols:
            if col not in df.columns:
                df[col] = "غير محدد"
                
        return df
    except:
        return pd.DataFrame(columns=default_cols)

df_orders = load_orders_from_github()

# --- نظام إدارة الجلسة والصفحات (Session State) ---
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None

# ==================== [ شاشة تسجيل الدخول الرئيسية ] ====================
if st.session_state["user_role"] is None:
    st.title("🛍️ نظام متجر SAWA SHOP")
    st.subheader("مرحباً بك، يرجى اختيار نوع الحساب للمتابعة")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_login1, col_login2 = st.columns(2)
    
    with col_login1:
        with st.form(key="customer_login_form"):
            st.markdown("### 👕 تصفح واطلب ملابسك")
            st.write("ادخل لتصميم تيشيرتك أو الهودي الخاص بك وإرساله للمصنع فوراً.")
            submit_cust = st.form_submit_button("الدخول كـ مستخدم (زبون)")
            if submit_cust:
                st.session_state["user_role"] = "customer"
                st.rerun()
        
    with col_login2:
        with st.form(key="admin_login_form"):
            st.markdown("### 🔐 لوحة تحكم الإدارة")
            st.write("خاصة بمدير المصنع لمتابعة الأوردرات والداش بورد.")
            
            admin_name = st.text_input("اسم المستخدم:", key="adm_username")
            admin_pass = st.text_input("كلمة المرور:", type="password", key="adm_password")
            
            submit_admin = st.form_submit_button("تسجيل الدخول كـ أدمن")
            if submit_admin:
                if admin_name == "admin" and admin_pass == "sawa2026":
                    st.session_state["user_role"] = "admin"
                    st.toast("🎉 مرحباً بك يا فنان، جاري فتح لوحة التحكم...")
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة يا فنان!")

# ==================== [ صفحة المستخدم / الزبون ] ====================
elif st.session_state["user_role"] == "customer":
    st.title("🛍️ متجر SAWA SHOP الإلكتروني")
    st.subheader("صمم قطعتك الفريدة ودع الباقي للمصنع")
    
    if st.sidebar.button("⬅️ تسجيل الخروج والعودة للرئيسية"):
        st.session_state["user_role"] = None
        st.rerun()
        
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
        
        promo_code = st.text_input("هل لديك كود خصم؟ 🎁", placeholder="اكتب كود الخصم هنا لو معاك")
        if promo_code:
            if promo_code.upper() == "SAWA10":
                st.success("🔥 مبروك يا فنان! تم تفعيل كود الخصم (10% خصم على إجمالي الطلب)")
                st.balloons()
            else:
                st.warning("كود الخصم هذا غير صحيح أو انتهت صلاحيته.")
    
    with col2:
        st.markdown("<p style='font-weight: bold; font-size: 16px; margin-bottom:5px;'>📸 ارفع لوحة تصميمك هنا:</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="معاينة التصميم المرفوع", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("إرسال وتأكيد الأوردر للمصنع 🚀"):
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
                    st.toast("🚀 تم تسجيل الأوردر بنجاح في قاعدة البيانات!")
            else:
                st.error("من فضلك، تأكد من كتابة الاسم ورقم الموبايل ورفع صورة التصميم أولاً!")

    with btn_col2:
        st.markdown('<div class="whatsapp-btn">', unsafe_allow_html=True)
        whatsapp_url = f"https://wa.me/201149243249?text=مرحباً%20SAWA%20Shop،%20كنت%20محتاج%20أستفسر%20عن%20تفاصيل%20أوردر%20طباعة"
        if st.button("💬 تواصل معنا عبر الواتساب"):
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{whatsapp_url}\'" />', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== [ صفحة الإدارة / الداش بورد المحمية ] ====================
elif st.session_state["user_role"] == "admin":
    st.title("📊 داش بورد نظام إدارة SAWA SHOP")
    st.subheader("مرحباً بك يا فنان في لوحة التحكم المركزية")
    
    if st.sidebar.button("⬅️ تسجيل الخروج"):
        st.session_state["user_role"] = None
        st.rerun()
        
    st.divider()
    
    if not df_orders.empty:
        # تحويل الكميات لأرقام بأمان لمعالجة أي نصوص
        df_orders['الكمية'] = pd.to_numeric(df_orders['الكمية'], errors='coerce').fillna(1)
        
        total_orders = len(df_orders)
        total_pieces = int(df_orders['الكمية'].sum())
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="📈 إجمالي الأوردرات المستلمة", value=f"{total_orders} أوردر")
        with stat_col2:
            st.metric(label="👕 إجمالي القطع المطلوب طباعتها", value=f"{total_pieces} قطعة")
            
        st.divider()
        
        st.markdown("### 📊 تحليل السوق ومبيعات المتجر")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 🎨 الألوان الأكثر طلباً من الزبائن:")
            if 'اللون' in df_orders.columns:
                color_counts = df_orders.groupby('اللون')['الكمية'].sum()
                st.bar_chart(color_counts)
            else:
                st.info("لا توجد بيانات ألوان كافية للرسم البياني.")
            
        with chart_col2:
            st.markdown("#### 👕 المنتجات الأكثر مبيعاً في المصنع:")
            if 'النوع' in df_orders.columns:
                type_counts = df_orders.groupby('النوع')['الكمية'].sum()
                st.bar_chart(type_counts)
            else:
                st.info("لا توجد بيانات منتجات كافية للرسم البياني.")
            
        st.divider()
        
        st.markdown("#### 📄 جدول سجل الطلبات التفصيلي:")
        st.dataframe(df_orders, use_container_width=True)
        st.divider()
        
        st.markdown("### 🖼️ استعراض وتنزيل لوحات التصاميم للطباعة")
        for idx, row in df_orders.iterrows():
            with st.container():
                col_txt, col_img = st.columns([2, 1])
                with col_txt:
                    st.write(f"👤 **العميل:** {row['الاسم']}")
                    st.write(f"📞 **واتساب العميل:** {row['الموبايل']}")
                    st.write(f"🏷️ **نوع القطعة:** {row.get('النوع', 'غير محدد')}")
                    st.write(f"🎨 **المواصفات:** لون {row.get('اللون', 'غير محدد')} | مقاس {row.get('المقاس', 'غير محدد')} | عدد {row['الكمية']} قطع")
                    st.write(f"📝 **ملاحظات العميل للطباعة:** {row.get('ملاحظات', 'لا يوجد')}")
                    st.write(f"📅 **التاريخ والوقت:** {row.get('التاريخ', 'غير مسجل')}")
                    if 'رابط_التصميم' in row and str(row['رابط_التصميم']).startswith('http'):
                        st.markdown(f"[📥 تحميل الصورة بجودة عالية للماكينة]({row['رابط_التصميم']})")
                with col_img:
                    if 'رابط_التصميم' in row and str(row['رابط_التصميم']).startswith('http'):
                        st.image(row['رابط_التصميم'], width=180)
                st.divider()
    else:
        st.info("لا توجد أوردرات مسجلة في قاعدة البيانات حتى الآن.")
