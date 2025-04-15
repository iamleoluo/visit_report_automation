from ollama import Client
from typing import List, Dict, Optional, Union

class ChatBot:
    def __init__(self, model: str = "llama3.2", host: str = "http://127.0.0.1:11434"):
        """初始化聊天機器人
        
        Args:
            model: 使用的模型名稱
            host: Ollama主機URL
        """
        self.client = Client(host=host)
        self.model = model
    
    def chat(self, messages: List[Dict[str, str]], 
             temperature: float = 0.0, stream: bool = False) -> str:
        """與AI進行對話
        
        Args:
            messages: 消息列表，包含對話歷史
            temperature: 溫度參數，控制回答的隨機性
            stream: 是否使用流式輸出
            
        Returns:
            AI的回應文本
        """
        try:
            # 獲取AI回應
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=stream,
                options={"temperature": temperature}
            )
            
            # 處理流式輸出
            if stream:
                full_response = ""
                for chunk in response:
                    if isinstance(chunk, dict) and 'message' in chunk:
                        content = chunk['message'].get('content', '')
                        if content:
                            full_response += content
                response_text = full_response
            else:
                response_text = response['message']['content']
            
            return response_text
            
        except Exception as e:
            error_message = f"發生錯誤: {str(e)}"
            return error_message
