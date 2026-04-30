import streamlit as st
import google.generativeai as genai

# 1. إعدادات واجهة الموقع
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("أهلاً بك في موقع ياسين للذكاء الاصطناعي")

# 2. تفعيل مفتاح الـ API من الخزنة (Secrets)
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("المفتاح غير موجود في Secrets! تأكد من إضافته في إعدادات Streamlit.")
    st.stop()

# 3. إعداد ذاكرة الشات والموديل
if "messages" not in st.session_state:
    st.session_state.messages = []

# استخدمنا gemini-pro لأنه الأكثر استقراراً لتجنب خطأ 404
model = genai.GenerativeModel('gemini-pro')

# 4. عرض الرسائل السابقة في المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطقة إدخال المستخدم ومعالجة الرد
if prompt := st.chat_input("اسألني أي حاجة..."):
    # إضافة رسالة المستخدم للذاكرة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # محاولة جلب الرد من جوجل
    try:
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            # حفظ رد البوت في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # عرض رسالة خطأ بسيطة لو حصلت مشكلة في الاتصال
        st.error(f"حصلت مشكلة بسيطة في الرد: {e}")
