import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("أهلاً بك في موقع ياسين للذكاء الاصطناعي")

# 2. سحب المفتاح وتفعيل جوجل (دي الخطوة اللي كانت ناقصة)
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. تجهيز الموديل والرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

model = genai.GenerativeModel('gemini-1.5-flash')

# 4. عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الدردشة
if prompt := st.chat_input("اسألني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
