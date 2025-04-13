# Ollama Chat Interface

A simple Python interface for interacting with Ollama language models, providing both regular and streaming chat capabilities.

## Features

- Easy-to-use chat interface with Ollama models
- Support for conversation history
- Stream mode for real-time responses
- Temperature control for response randomness
- System prompt support
- Conversation history management

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running
- Required Python packages:
  ```
  ollama
  ```

## Setup

1. Install Ollama (if not already installed):
   ```bash
   curl https://ollama.ai/install.sh | sh
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Ollama server:
   ```bash
   ollama serve
   ```

## Usage

### Basic Usage

```python
from chat import ChatBot

# Initialize the chatbot
chatbot = ChatBot(model="llama2", host="http://127.0.0.1:11434")

# Simple chat
response = chatbot.chat("Hello, how are you?")
print(response)
```

### Advanced Features

1. Using system prompts:
```python
response = chatbot.chat(
    user_input="What's the capital of France?",
    system_prompt="You are a geography expert."
)
```

2. Streaming mode:
```python
response = chatbot.chat(
    user_input="Tell me a story.",
    stream=True
)
```

3. Adjusting temperature:
```python
response = chatbot.chat(
    user_input="Write a creative story.",
    temperature=0.7
)
```

4. Managing conversation history:
```python
# Clear conversation history
chatbot.clear_history()
```

## Interactive Mode

The script includes an interactive mode when run directly:

```bash
python chat.py
```

Commands in interactive mode:
- `/quit`: Exit the chat
- `/clear`: Clear conversation history

## Class Reference

### ChatBot

#### Methods

- `__init__(model: str = "llama2", host: str = "http://127.0.0.1:11434")`
  - Initializes the chatbot with specified model and host

- `chat(user_input: str, system_prompt: Optional[str] = None, temperature: float = 0.0, stream: bool = False) -> str`
  - Sends a message to the AI and returns the response
  - Parameters:
    - user_input: The message to send
    - system_prompt: Optional system instructions
    - temperature: Controls response randomness (0.0 to 1.0)
    - stream: Enable streaming mode

- `clear_history() -> None`
  - Clears the conversation history 