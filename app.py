import streamlit as st
import base64
import requests
import json

# 1. إعدادات الصفحة العامة للمتجر
st.set_page_config(page_title="World of Books", page_icon="📚", layout="wide")

# 2. تصميم النيون الاحترافي مع دعم كامل للغة العربية والمحاذاة الصحيحة (CSS)
neon_style = """
<style>
.stApp {
    background: linear-gradient(rgba(15, 15, 26, 0.96), rgba(15, 15, 26, 0.98)), 
                url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1600');
    background-size: cover; background-position: center; background-attachment: fixed;
}
.main .block-container, [data-testid="stSidebarUserContent"] {
    direction: rtl !important;
    text-align: right !important;
}
@keyframes neon-glow {
    0% { text-shadow: 0 0 8px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; opacity: 1; }
    50% { text-shadow: 0 0 3px #00f3ff, 0 0 8px #00f3ff, 0 0 15px #00f3ff; opacity: 0.85; }
    100% { text-shadow: 0 0 8px #00f3ff, 0 0 15px #00f3ff, 0 0 30px #00f3ff; opacity: 1; }
}
.neon-title { 
    color: #fff; text-align: center; font-size: 3.5rem; font-weight: bold; 
    margin-bottom: 10px; padding-top: 20px;
    animation: neon-glow 2.5s infinite ease-in-out;
}
.neon-subtitle { color: #ff007f; text-align: center; font-size: 1.5rem; text-shadow: 0 0 5px #ff007f; margin-bottom: 40px; }
.login-box {
    background: rgba(25, 25, 40, 0.9); border: 2px solid #00f3ff; border-radius: 15px;
    padding: 30px; box-shadow: 0 0 20px rgba(0, 243, 255, 0.2); margin-top: 50px;
}
.deposit-warning {
    background: rgba(255, 0, 127, 0.15); border: 1px solid #ff007f; border-radius: 10px;
    padding: 15px; color: #ff007f; font-weight: bold; font-size: 1.1rem;
    text-align: center; margin-bottom: 20px; text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
}
.book-card { 
    background: rgba(25, 25, 40, 0.85); border: 2px solid #ff007f; border-radius: 15px; 
    padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(255, 0, 127, 0.2); 
    display: flex; flex-direction: column; justify-content: space-between;
    height: 620px; margin-bottom: 20px;
}
.book-img { width: 100%; height: 260px; object-fit: cover; border-radius: 10px; border: 1px solid #ff007f; margin-bottom: 15px; }
.book-title { color: #fff; font-size: 1.3rem; font-weight: bold; margin: 5px 0; min-height: 40px; display: flex; align-items: center; justify-content: center; }
.book-author { color: #00f3ff; font-size: 1rem; margin-bottom: 5px; }
.book-category { color: #ff007f; font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; border: 1px solid #ff007f; display: inline-block; padding: 2px 8px; border-radius: 10px;}
.book-desc { color: #a0a0b0; font-size: 0.85rem; margin-bottom: 10px; line-height: 1.4; min-height: 60px; overflow: hidden; }
.book-price { color: #39ff14; font-size: 1.3rem; font-weight: bold; text-shadow: 0 0 5px #39ff14; margin-top: auto; }
div.stButton > button { background-color: transparent !important; color: #00f3ff !important; border: 2px solid #00f3ff !important; border-radius: 8px !important; font-weight: bold !important; width: 100%; margin-top: 5px;}
div.stButton > button:hover { background-color: #00f3ff !important; color: #121212 !important; box-shadow: 0 0 25px #00f3ff !important; }
.whatsapp-btn { position: fixed; bottom: 20px; left: 20px; background-color: #25d366; color: white !important; padding: 15px 25px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 0 15px #25d366; z-index: 9999; display: flex; align-items: center; gap: 10px; transition: transform 0.3s; }
.whatsapp-btn:hover { transform: scale(1.1); box-shadow: 0 0 25px #25d366; color: white; }
</style>
"""
st.markdown(neon_style, unsafe_allow_html=True)

# 3. الدالة البرمجية الذكية لربط السيرفر بـ GitHub ومنع كراش الموقع
def github_action(path, action="LOAD", data_to_save=None):
    try:
        if "GITHUB_TOKEN" in st.secrets and "GITHUB_REPO" in st.secrets:
            token = st.secrets["GITHUB_TOKEN"]
            repo = st.secrets["GITHUB_REPO"]
            url = f"https://api.github.com/repos/{repo}/contents/{path}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            
            res = requests.get(url, headers=headers)
            sha = res.json()["sha"] if res.status_code == 200 else None
            
            if action == "LOAD":
                if res.status_code == 200:
                    content = base64.b64decode(res.json()["content"]).decode('utf-8')
                    return json.loads(content)
                return None
                
            elif action == "SAVE":
                encoded_content = base64.b64encode(json.dumps(data_to_save, ensure_ascii=False, indent=4).encode('utf-8')).decode('utf-8')
                payload = {"message": f"🔄 تحديث ملف {path}", "content": encoded_content}
                if sha: payload["sha"] = sha
                put_res = requests.put(url, headers=headers, json=payload)
                return put_res.status_code in [200, 201]
    except:
        pass
    return [] if action == "LOAD" else False
