import streamlit as st

# 1. إعدادات الصفحة (يجب أن تكون في أول الكود)
st.set_page_config(page_title="متجر الروايات النيوني", page_icon="📚", layout="wide")

# 2. كود الديكور والنيون والخلفية (CSS)
neon_style = """
<style>
/* إعداد خلفية الموقع بالكامل (صورة مكتبة فخمة مع طبقة داكنة) */
.stApp {
    background: linear-gradient(rgba(15, 15, 26, 0.88), rgba(15, 15, 26, 0.95)), 
                url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    direction: rtl;
}

/* تصميم عنوان الموقع بتأثير النيون الأزرق المضيء */
.neon-title {
    color: #fff;
    text-align: center;
    font-size: 3.5rem;
    font-weight: bold;
    text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 40px #00f3ff;
    margin-bottom: 5px;
    padding-top: 20px;
}

.neon-subtitle {
    color: #ff007f;
    text-align: center;
    font-size: 1.5rem;
    text-shadow: 0 0 5px #ff007f, 0 0 10px #ff007f;
    margin-bottom: 40px;
}

/* تصميم كارت الكتاب (برواز نيون وردي مضيء يتفاعل مع الحركة) */
.book-card {
    background: rgba(25, 25, 40, 0.65);
    border: 2px solid #ff007f;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.3), inset 0 0 10px rgba(255, 0, 127, 0.1);
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
}

.book-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.8), inset 0 0 15px rgba(255, 0, 127, 0.4);
    border-color: #fff;
}

/* نصوص الكارت داخل النيون */
.book-title {
    color: #fff;
    font-size: 1.4rem;
    font-weight: bold;
    text-shadow: 0 0 5px #fff;
    margin-top: 15px;
}

.book-author {
    color: #00f3ff;
    font-size: 1rem;
    text-shadow: 0 0 3px #00f3ff;
    margin: 5px 0;
}

.book-price {
    color: #39ff14; /* أخضر نيون فسفوري */
    font-size: 1.3rem;
    font-weight: bold;
    text-shadow: 0 0 5px #39ff14;
    margin-bottom: 10px;
}

/* تحويل أزرار Streamlit العادية إلى أزرار نيون متوهجة */
div.stButton > button {
    background-color: transparent !important;
    color: #00f3ff !important;
    border: 2px solid #00f3ff !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1rem !important;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.4) !important;
    text-shadow: 0 0 5px #00f3ff !important;
    width: 100%;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover {
    background-color: #00f3ff !important;
    color: #121212 !important;
    box-shadow: 0 0 25px #00f3ff !important;
    transform: scale(1.02);
}
</style>
"""

# تطبيق الديكور على الموقع
st.markdown(neon_style, unsafe_allow_html=True)

# 3. واجهة الموقع الرئيسية
st.markdown('<div class="neon-title">مـكـتـبـة الـنـيـون 📚</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">بوابتك السحرية لأجمل الكتب والروايات</div>', unsafe_allow_html=True)

# 4. قاعدة بيانات الكتب والصور
books = [
    {
        "id": "b1",
        "title": "رواية الخيميائي",
        "author": "باولو كويلو",
        "price": 150,
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400"
    },
    {
        "id": "b2",
        "title": "أرض زيكولا",
        "author": "عمرو عبد الحميد",
        "price": 180,
        "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400"
    },
    {
        "id": "b3",
        "title": "فن اللامبالاة",
        "author": "مارك مانسون",
        "price": 120,
        "image": "https://images.unsplash.com/photo-1532012197267-da84d127e765?q=80&w=400"
    }
]

# 5. عرض الكتب في تصميم ثلاثي الأعمدة (Grid)
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for index, book in enumerate(books):
    with columns[index]:
        # عرض كارت الكتاب بالديكور المخصص
        st.markdown(f"""
        <div class="book-card">
            <img src="{book['image']}" style="width:100%; height:250px; object-fit:cover; border-radius:10px; border: 1px solid #ff007f;">
            <div class="book-title">{book['title']}</div>
            <div class="book-author">تأليف: {book['author']}</div>
            <div class="book-price">{book['price']} جنيه</div>
        </div>
        """, unsafe_allow_html=True)
        
        # مسافة صغيرة ثم زر الشراء المتوهج
        st.write("")
        if st.button(f"🛒 أضف للسلة", key=book['id']):
            st.toast(f"تمت إضافة ({book['title']}) إلى سلة المشتريات! 🎉")
