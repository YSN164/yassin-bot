import streamlit as st
import google.generativeai as genai
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
st.caption("النسخة النهائية المستقرة 🔥")

with st.sidebar:
    st.header("⚙️ التحكم")
    if st.button("🗑️ مسح الشات"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("Made by Yassin 😎")

# 4. إعداد الـ API والـ الموديل (رجعنا للمكتبة المستقرة لضمان التشغيل)
if "GENAI_API_KEY" in st.secrets:
    api_key = st.secrets["GENAI_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدام الموديل المستقر مباشرة
    model = genai.GenerativeModel('gemini-1.5-flash')
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
            # ✅ الطريقة المضمونة للرد
            response = model.generate_content(prompt)
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
            st.error(f"❌ حصل خطأ: {e}")
