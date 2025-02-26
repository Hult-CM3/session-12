

# Ollama Chat App for GitHub Codespaces

This project provides a Streamlit chat interface for Ollama LLMs running directly in GitHub Codespaces. No API keys, no rate limits, and completely free to use!

## Quick Start

1. **Open in Codespaces**:
   - Click the "Code" button on your GitHub repository
   - Select the "Codespaces" tab
   - Click "Create codespace on main"

2. **The setup will run automatically**:
   - Ollama will be installed
   - The LLama2 model will be pulled
   - The Streamlit app will be ready to use

3. **Run the app**:
   ```bash
   streamlit run streamlit_ollama_app.py
   ```

4. **Access the app**:
   - Click on the "Open in Browser" button that appears
   - Or use the Ports tab to access port 8501

## Features

- **No API Key Required**: All processing happens locally in your Codespace
- **No Rate Limits**: Use it as much as you want without restrictions
- **Multiple Models**: Choose from several open-source models
- **Full Control**: Adjust temperature and other settings
- **Easy Setup**: Everything is configured automatically

## Available Models

- **llama2**: Meta AI's LLaMA 2 model
- **mistral**: Mistral AI's 7B model
- **phi**: Microsoft's Phi models
- **gemma**: Google's Gemma models
- **neural-chat**: Intel's NeuralChat
- **tinyllama**: Smaller version of LLaMA

## Manual Setup

If automatic setup doesn't work:

1. Run the setup script:
   ```bash
   chmod +x ./setup-ollama.sh
   ./setup-ollama.sh
   ```

2. Start Ollama:
   ```bash
   ~/ollama serve
   ```

3. Pull a model:
   ```bash
   ~/ollama pull llama2
   ```

4. Run Streamlit:
   ```bash
   streamlit run streamlit_ollama_app.py
   ```

## Troubleshooting

If you encounter issues:

- **Ollama not starting**: Check if it's already running with `ps aux | grep ollama`
- **Model not found**: Make sure you've pulled the model first
- **Port not accessible**: Check the Ports tab in VS Code to ensure ports 8501 and 11434 are forwarded

## Limitations

- Model downloads can take some time, especially on slower connections
- Larger models may not work well in Codespaces due to memory constraints
- Codespaces has a usage limit (120 core hours per month for free accounts)
