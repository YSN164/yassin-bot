import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("أهلاً بك في نسخة الطوارئ النهائية")

# 2. الحصول على الـ API Key من الـ Secrets
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("المفتاح غير موجود في Secrets! لازم تروح لـ Advanced Settings وتضيفه.")
    st.stop()

# 3. محاولة تشغيل الموديل بأكثر من طريقة لضمان النجاح
@st.cache_resource
def load_model():
    # بنجرب أكتر من موديل عشان لو واحد مش مدعوم التاني يشتغل
    model_names = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-1.5-flash']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # تجربة وهمية للتأكد إن الموديل شغال
            m.generate_content("test") 
            return m
        except:
            continue
    return None

model = load_model()

if model is None:
    st.error("السيرفر مش قادر يوصل لموديلات جوجل. اتأكد إنك حاطط google-generativeai==0.8.3 في ملف requirements.txt وعملت Reboot.")
    st.stop()

# 4. الذاكرة وعرض الشات
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال
if prompt := st.chat_input("اسأل ياسين بوت..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حصل خطأ أثناء الرد: {e}")
