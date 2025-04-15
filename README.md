# Ollama Chat Framework

一個模組化的 Ollama 聊天框架，提供分層的對話管理和提示詞處理功能。

## 架構設計

該框架採用三層架構：

1. **應用層 (Application Layer)**
   - 實現具體的業務邏輯
   - 配置特定的提示詞模板
   - 處理輸入輸出
   - 例如：`auto_summarize.py`

2. **提示詞層 (Prompt Layer)**
   - 管理對話歷史
   - 處理提示詞模板
   - 控制對話參數
   - 位於：`prompt.py`

3. **聊天層 (Chat Layer)**
   - 處理與 Ollama API 的基礎通信
   - 提供核心聊天功能
   - 位於：`chat.py`

## 功能特點

- 分層架構，職責分明
- 完整的對話歷史管理
- 靈活的提示詞模板系統
- 支持流式輸出
- 可調節的溫度參數
- JSON 格式的結果保存

## 安裝需求

- Python 3.8 或更高版本
- Ollama 服務
- Python 依賴套件：
  ```
  ollama
  ```

## 快速開始

1. 安裝 Ollama（如果尚未安裝）：
   ```bash
   curl https://ollama.ai/install.sh | sh
   ```

2. 安裝 Python 依賴：
   ```bash
   pip install -r requirements.txt
   ```

3. 啟動 Ollama 服務：
   ```bash
   ollama serve
   ```

## 使用示例

### 基本使用

```python
from prompt import PromptManager
import uuid

# 初始化
prompt_manager = PromptManager(model="llama3.2")
conversation_id = str(uuid.uuid4())

# 建立對話
prompt_manager.create_conversation(conversation_id)

# 進行對話
response = prompt_manager.chat(
    conversation_id=conversation_id,
    user_input="你好",
    system_prompt="你是一個友善的助手"
)

# 獲取對話歷史
history = prompt_manager.get_conversation_history(conversation_id)

# 清除對話歷史
prompt_manager.clear_conversation(conversation_id)
```

### 文件摘要示例

```python
from prompt import PromptManager
import uuid

# 初始化
prompt_manager = PromptManager()
conversation_id = str(uuid.uuid4())

# 設置系統提示詞
system_prompt = """
你是一個專業的文件摘要助手。請遵循以下準則：
1. 保持摘要簡潔但完整
2. 突出文檔的主要觀點
3. 使用客觀的語氣
"""

# 進行摘要
summary = prompt_manager.chat(
    conversation_id=conversation_id,
    user_input=f"請總結以下文檔：\n{text}",
    system_prompt=system_prompt
)

# 保存結果
with open("summary.json", "w") as f:
    json.dump(summary, f)
```

## API 參考

### PromptManager

主要的提示詞管理類，提供完整的對話管理功能。

#### 方法

- `__init__(model: str = "llama3.2", host: str = "http://127.0.0.1:11434")`
  - 初始化提示詞管理器

- `create_conversation(conversation_id: str) -> None`
  - 建立新的對話

- `chat(conversation_id: str, user_input: str, system_prompt: Optional[str] = None) -> str`
  - 進行對話

- `get_conversation_history(conversation_id: str) -> List[Dict[str, str]]`
  - 獲取對話歷史

- `clear_conversation(conversation_id: str) -> None`
  - 清除對話歷史

- `set_default_parameters(temperature: float = 0.0, stream: bool = False) -> None`
  - 設置默認參數

### ChatBot

底層的聊天實現類，處理與 Ollama API 的直接通信。

#### 方法

- `__init__(model: str = "llama3.2", host: str = "http://127.0.0.1:11434")`
  - 初始化聊天機器人

- `chat(messages: List[Dict[str, str]], temperature: float = 0.0, stream: bool = False) -> str`
  - 發送消息到 Ollama API

## 注意事項

1. 確保 Ollama 服務正在運行
2. 妥善管理對話 ID
3. 適時清理不需要的對話歷史
4. 根據需求調整溫度參數
5. 對於大型文本，建議使用流式輸出 