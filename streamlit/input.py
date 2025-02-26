import streamlit as st

st.set_page_config(page_title="First Chat", page_icon="💬")
st.title("💬 Hult GPT v1.0")
prompt = st.chat_input("Ask me a question")
if prompt:
    st.write(f"User has sent the following: {prompt}")