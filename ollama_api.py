from typing import List, Dict, Optional, Union, Generator
from ollama import Client
import json

class OllamaAPI:
    def __init__(self, host: str = 'http://127.0.0.1:11434', model: str = 'llama3.2'):
        """Initialize Ollama API wrapper.
        
        Args:
            host: Ollama host URL
            model: Default model to use
        """
        self.client = Client(host=host)
        self.model = model
        self.history: List[Dict[str, str]] = []

    def chat(self, 
             prompt: str, 
             system_prompt: Optional[str] = None,
             temperature: float = 0.7,
             top_p: float = 0.9,
             stream: bool = False,
             context_window: Optional[int] = None) -> Union[str, Generator]:
        """Send a chat message to Ollama.
        
        Args:
            prompt: User message
            system_prompt: Optional system prompt to set behavior
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Top-p sampling (0.0 to 1.0)
            stream: Whether to stream the response
            context_window: Max context window size
            
        Returns:
            Response text or generator if streaming
        """
        messages = self.history.copy()
        
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=stream,
                options={
                    "temperature": temperature,
                    "top_p": top_p,
                    **({"num_ctx": context_window} if context_window else {})
                }
            )

            if stream:
                return self._stream_response(response)
            else:
                return self._get_full_response(response)

        except Exception as e:
            raise OllamaAPIError(f"Chat error: {str(e)}")

    def _stream_response(self, response: Generator) -> Generator:
        """Process streaming response."""
        try:
            for chunk in response:
                if 'message' in chunk:
                    yield chunk['message']['content']
        except Exception as e:
            raise OllamaAPIError(f"Streaming error: {str(e)}")

    def _get_full_response(self, response: Generator) -> str:
        """Get complete response from generator."""
        try:
            full_response = ""
            for chunk in response:
                if 'message' in chunk:
                    full_response += chunk['message']['content']
            return full_response
        except Exception as e:
            raise OllamaAPIError(f"Response processing error: {str(e)}")

    def clear_history(self):
        """Clear chat history."""
        self.history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get chat history."""
        return self.history.copy()

    def save_history(self, filepath: str):
        """Save chat history to file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            raise OllamaAPIError(f"History save error: {str(e)}")

    def load_history(self, filepath: str):
        """Load chat history from file."""
        try:
            with open(filepath, 'r') as f:
                self.history = json.load(f)
        except Exception as e:
            raise OllamaAPIError(f"History load error: {str(e)}")

class OllamaAPIError(Exception):
    """Custom exception for Ollama API errors."""
    pass 