# 4. الأقسام الستة الكبرى المعتمدة لمنع العشوائية والسويقة
default_cats = [
    "روايات رعب وغموض", 
    "روايات فانتازيا وتشويق", 
    "تنمية ذاتية وعلم نفس", 
    "روايات أدبية وكلاسيكيات", 
    "كتب إسلامية ودينية", 
    "قصص بوليسية ومغامرات"
]

# 5. قاعدة البيانات الضخمة المنظمة للكتب المطلوبة بالكامل
default_books = [
    # --- رعب وغموض ---
    {"id": "h1", "title": "خوف", "author": "أسامة المسلم", "price": 140, "category": "روايات رعب وغموض", "description": "الولوج إلى العالم الآخر وكشف الأسرار المخفية بين عالمنا وعالم الجان.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.9},
    {"id": "h2", "title": "خوف 2", "author": "أسامة المسلم", "price": 150, "category": "روايات رعب وغموض", "description": "تكملة الصراع النفسي والفكري في عوالم الغموض والإثارة والجان.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.8},
    {"id": "h3", "title": "خوف 3", "author": "أسامة المسلم", "price": 160, "category": "روايات رعب وغموض", "description": "الجزء الثالث الحاسم من الملحمة النفسية الأكثر مبيعاً في الوطن العربي.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.7},
    {"id": "h4", "title": "نوح المذبوح", "author": "حسن الجندي", "price": 130, "category": "روايات رعب وغموض", "description": "رواية رعب شرقي مخيفة تدور حول اللعنات القديمة والطقوس المنسية.", "image": "https://images.unsplash.com/photo-1514849963640-9cc74b2a826f?q=80&w=400", "rating": 4.6},
    {"id": "h5", "title": "نادر فوده 1 (قبل البداية)", "author": "أحمد يونس", "price": 110, "category": "روايات رعب وغموض", "description": "المغامرة الأولى للصحفي نادر فودة مع عوالم ما وراء الطبيعة والمقابر.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    {"id": "h6", "title": "نادر فوده 2 (كسر الصنم)", "author": "أحمد يونس", "price": 115, "category": "روايات رعب وغموض", "description": "ملفات كسر الصنم وعودة الكيانات المظلمة لملاحقة نادر فودة وعائلته.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.6},
    {"id": "h7", "title": "نادر فوده 3 (الخوف)", "author": "أحمد يونس", "price": 120, "category": "روايات رعب وغموض", "description": "رحلة جديدة تحبس الأنفاس داخل سراديب الموت والجن المتربص بالبشر.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.8},
    {"id": "h8", "title": "نادر فوده 4 (عمارة الفزع)", "author": "أحمد يونس", "price": 125, "category": "روايات رعب وغموض", "description": "صراعات غامضة ومواجهة الكيانات السبعة في عمارة سكنية ملعونة.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.5},
    {"id": "h9", "title": "نادر فوده 5 (العين الثالثة)", "author": "أحمد يونس", "price": 130, "category": "روايات رعب وغموض", "description": "العين الثالثة وكشف المستور من القضايا الجنائية ذات الطابع الغيبي.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    {"id": "h10", "title": "نادر فوده 6 (الرصد)", "author": "أحمد يونس", "price": 135, "category": "روايات رعب وغموض", "description": "رواية الرعب والتشويق المستمر مع عالم الرصد الفرعوني وحراس المقابر.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.6},
    {"id": "h11", "title": "نادر فوده 7 (الجاثوم)", "author": "أحمد يونس", "price": 140, "category": "روايات رعب وغموض", "description": "قضايا وأسرار مثيرة من واقع ملفات ما وراء الطبيعة المخفية والجاثوم.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.8},
    {"id": "h12", "title": "نادر فوده 8 (الخادمة)", "author": "أحمد يونس", "price": 145, "category": "روايات رعب وغموض", "description": "قبل المعركة الأخيرة، مغامرة تكشف أوراقاً ظلت غامضة لسنوات في القرية.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    {"id": "h13", "title": "نادر فوده 9 (السيد)", "author": "أحمد يونس", "price": 150, "category": "روايات رعب وغموض", "description": "الجزء التاسع المنتظر من سلسلة الرعب الإذاعية الشهيرة خادمة الجن.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.9},
    {"id": "h14", "title": "سر الغرفة 207", "author": "أحمد خالد توفيق", "price": 110, "category": "روايات رعب وغموض", "description": "أحداث مرعبة وغير طبيعية تحدث داخل غرفة فندق يرفض مغادرتها الأحياء بسلام.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.9},
    {"id": "h15", "title": "الجزار", "author": "حسن الجندي", "price": 145, "category": "روايات رعب وغموض", "description": "رواية رعب وجريمة سيكولوجية معقدة عن الانتقام والعدالة والدم.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.8},
    {"id": "h16", "title": "لوكاندة في بير الوطاويط", "author": "أحمد مراد", "price": 160, "category": "روايات رعب وغموض", "description": "جريمة غموض تاريخية مشوقة في القاهرة القديمة تكشفها يوميات ومقابر سريّة.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.7},
    {"id": "h17", "title": "ابتسم فأنت ميت", "author": "حسن الجندي", "price": 120, "category": "روايات رعب وغموض", "description": "شقة سكنية بوسط القاهرة تخفي سراً مرعباً لكل من يحاول السكن بها.", "image": "https://images.unsplash.com/photo-1514849963640-9cc74b2a826f?q=80&w=400", "rating": 4.6},
    {"id": "h18", "title": "منزل أبو خطوة", "author": "حسن الجندي", "price": 125, "category": "روايات رعب وغموض", "description": "إثارة وغموض في بيت ريفي قديم تحوم حوله الشبهات واللعنات المتوارثة.", "image": "https://images.unsplash.com/photo-1514849963640-9cc74b2a826f?q=80&w=400", "rating": 4.5},
    {"id": "h19", "title": "حارة الجزار", "author": "عمرو المنوفي", "price": 115, "category": "روايات رعب وغموض", "description": "غموض يكتنف سلسلة جرائم قتل متتالية مرعبة في حي شعبي هادئ.", "image": "https://images.unsplash.com/photo-1514849963640-9cc74b2a826f?q=80&w=400", "rating": 4.4},
    {"id": "h20", "title": "جثة لذيذة", "author": "أحمد العايدي", "price": 110, "category": "روايات رعب وغموض", "description": "رواية ساخرة سوداء تمزج بين الرعب النفسي والتشويق المثير.", "image": "https://images.unsplash.com/photo-1514849963640-9cc74b2a826f?q=80&w=400", "rating": 4.3},
    {"id": "h21", "title": "إنهم يأتون ليلاً", "author": "تامر إبراهيم", "price": 130, "category": "روايات رعب وغموض", "description": "مجموعة قصصية مرعبة تحبس الأنفاس تدور أحداثها بالكامل في ظلام الليل.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.6},
    {"id": "h22", "title": "الهلكوت", "author": "محمد عصمت", "price": 120, "category": "روايات رعب وغموض", "description": "رواية رعب وإثارة لاهثة حول طقوس استدعاء قديمة تقلب الأمور رأسا على عقب.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.5},
    {"id": "h23", "title": "يحدث ليلاً في غرفة مظلمة", "author": "مروى جوهر", "price": 115, "category": "روايات رعب وغموض", "description": "أسرار غامضة وتحقيقات مثيرة في غرف مغلقة يكتنفها السحر والشعوذة.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.4},
    {"id": "h24", "title": "في حضرة الجان", "author": "حسن الجندي", "price": 140, "category": "روايات رعب وغموض", "description": "مواجهات مباشرة وحكايات مرعبة من كتابات المخطوطات القديمة وعالم الجان.", "image": "https://images.unsplash.com/photo-1514849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    {"id": "h25", "title": "سرداب قصر البارون", "author": "عمرو المنوفي", "price": 125, "category": "روايات رعب وغموض", "description": "رواية رعب تعتمد على الأساطير المصرية حول قصر البارون الشهير وسراديبه الكامنة.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.6},
    {"id": "h26", "title": "ليلة ظهور القرين", "author": "محمد رجب", "price": 120, "category": "روايات رعب وغموض", "description": "عندما يواجه الإنسان قرينه في ليلة شتوية ممطرة، صراع البقاء المرعب.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.3},

    # --- فانتازيا وتشويق ---
    {"id": "f1", "title": "أرض زيكولا", "author": "عمرو عبد الحميد", "price": 130, "category": "روايات فانتازيا وتشويق", "description": "عالم غريب يتعامل بوحدات الذكاء بدلاً من النقود، والفقير يُذبح!", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.9},
    {"id": "f2", "title": "أمواج أكما", "author": "عمرو عبد الحميد", "price": 140, "category": "روايات فانتازيا وتشويق", "description": "الجزء الثالث من ملحمة قواعد جارتين وصراع العقول والحرية المنتظرة.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.8},
    {"id": "f3", "title": "دقات الشامو", "author": "عمرو عبد الحميد", "price": 135, "category": "روايات فانتازيا وتشويق", "description": "قواعد جارتين تشتعل بالصراعات والأسرار المخفية للنسل الجديد المتمرد.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.7},
    {"id": "f4", "title": "قواعد جارتين", "author": "عمرو عبد الحميد", "price": 130, "category": "روايات فانتازيا وتشويق", "description": "بداية الثلاثية الأسطورية الخيالية عن مجتمع تحكمه قوانين قاسية وعجيبة.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.8},
    {"id": "f5", "title": "إيكادولي", "author": "حنان لاشين", "price": 140, "category": "روايات فانتازيا وتشويق", "description": "سفر في مملكة البلاغة، حيث تحلق الكلمات وتجسد الروايات قيم النبل والخير.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.9},
    {"id": "f6", "title": "جومانه", "author": "حنان لاشين", "price": 145, "category": "روايات فانتازيا وتشويق", "description": "رحلة ملحمية جديدة داخل مملكة البلاغة بأسلوب ساحر ومميز يجذب العقول.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.7},
    {"id": "f7", "title": "ياجوج وماجوج", "author": "عمرو المنوفي", "price": 120, "category": "روايات فانتازيا وتشويق", "description": "فانتازيا تاريخية مثيرة مستوحاة من الأساطير والقصص الدينية القديمة.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.5},
    {"id": "f8", "title": "يوتوبيا", "author": "أحمد خالد توفيق", "price": 100, "category": "روايات فانتازيا وتشويق", "description": "رواية ديستوبيا مستقبلية مرعبة ومثيرة عن انقسام المجتمع لطبقتين متناقضتين.", "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?q=80&w=400", "rating": 4.8},
    {"id": "f9", "title": "لارسيا", "author": "أحمد آل حمدان", "price": 150, "category": "روايات فانتازيا وتشويق", "description": "صراعات العروش الخيالية والسحر الأسود في ملحمة روائية مبهرة.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.7},
    {"id": "f10", "title": "المرتد", "author": "حسن الجندي", "price": 135, "category": "روايات فانتازيا وتشويق", "description": "الجزء الثاني من رواية مخطوطة ابن إسحاق، إثارة وتداخل عوالم خيالية.", "image": "https://images.unsplash.com/photo-1614849963640-9cc74b2a826f?q=80&w=400", "rating": 4.8},
    {"id": "f12", "title": "أرسس 2", "author": "أحمد آل حمدان", "price": 150, "category": "روايات فانتازيا وتشويق", "description": "تكملة قصة الكائن الأخير والمواجهة الكبرى لحماية الكوكب الخيالي.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.7},

    # --- تنمية ذاتية وعلم نفس ---
    {"id": "s1", "title": "نظرية الفستق التاني", "author": "فهد عامر الأحمدي", "price": 160, "category": "تنمية ذاتية وعلم نفس", "description": "استكمال لمقالات تطوير الذات وطرق التفكير الإيجابي وتعديل السلوك اليومي.", "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=400", "rating": 4.8},
    {"id": "s2", "title": "العادات الذرية", "author": "جيمس كلير", "price": 190, "category": "تنمية ذاتية وعلم نفس", "description": "إطار عمل لبناء العادات الحسنة والتخلص من السيئة عبر خطوات يومية صغيرة.", "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=400", "rating": 4.9},
    {"id": "s3", "title": "فن اللامبالاة", "author": "مارك مانسون", "price": 150, "category": "تنمية ذاتية وعلم نفس", "description": "دليل يعلمك كيف تتوقف عن الاهتمام بأشياء لا تستحق لتعيش حياة هادئة ومستقرة.", "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=400", "rating": 4.7},
    {"id": "s4", "title": "محاط بالحمقى", "author": "توماس إريكسون", "price": 180, "category": "تنمية ذاتية وعلم نفس", "description": "فهم الأنماط الأربعة للشخصيات البشرية (الألوان) وكيفية التعامل الذكي معهم.", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400", "rating": 4.6},
    {"id": "s5", "title": "عقدك النفسية سجنك للأبد", "author": "يوسف الحسني", "price": 165, "category": "تنمية ذاتية وعلم نفس", "description": "كشف الأقنعة النفسية وتحليل العلاقات الإنسانية من منظور واقعي طبي مدعم بالأمثلة.", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400", "rating": 4.8},
    {"id": "s6", "title": "جلسات نفسية", "author": "محمد إبراهيم", "price": 120, "category": "تنمية ذاتية وعلم نفس", "description": "رسائل ودعم نفسي لترميم الذات والسلام الداخلي والتصالح مع مخاوف الحياة.", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400", "rating": 4.8},
    {"id": "s7", "title": "أبي الذي أكره", "author": "عماد رشاد عثمان", "price": 140, "category": "تنمية ذاتية وعلم نفس", "description": "كتاب رائع يناقش التعافي من صدمات التنشئة والروابط الوالدية السامة والشفاء منها.", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400", "rating": 4.9},
    {"id": "s8", "title": "الخروج عن النص من جديد", "author": "محمد طه", "price": 130, "category": "تنمية ذاتية وعلم نفس", "description": "دعوة لاكتشاف الذات الحقيقية والتخلص من الأدوار المزيفة المفروضة عليك مجتمعياً.", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400", "rating": 4.7},
    {"id": "s9", "title": "قبل أن تبرد القهوة (الأخضر)", "author": "توشيكازو كواغوتشي", "price": 135, "category": "تنمية ذاتية وعلم نفس", "description": "رواية يابانية بنكهة نفسية عن مقهى يتيح فرصة السفر عبر الزمن بشروط صارمة.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.8},
    {"id": "s10", "title": "قبل أن تبرد القهوة (الأزرق)", "author": "توشيكازو كواغوتشي", "price": 135, "category": "تنمية ذاتية وعلم نفس", "description": "الجزء الثاني واستكمال للحكايات الإنسانية المؤثرة لمن يتمنون العودة للماضي لدقائق.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.7},
    {"id": "s11", "title": "قبل أن تبرد القهوة (الأصفر)", "author": "توشيكازو كواغوتشي", "price": 135, "category": "تنمية ذاتية وعلم نفس", "description": "رحلة نفسية جديدة في إصدار متميز يطرح أسئلة فلسفية حول الخيارات والفرص الصعبة.", "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=400", "rating": 4.6},
    {"id": "s12", "title": "فن الكلام", "author": "إيهاب فكري", "price": 110, "category": "تنمية ذاتية وعلم نفس", "description": "دليل عملي لاكتساب مهارات الرد، والحديث الدبلوماسي، والذكاء الاجتماعي الراقي.", "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=400", "rating": 4.6},
    {"id": "s14", "title": "أسرار عقل المليونير", "author": "تي هارف إيكر", "price": 170, "category": "تنمية ذاتية وعلم نفس", "description": "إعادة ضبط وتغيير طريقة تفكيرك المالي للتخلص من المعتقدات المقيدة للثراء.", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400", "rating": 4.8},

    # --- روايات أدبية وكلاسيكيات ---
    {"id": "l1", "title": "زقاق المدق", "author": "نجيب محفوظ", "price": 95, "category": "روايات أدبية وكلاسيكيات", "description": "من أشهر كلاسيكيات الأدب العربي التي تصور الحياة في حواري القاهرة القديمة.", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400", "rating": 4.9},
    {"id": "l2", "title": "ثرثرة فوق النيل", "author": "نجيب محفوظ", "price": 90, "category": "روايات أدبية وكلاسيكيات", "description": "نقد لاذع للأوضاع الاجتماعية والسياسية عبر جلسات العوامة الشهيرة الساخرة.", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400", "rating": 4.8},
    {"id": "l3", "title": "الخيميائي", "author": "باولو كويلو", "price": 110, "category": "روايات أدبية وكلاسيكيات", "description": "رواية رمزية عالمية تحث الإنسان على تتبع شغفه وتحقيق أسطورته الشخصية.", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400", "rating": 4.7},
    {"id": "l4", "title": "الليالي البيضاء", "author": "فيودور دوستويفسكي", "price": 100, "category": "روايات أدبية وكلاسيكيات", "description": "رواية عاطفية كلاسيكية شهيرة عن الحب، الأحلام، والوحدة في مدينة بطرسبرغ.", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400", "rating": 4.9},
    {"id": "l5", "title": "عائد إلى حيفا", "author": "غسان كنفاني", "price": 85, "category": "روايات أدبية وكلاسيكيات", "description": "أدب مقاوم يجسد مأساة الهوية والوطن عبر رحلة عائلة فلسطينية تبحث عن طفلها المفقود.", "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400", "rating": 4.9},

    # --- كتب إسلامية ودينية ---
    {"id": "r1", "title": "لأنك الله", "author": "علي بن جابر الفيفي", "price": 90, "category": "كتب إسلامية ودينية", "description": "رحلة روحانية دافئة في معاني أسماء الله الحسنى وكيف نعيش بها في تفاصيل يومنا.", "image": "https://images.unsplash.com/photo-1585036156171-384164a8c675?q=80&w=400", "rating": 4.9},
    {"id": "r2", "title": "فاتتني صلاة", "author": "إسلام جمال", "price": 120, "category": "كتب إسلامية ودينية", "description": "كتاب يلهمك للحفاظ على الصلاة ويوضح لك الأسرار النفسية والعملية للالتزام المستمر.", "image": "https://images.unsplash.com/photo-1585036156171-384164a8c675?q=80&w=400", "rating": 4.9},
    {"id": "r3", "title": "مع النبي", "author": "أدهم شرقاوي", "price": 130, "category": "كتب إسلامية ودينية", "description": "قصص نبوية شريفة بأسلوب أدبي وعظي يملأ القلب بالدروس والعبر التربوية الميسرة.", "image": "https://images.unsplash.com/photo-1585036156171-384164a8c675?q=80&w=400", "rating": 4.8},

    # --- قصص بوليسية ومغامرات ---
    {"id": "d1", "title": "ثم لم يبقَ أحد", "author": "أجاثا كريستي", "price": 110, "category": "قصص بوليسية ومغامرات", "description": "الرواية البوليسية الأكثر مبيعاً في التاريخ: 10 غُرباء في جزيرة معزولة ويموتون تلو الآخر.", "image": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=400", "rating": 4.9},
    {"id": "d2", "title": "الياقوتة الزرقاء", "author": "أرثر كونان دويل", "price": 85, "category": "قصص بوليسية ومغامرات", "description": "قضية ذكية ومثيرة للمحقق العبقري شيرلوك هولمز في البحث عن جوهرة ثمينة مسروقة داخل إوزة.", "image": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=400", "rating": 4.7}
    ]
# 6. تهيئة وفحص الـ Session State لمنع اختفاء البيانات ودعم الربط الفوري بجيت هب
if "books" not in st.session_state:
    loaded_books = github_action("books.json", "LOAD")
    st.session_state.books = loaded_books if loaded_books else default_books

if "categories" not in st.session_state:
    loaded_cats = github_action("categories.json", "LOAD")
    st.session_state.categories = loaded_cats if loaded_cats else default_cats

if "orders" not in st.session_state:
    loaded_orders = github_action("orders.json", "LOAD")
    st.session_state.orders = loaded_orders if loaded_orders else []

if "comments" not in st.session_state:
    loaded_comments = github_action("comments.json", "LOAD")
    st.session_state.comments = loaded_comments if isinstance(loaded_comments, dict) else {}

if "users" not in st.session_state:
    loaded_users = github_action("users.json", "LOAD")
    st.session_state.users = loaded_users if loaded_users else []

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_role" not in st.session_state: st.session_state.user_role = "user"
if "user_info" not in st.session_state: st.session_state.user_info = {"name": "", "whatsapp": ""}
if "cart" not in st.session_state: st.session_state.cart = []

# ==================== [ فحص الأمان: حظر العميل الفوري والطرد التلقائي ] ====================
if st.session_state.logged_in and st.session_state.user_role == "user":
    current_user_check = next((u for u in st.session_state.users if u["whatsapp"] == st.session_state.user_info["whatsapp"]), None)
    if current_user_check:
        if current_user_check["status"] == "محظور":
            st.error("🚫 عذراً، لقد تم حظر حسابك بالكامل من دخول المتجر بواسطة الإدارة للإخلال بالشروط.")
            st.session_state.logged_in = False
            st.stop()
        elif current_user_check["status"] == "معلق":
            st.warning("⏳ حسابك معلق مؤقتاً لمراجعة الطلبات السابقة من قبل الإدارة، تواصل معنا لتفعيله.")
            st.session_state.logged_in = False
            st.stop()

# ==================== [ شاشة تسجيل الدخول والـ Backdoor للأدمن ] ====================
if not st.session_state.logged_in:
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="neon-subtitle">سجل دخولك لتصفح وحجز أحدث الروايات والكتب الحصرية</div>', unsafe_allow_html=True)
    
    col_login, _ = st.columns([2, 1])
    with col_login:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        reg_name = st.text_input("👤 الاسم الكامل:")
        
        if reg_name.strip() == "admin_login":
            admin_pass = st.text_input("🔑 كلمة مرور الأدمن السري:", type="password")
            if st.button("دخول الإدارة السرية 🔐"):
                if admin_pass == "admin123":
                    st.session_state.user_role = "admin"
                    st.session_state.logged_in = True
                    st.success("مرحباً بك يا مدير المتجر!")
                    st.rerun()
                else: 
                    st.error("كلمة المرور غير صحيحة!")
        else:
            reg_phone = st.text_input("📞 رقم الواتساب الخاص بك للتأكيد:")
            if st.button("دخول المتجر الآن 🛒"):
                if reg_name.strip() and reg_phone.strip():
                    user_match = next((u for u in st.session_state.users if u["whatsapp"] == reg_phone.strip()), None)
                    
                    if user_match:
                        if user_match["status"] == "محظور":
                            st.error("🚫 هذا الحساب محظور تماماً من دخول المتجر!")
                        elif user_match["status"] == "معلق":
                            st.warning("⏳ حسابك معلق حالياً، تواصل مع الإدارة.")
                        else:
                            st.session_state.user_info = {"name": user_match["name"], "whatsapp": user_match["whatsapp"]}
                            st.session_state.user_role = "user"
                            st.session_state.logged_in = True
                            st.rerun()
                    else:
                        new_u = {"name": reg_name.strip(), "whatsapp": reg_phone.strip(), "status": "نشط"}
                        st.session_state.users.append(new_u)
                        github_action("users.json", "SAVE", st.session_state.users)
                        
                        st.session_state.user_info = {"name": reg_name.strip(), "whatsapp": reg_phone.strip()}
                        st.session_state.user_role = "user"
                        st.session_state.logged_in = True
                        st.rerun()
                else: 
                    st.error("برجاء إدخال اسمك ورقم واتساب صحيح لخدمتك!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
# ==================== [ القائمة الجانبية للتنقل ] ====================
page_options = ["🔐 لوحة الإدارة", "🛒 المتجر الإلكتروني"] if st.session_state.user_role == "admin" else ["🛒 المتجر الإلكتروني"]
menu = st.sidebar.selectbox("🧭 انتقل إلى صفحة:", page_options)

if st.sidebar.button("🚪 تسجيل الخروج من الحساب"):
    st.session_state.logged_in = False
    st.session_state.user_role = "user"
    st.session_state.cart = []
    st.rerun()

# ==================== [ صفحة المتجر الإلكتروني للجمهور ] ====================
if menu == "🛒 المتجر الإلكتروني":
    st.markdown('<div class="neon-title">World of Books 📚</div>', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([2, 1])
    search_query = col_s1.text_input("🔍 ابحث عن اسم رواية أو مؤلف كتاب:")
    selected_category = col_s2.selectbox("📂 تصفية الأقسام:", ["الكل"] + st.session_state.categories)
    
    filtered_books = [b for b in st.session_state.books if (search_query.lower() in b["title"].lower() or search_query.lower() in b["author"].lower()) and (selected_category == "الكل" or b["category"] == selected_category)]

    if not filtered_books:
        st.info("لا توجد كتب مطابقة لبحثك حالياً في هذا القسم.")
    else:
        cols = st.columns(3)
        for index, book in enumerate(filtered_books):
            with cols[index % 3]:
                st.markdown(f"""
                <div class="book-card">
                    <img src="{book['image']}" class="book-img">
                    <div class="book-title">{book['title']}</div>
                    <div class="book-author">المؤلف: {book['author']}</div>
                    <div><span class="book-category">{book['category']}</span></div>
                    <div class="book-desc">{book.get('description', 'لا يوجد وصف متاح لهذا الكتاب.')}</div>
                    <div style="color: gold; font-size: 1.1rem; margin-bottom: 5px;">⭐ {book.get('rating', 5.0)}/5.0</div>
                    <div class="book-price">{book['price']} جنيه</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("أضف إلى السلة 🛒", key=f"add_{book['id']}"):
                    st.session_state.cart.append(book)
                    st.toast(f"تم إضافة {book['title']} إلى سلتك!")
                
                with st.expander("💬 آراء القراء والتقييم الحقيقي"):
                    new_rating = st.slider("قيم الكتاب بالنجوم:", 1.0, 5.0, float(book.get('rating', 5.0)), 0.1, key=f"rate_{book['id']}")
                    if st.button("حفظ التقييم ⭐", key=f"btn_rate_{book['id']}"):
                        book['rating'] = new_rating
                        github_action("books.json", "SAVE", st.session_state.books)
                        st.toast("تم حفظ تقييمك بنجاح في قاعدة البيانات!")
                        st.rerun()
                        
                    bid = book["id"]
                    if bid not in st.session_state.comments: st.session_state.comments[bid] = []
                    for c in st.session_state.comments[bid]:
                        st.markdown(f"👤 **{c['user']}**: {c['text']}")
                    
                    new_comment = st.text_input("اكتب مراجعة وتعليق على الرواية:", key=f"comm_{bid}")
                    if st.button("نشر المراجعة 🚀", key=f"btn_comm_{bid}") and new_comment.strip():
                        st.session_state.comments[bid].append({"user": st.session_state.user_info["name"], "text": new_comment.strip()})
                        github_action("comments.json", "SAVE", st.session_state.comments)
                        st.rerun()

    # سلة المشتريات التفاعلية وحجز العربون
    if len(st.session_state.cart) > 0:
        st.markdown("---")
        st.markdown('<div class="neon-subtitle" style="text-align: right;">🛒 سلة المشتريات الحالية وعملية الحجز</div>', unsafe_allow_html=True)
        total_price = sum(item['price'] for item in st.session_state.cart)
        st.success(f"لديك {len(st.session_state.cart)} كتب في السلة | إجمالي حساب الكتب: {total_price} جنيه مصري")
        st.markdown('<div class="deposit-warning">⚠️ تنبيه أمان: لإتمام شحن الكتب المحجوزة، يجب دفع (عربون بسيط) عبر الواتساب لتأكيد الحجز الفعلي ومكافحة الحسابات الوهمية!</div>', unsafe_allow_html=True)
        
        with st.form("checkout_form"):
            address = st.text_input("🏠 عنوان الشحن بالتفصيل (المحافظة/المدينة/الشارع):")
            if st.form_submit_button("تأكيد الطلب وحجز الروايات رسمياً 🚚") and address.strip():
                order_data = {
                    "books": [b['title'] for b in st.session_state.cart], 
                    "total_price": total_price, 
                    "name": st.session_state.user_info["name"], 
                    "phone": st.session_state.user_info["whatsapp"], 
                    "address": address.strip()
                }
                st.session_state.orders.append(order_data)
                github_action("orders.json", "SAVE", st.session_state.orders)
                st.session_state.cart = []
                st.success("🎉 تم تسجيل طلبك بنجاح دائم على السيرفر، يرجى الضغط على زر الواتساب أسفله لإرسال العربون وتأكيد الشحن!")
                st.rerun()
                # ==================== [ صفحة الإدارة والتحكم الشاملة (الأدمن) ] ====================
elif menu == "🔐 لوحة الإدارة":
    st.title("🔐 لوحة تحكم وتوجيه المدير المسؤول")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📦 الأوردرات", "➕ إضافة كتاب", "📁 إدارة الأقسام", "✏️ تعديل الكتب", "👤 إدارة المستخدمين"])
    
    with tab1:
        st.subheader("📦 طلبات حجز الكتب الواردة المحفوظة على GitHub")
        if not st.session_state.orders: 
            st.info("لا توجد طلبات شراء مسجلة حالياً.")
        for i, order in enumerate(st.session_state.orders):
            with st.expander(f"أوردر رقم {i+1} - للعميل: {order['name']}"):
                st.write(f"**📞 واتساب العميل للتواصل:** {order['phone']}")
                st.write(f"**🏠 عنوان التوصيل:** {order['address']}")
                st.write(f"**📚 الكتب المطلوبة للطلب:** {', '.join(order['books'])}")
                st.write(f"**💰 الحساب الإجمالي المستحق:** {order['total_price']} جنيه مصري")

    with tab2:
        st.subheader("➕ إضافة كتاب أو رواية جديدة للمتجر")
        with st.form("add_book_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            t = col1.text_input("اسم الكتاب / الرواية:")
            a = col2.text_input("اسم الكاتب / المؤلف:")
            cat = col1.selectbox("قسم وتصنيف الكتاب:", st.session_state.categories)
            p = col2.number_input("سعر الكتاب الحقيقي بالجنيه:", min_value=1, step=5)
            desc = st.text_area("وصف مختصر وشيق لقصة الرواية:")
            img = st.file_uploader("صورة الغلاف الحقيقية للكتاب:", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("إدخال وحفظ الكتاب على جيت هب 🚀") and t and img:
                base64_img = base64.b64encode(img.getvalue()).decode()
                src = f"data:image/{img.type.split('/')[-1]};base64,{base64_img}"
                st.session_state.books.append({
                    "id": f"b{len(st.session_state.books)+1}", 
                    "title": t.strip(), 
                    "author": a.strip(), 
                    "price": p, 
                    "category": cat, 
                    "description": desc.strip(), 
                    "image": src, 
                    "rating": 5.0
                })
                github_action("books.json", "SAVE", st.session_state.books)
                st.success("تم رفع الرواية وتحديث قاعدة بيانات GitHub بنجاح وأمان دائم!")
                st.rerun()

    with tab3:
        st.subheader("📁 إضافة وإدارة الأقسام المعتمدة")
        new_cat = st.text_input("اكتب اسم القسم الجديد المراد تعميمه:")
        if st.button("تأكيد حفظ القسم الجديد 📁") and new_cat.strip():
            if new_cat.strip() not in st.session_state.categories:
                st.session_state.categories.append(new_cat.strip())
                github_action("categories.json", "SAVE", st.session_state.categories)
                st.success("تم حفظ وتعميم القسم الجديد في الفلاتر!")
                st.rerun()
        st.write("الأقسام الحالية المعتمدة لحماية النظام من العشوائية:", ", ".join(st.session_state.categories))

    with tab4:
        st.subheader("✏️ تعديل بيانات وأسعار وغلاف الكتب الحالية")
        selected_book_title = st.selectbox("اختر الرواية التي تريد تعديلها حالياً:", [b["title"] for b in st.session_state.books])
        book_to_edit = next((b for b in st.session_state.books if b["title"] == selected_book_title), None)
        
        if book_to_edit:
            with st.form("edit_book_form_secure"):
                new_t = st.text_input("تعديل الاسم الرئيسي للرواية:", value=book_to_edit["title"])
                new_a = st.text_input("تعديل اسم المؤلف:", value=book_to_edit["author"])
                new_cat = st.selectbox("تعديل القسم:", st.session_state.categories, index=st.session_state.categories.index(book_to_edit["category"]) if book_to_edit["category"] in st.session_state.categories else 0)
                new_desc = st.text_area("تعديل الوصف والقصة التخيلية:", value=book_to_edit.get("description", ""))
                new_p = st.number_input("تعديل سعر البيع بالجنيه:", min_value=1, value=int(book_to_edit["price"]))
                
                st.write("🖼️ غلاف الرواية الحالي في المتجر:")
                st.image(book_to_edit["image"], width=130)
                new_img = st.file_uploader("رفع غلاف وصورة جديدة كلياً (اتركه فارغاً للاحتفاظ بالصورة الحالية):", type=["png", "jpg", "jpeg"])
                
                if st.form_submit_button("تحديث البيانات وحفظ التغييرات نهائياً 💾"):
                    book_to_edit["title"] = new_t.strip()
                    book_to_edit["author"] = new_a.strip()
                    book_to_edit["category"] = new_cat
                    book_to_edit["description"] = new_desc.strip()
                    book_to_edit["price"] = new_p
                    if new_img:
                        base64_img = base64.b64encode(new_img.getvalue()).decode()
                        book_to_edit["image"] = f"data:image/{new_img.type.split('/')[-1]};base64,{base64_img}"
                    
                    github_action("books.json", "SAVE", st.session_state.books)
                    st.success("تم تحديث البيانات بالكامل وحفظها دافورياً على GitHub!")
                    st.rerun()

    with tab5:
        st.subheader("👤 إدارة حسابات المشترين وصلاحيات الحظر والتعليق")
        st.markdown("تحكم كامل بحسابات العملاء لمكافحة الأرقام المزعجة والطلبات الوهمية:")
        
        if not st.session_state.users:
            st.info("لم يسجل أي عميل أو مستخدم في النظام حتى الآن.")
        else:
            for idx, user in enumerate(st.session_state.users):
                with st.container():
                    col_u1, col_u2, col_u3 = st.columns([3, 2, 1])
                    col_u1.write(f"👤 **الاسم:** {user['name']} | 📞 **واتساب:** `{user['whatsapp']}`")
                    
                    status_options = ["نشط", "معلق", "محظور"]
                    current_idx = status_options.index(user.get("status", "نشط"))
                    
                    new_status = col_u2.selectbox(f"تعديل صلاحية {user['name']}:", status_options, index=current_idx, key=f"status_select_{idx}")
                    
                    if col_u3.button("حفظ التعديل 💾", key=f"save_user_btn_{idx}"):
                        user["status"] = new_status
                        github_action("users.json", "SAVE", st.session_state.users)
                        st.success(f"تم تغيير حالة {user['name']} إلى ({new_status}) بنجاح!")
                        st.rerun()
                st.markdown("---")

# زر الواتساب العائم في زاوية الشاشة للتواصل والدعم
whatsapp_url = "https://wa.me/201149243249?text=مرحباً%20بإدارة%20مكتبة%20World%20of%20Books%20أود%20تأكيد%20حجز%20الكتب%20ودفع%20العربون"
st.markdown(f'<a href="{whatsapp_url}" class="whatsapp-btn" target="_blank">💬 تواصل وتأكيد دفع العربون</a>', unsafe_allow_html=True)
