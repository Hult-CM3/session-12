import streamlit as st
import requests
import json
import time
import logging
import subprocess
import os
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(page_title="Codespaces Ollama Chat", page_icon="💬")
st.title("💬 Ollama Chat in GitHub Codespaces")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ollama_status" not in st.session_state:
    st.session_state.ollama_status = "unknown"

# Sidebar with configuration
st.sidebar.title("Model Settings")

# Ollama server URL
ollama_url = "http://localhost:11434"

# Available models - these are the models that come with Ollama
model_option = st.sidebar.selectbox(
    "Choose a model",
    [
        "llama2",
        "mistral",
        "phi",
        "gemma",
        "neural-chat",
        "tinyllama"
    ],
    index=0
)

# Temperature setting
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Function to check if Ollama is running
def check_ollama_status():
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            available_models = [model["name"] for model in response.json().get("models", [])]
            return True, available_models
        return False, []
    except Exception as e:
        logger.error(f"Error checking Ollama status: {e}")
        return False, []

# Function to start Ollama server
def start_ollama_server():
    try:
        home_dir = os.path.expanduser("~")
        ollama_path = os.path.join(home_dir, "ollama")
        subprocess.Popen([ollama_path, "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for the server to start
        return True
    except Exception as e:
        logger.error(f"Error starting Ollama: {e}")
        return False

# Function to pull a model
def pull_model(model_name):
    try:
        home_dir = os.path.expanduser("~")
        ollama_path = os.path.join(home_dir, "ollama")
        st.sidebar.info(f"Pulling model {model_name}... This might take a while.")
        process = subprocess.Popen(
            [ollama_path, "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Show progress updates
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                st.sidebar.text(output.strip())
        
        return True
    except Exception as e:
        logger.error(f"Error pulling model: {e}")
        return False

# Function to generate response from Ollama
def generate_response(messages: List[Dict[str, str]], model: str):
    # Convert messages to Ollama format
    prompt = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            prompt += f"User: {content}\n"
        elif role == "assistant":
            prompt += f"Assistant: {content}\n"
    
    prompt += "Assistant: "
    
    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=90
        )
        
        if response.status_code == 200:
            return response.json().get("response", "No response generated")
        else:
            logger.error(f"Ollama API error: {response.status_code}, {response.text}")
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Error: {str(e)}"

# Check Ollama status
ollama_running, available_models = check_ollama_status()

if not ollama_running:
    st.sidebar.warning("Ollama is not running. Trying to start it...")
    if start_ollama_server():
        time.sleep(2)  # Give it a moment to fully initialize
        ollama_running, available_models = check_ollama_status()

if ollama_running:
    st.session_state.ollama_status = "running"
    st.sidebar.success("✅ Ollama is running")
    
    # Check if selected model is available
    if available_models:
        st.sidebar.write("Available models:")
        for model in available_models:
            st.sidebar.write(f"- {model}")
        
        if model_option not in available_models:
            st.sidebar.warning(f"Selected model '{model_option}' is not available.")
            if st.sidebar.button(f"Pull {model_option} model"):
                pull_model(model_option)
                st.rerun()
    else:
        st.sidebar.info("No models detected. You need to pull a model.")
        if st.sidebar.button(f"Pull {model_option} model"):
            pull_model(model_option)
            st.rerun()
else:
    st.session_state.ollama_status = "not_running"
    st.sidebar.error("❌ Ollama is not running or not accessible")
    st.sidebar.info("""
    Make sure Ollama is installed and running:
    1. Run `./setup-ollama.sh` in the terminal
    2. Or manually start with `~/ollama serve`
    """)
    
    if st.sidebar.button("Try to start Ollama"):
        start_ollama_server()
        st.rerun()

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to talk about?"):
    # Check again if the model is available
    ollama_running, available_models = check_ollama_status()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate a response if Ollama is running and model is available
    if ollama_running and model_option in available_models:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(st.session_state.messages, model_option)
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
    elif ollama_running and model_option not in available_models:
        st.error(f"Model '{model_option}' is not available. Please pull it first.")
    else:
        st.error("Please start Ollama first!")

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Information section
with st.sidebar.expander("Codespaces Instructions"):
    st.write("""
    ### Using Ollama in GitHub Codespaces:
    
    1. The setup script should have installed Ollama automatically
    
    2. If Ollama isn't running:
       - Run `./setup-ollama.sh` in the terminal
       - Or manually start with `~/ollama serve`
    
    3. To pull a different model:
       - Use the dropdown and "Pull model" button
       - Or run: `~/ollama pull modelname`
    
    4. Troubleshooting:
       - Check terminal for error messages
       - Restart the Codespace if necessary
    """)