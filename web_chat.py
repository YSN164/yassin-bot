import streamlit as st
from google import genai
import time

# ====== إعداد الصفحة ======
st.set_page_config(
    page_title="AI Yassin Bot",
    page_icon="🤖",
    layout="centered"
)

# ====== STYLE ======
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== HEADER ======
st.title("🤖 AI Yassin Bot")
st.caption("نسخة احترافية شغالة 🔥")

# ====== SIDEBAR ======
with st.sidebar:
    st.header("⚙️ التحكم")

    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("Made by Yassin 😎")

# ====== API KEY ======
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
else:
    st.error("حط API KEY في Secrets")
    st.stop()

# ====== CLIENT ======
response = client.models.generate_content(
    model="gemini-1.0-pro",
    contents=prompt
)

# ====== MEMORY ======
if "messages" not in st.session_state:
    st.session_state.messages = []

# ====== عرض الرسائل ======
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ====== INPUT ======
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()

        try:
            # ✅ موديل مضمون شغال
            response = client.models.generate_content(
                model="gemini-1.5-flash-latest",
                contents=prompt
            )

            full_text = response.text if response.text else "مفيش رد من الموديل 😅"

            # ====== تأثير الكتابة ======
            displayed = ""
            for char in full_text:
                displayed += char
                message_placeholder.markdown(displayed)
                time.sleep(0.01)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_text
            })

        except Exception as e:
            st.error(f"❌ حصل خطأ: {e}")
