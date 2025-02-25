import torch  
import streamlit as st  
from PIL import Image  

model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)  
uploaded_file = st.file_uploader("Upload an image...")  
if uploaded_file:  
    image = Image.open(uploaded_file)  
    st.image(image)  
    # Preprocess image and run inference  
    prediction = "Example: Golden Retriever (98.5%)"  
    st.write(f"Prediction: {prediction}")
