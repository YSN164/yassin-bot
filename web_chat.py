import streamlit as st
import google.generativeai as genai

# 1. إعدادات واجهة الموقع
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("أهلاً بك في موقع ياسين للذكاء الاصطناعي - النسخة المستقرة")

# 2. تفعيل مفتاح الـ API من الخزنة (Secrets)
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("المفتاح غير موجود! تأكد من إضافة GENAI_API_KEY في إعدادات Streamlit.")
    st.stop()

# 3. إعداد ذاكرة الشات والموديل
if "messages" not in st.session_state:
    st.session_state.messages = []

# استخدمنا الموديل ده لأنه الأضمن لتجنب خطأ 404
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة إدخال المستخدم
if prompt := st.chat_input("اسألني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # طلب الرد من الموديل
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # لو لسه فيه مشكلة هيظهر لنا السبب بوضوح هنا
        st.error(f"حصلت مشكلة بسيطة: {e}")
