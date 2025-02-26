from transformers import pipeline  
import streamlit as st  

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")  
text = st.text_area("Paste your text here...")  
if text:  
    summary = summarizer(text, max_length=150)[0]['summary_text']  
    st.write("Summary:", summary)