# Local Ollama with Llama 2

This project demonstrates how to use Ollama with Llama 2 locally using Python.

## Prerequisites

1. Install Ollama on your system:
   - macOS: `brew install ollama`
   - Linux: `curl https://ollama.ai/install.sh | sh`
   - Windows: Follow instructions at [Ollama Windows](https://github.com/ollama/ollama/blob/main/docs/windows.md)

2. Pull the Llama 2 model:
   ```bash
   ollama pull llama2
   ```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

2. Run the script:
   ```bash
   python main.py
   ```

## Features

- Simple chat interface with Llama 2
- Stream responses in real-time
- Example of system prompts and chat history management 