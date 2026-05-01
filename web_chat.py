import streamlit as st
from google import genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("نسخة شغالة 100% 🚀")

# 2. API Key
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
else:
    st.error("حط API KEY في Secrets الأول!")
    st.stop()

# 3. إعداد العميل
client = genai.Client(api_key=api_key)

# 4. تخزين المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. إدخال المستخدم
if prompt := st.chat_input("اسأل ياسين بوت..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            reply = response.text
            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

    except Exception as e:
        st.error(f"حصل خطأ: {e}")
