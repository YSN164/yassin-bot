import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")

# التأكد من المفتاح
if "GENAI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GENAI_API_KEY"])
else:
    st.error("المفتاح ناقص في الـ Secrets!")
    st.stop()

# إعداد الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- الضربة القاضية: تحديد النسخة المستقرة يدوياً ---
# استخدمنا gemini-pro لأنه الأكثر استقراراً مع النسخ القديمة
model = genai.GenerativeModel(model_name='gemini-pro') 

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # بنجبر الموديل يشتغل حتى لو النسخة v1beta
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # لو فشل، هنجرب نغير اسم الموديل لنسخة أقدم مضمونة
        try:
             model_backup = genai.GenerativeModel('models/gemini-pro')
             response = model_backup.generate_content(prompt)
             st.markdown(response.text)
             st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
             st.error("السيرفر محتاج تحديث للمكتبات، اتأكد من ملف requirements.txt")
