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
