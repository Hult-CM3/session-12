from transformers import pipeline  
import streamlit as st  

chatbot = pipeline('text-generation', model='microsoft/DialoGPT-medium')  
user_input = st.chat_input("Talk to the AI...")  
if user_input:  
    response = chatbot(user_input, max_length=100)[0]['generated_text']  
    st.write(f"AI: {response}")
