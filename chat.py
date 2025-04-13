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
        self.conversation_history: List[Dict[str, str]] = []
    
    def chat(self, user_input: str, system_prompt: Optional[str] = None, 
             temperature: float = 0.0, stream: bool = False) -> str:
        """與AI進行對話

        
        Args:
            user_input: 用戶輸入的文本
            system_prompt: 系統提示詞
            temperature: 溫度參數，控制回答的隨機性
            stream: 是否使用流式輸出
            
        Returns:
            AI的回應文本
        """
        # 添加用戶輸入到對話歷史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 準備消息列表
        messages = self.conversation_history.copy()
        
        # 如果有系統提示詞，添加到消息列表的開頭
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        # 打印發送給AI的完整文本
        print("\n發送給AI的文本:")
        for msg in messages:
            print(f"[{msg['role']}]: {msg['content']}")
        # print temperature and stream
        print(f"temperature: {temperature}, stream: {stream}")  
        
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
            
            # 添加AI回應到對話歷史
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
            
        except Exception as e:
            error_message = f"發生錯誤: {str(e)}"
            return error_message
    
    def clear_history(self) -> None:
        """清除對話歷史"""
        self.conversation_history = []


if __name__ == "__main__":
    # 示例用法
    chatbot = ChatBot()
    print("簡單聊天機器人 (輸入 '/quit' 結束, 輸入 '/clear' 清除對話歷史)")
    
    while True:
        user_input = input("\n你: ").strip()
        
        if user_input.lower() == '/quit':
            break
        
        if user_input.lower() == '/clear':
            chatbot.clear_history()
            print("\n對話歷史已清除")
            continue
            
        if user_input:
            response = chatbot.chat(user_input)
            print("\nAI:", response)