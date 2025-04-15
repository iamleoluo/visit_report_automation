from prompt import PromptManager
import uuid

# 初始化
prompt_manager = PromptManager()
conversation_id = str(uuid.uuid4())

# 建立新對話
prompt_manager.create_conversation(conversation_id)

# 進行對話
response1 = prompt_manager.chat(
    conversation_id=conversation_id,
    user_input="你好",
    system_prompt="你是一個友善的助手"
)

# 繼續對話（會自動保持歷史記錄）
response2 = prompt_manager.chat(
    conversation_id=conversation_id,
    user_input="我想問你，你覺得我們的對話如何？"
)

# 查看歷史記錄
history = prompt_manager.get_conversation_history(conversation_id)
for msg in history:
    print(f"[{msg['role']}]: {msg['content']}")

# 清除歷史記錄
prompt_manager.clear_conversation(conversation_id)
