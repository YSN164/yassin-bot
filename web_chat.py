import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("أهلاً بك في موقع ياسين للذكاء الاصطناعي")

# 2. تفعيل المفتاح
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# 3. إعداد الرسائل والموديل (تأكد من كتابة gemini-1.5-flash صح)
if "messages" not in st.session_state:
    st.session_state.messages = []

# استخدمنا الموديل ده لأنه الأكثر استقراراً
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 4. عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة الإدخال
if prompt := st.chat_input("اسألني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حصلت مشكلة بسيطة: {e}")
