import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Yassin Bot", page_icon="🤖")
st.title("🤖 AI Yassin Bot")
st.caption("أهلاً بك في موقع ياسين للذكاء الاصطناعي")

import streamlit as st
api_key = st.secrets["GENAI_API_KEY"]
if "model_name" not in st.session_state:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.session_state.model_name = m.name
            break

model = genai.GenerativeModel(st.session_state.model_name)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني أي حاجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
