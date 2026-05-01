import streamlit as st
from google import genai
import time

# 1. إعداد الصفحة
st.set_page_config(
    page_title="AI Yassin Bot",
    page_icon="🤖",
    layout="centered"
)

# 2. تصميم الواجهة (CSS)
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. العنوان والجانب الجانبي
st.title("🤖 AI Yassin Bot")
st.caption("نسخة احترافية شغالة 🔥")

with st.sidebar:
    st.header("⚙️ التحكم")
    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("Made by Yassin 😎")

# 4. إعداد الـ API والـ Client
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    client = genai.Client(api_key=api_key) 
else:
    st.error("حط API KEY في Secrets")
    st.stop()

# 5. الذاكرة (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. عرض الرسائل القديمة
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 7. منطقة الإدخال والرد
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()

        try:
            # ✅ التعديل الذهبي: استخدمنا gemini-1.5-flash لضمان العمل على النسخة المستقرة
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )

            full_text = response.text if response.text else "مفيش رد من الموديل 😅"

            # تأثير الكتابة التدريجي
            displayed = ""
            for char in full_text:
                displayed += char
                message_placeholder.markdown(displayed + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_text
            })

        except Exception as e:
            # عرض الخطأ بشكل مبسط
            st.error(f"❌ حصل خطأ: {e}")
