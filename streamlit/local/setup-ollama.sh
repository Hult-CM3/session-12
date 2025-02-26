#!/bin/bash
# setup-ollama.sh - Script to install Ollama in GitHub Codespaces

echo "Setting up Ollama in GitHub Codespaces..."

# Update package lists
sudo apt-get update

# Install required dependencies
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Download and install Ollama for Linux
curl -fsSL https://ollama.com/install.sh | sh

# Make Ollama executable
chmod +x ~/ollama

# Start Ollama server in the background
~/ollama serve &

# Wait for the server to start
echo "Waiting for Ollama server to start..."
sleep 5

# Pull a model (change "llama2" to your preferred model)
~/ollama pull llama2

echo "Ollama setup complete! The server is running in the background."
echo "You can use the Streamlit app to interact with it now."
echo "Available at: http://localhost:11434"