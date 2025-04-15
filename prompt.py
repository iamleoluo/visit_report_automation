from typing import Optional, Dict, List
from chat import ChatBot

class PromptManager:
    def __init__(self, model: str = "llama3.2", host: str = "http://127.0.0.1:11434"):
        """初始化 Prompt 管理器
        
        Args:
            model: 使用的模型名稱
            host: Ollama主機URL
        """
        self.chat_bot = ChatBot(model=model, host=host)
        self.default_temperature = 0.0
        self.default_stream = False
        self.conversation_histories: Dict[str, List[Dict[str, str]]] = {}
        
    def create_conversation(self, conversation_id: str) -> None:
        """建立新的對話歷史
        
        Args:
            conversation_id: 對話的唯一識別碼
        """
        if conversation_id not in self.conversation_histories:
            self.conversation_histories[conversation_id] = []
            
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """獲取特定對話的歷史記錄
        
        Args:
            conversation_id: 對話的唯一識別碼
            
        Returns:
            對話歷史列表
        """
        return self.conversation_histories.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str) -> None:
        """清除特定對話的歷史記錄
        
        Args:
            conversation_id: 對話的唯一識別碼
        """
        if conversation_id in self.conversation_histories:
            self.conversation_histories[conversation_id] = []
        
    def chat(self, 
            conversation_id: str,
            user_input: str,
            system_prompt: Optional[str] = None,
            temperature: Optional[float] = None,
            stream: Optional[bool] = None) -> str:
        """使用特定的提示模板進行對話
        
        Args:
            conversation_id: 對話的唯一識別碼
            user_input: 用戶輸入的文本
            system_prompt: 系統提示詞
            temperature: 溫度參數
            stream: 是否使用流式輸出
            
        Returns:
            AI的回應文本
        """
        # 確保對話歷史存在
        self.create_conversation(conversation_id)
        
        # 準備消息列表
        messages = self.conversation_histories[conversation_id].copy()
        
        # 如果有系統提示詞且是新對話，添加到開頭
        if system_prompt and not messages:
            messages.insert(0, {"role": "system", "content": system_prompt})
            
        # 添加用戶輸入
        messages.append({"role": "user", "content": user_input})
        
        # 使用提供的參數或默認值
        temp = temperature if temperature is not None else self.default_temperature
        strm = stream if stream is not None else self.default_stream
        
        # 進行對話
        response = self.chat_bot.chat(
            messages=messages,
            temperature=temp,
            stream=strm
        )
        
        # 更新對話歷史
        if system_prompt and not self.conversation_histories[conversation_id]:
            self.conversation_histories[conversation_id].append(
                {"role": "system", "content": system_prompt}
            )
        self.conversation_histories[conversation_id].append(
            {"role": "user", "content": user_input}
        )
        self.conversation_histories[conversation_id].append(
            {"role": "assistant", "content": response}
        )
        
        return response

    def set_default_parameters(self, temperature: float = 0.0, stream: bool = False) -> None:
        """設置默認參數
        
        Args:
            temperature: 默認溫度參數
            stream: 默認是否使用流式輸出
        """
        self.default_temperature = temperature
        self.default_stream = stream
        
    def delete_conversation(self, conversation_id: str) -> bool:
        """刪除特定對話的歷史記錄
        
        Args:
            conversation_id: 要刪除的對話ID
            
        Returns:
            bool: 是否成功刪除
        """
        return self.chat_bot.delete_conversation(conversation_id)
