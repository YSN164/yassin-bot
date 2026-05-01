import streamlit as st
import google.generativeai as genai
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")

# 2. إعداد الـ API (تأكد إن الكود ده شغال)
if "GENAI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GENAI_API_KEY"])
    # الموديل هنا بدون إصدارات بيتا
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing!")
    st.stop()

st.title("🤖 AI Yassin Bot")

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. منطقة الإدخال
if prompt := st.chat_input("اكتب هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # الحركة دي بتجبره يشتغل بعيداً عن الـ v1beta
            response = model.generate_content(prompt)
            
            if response.text:
                full_text = response.text
                st.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
            else:
                st.error("الموديل مرفعش رد.")
        except Exception as e:
            st.error(f"Error: {e}")
