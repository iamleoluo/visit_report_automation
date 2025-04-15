# auto_summarize.py

import os
from prompt import PromptManager  # 改用 PromptManager
import uuid
import json
def read_document(file_path: str) -> str:
    """讀取 UTF-8 編碼的文檔並返回文本內容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    # 要讀取的文檔名稱
    file_path = "sample.txt"
    
    if not os.path.exists(file_path):
        print(f"檔案 {file_path} 不存在，請確認文檔是否正確放置於當前目錄中。")
        return

    # 讀取文檔內容
    text = read_document(file_path)

    # 初始化 PromptManager 實例
    prompt_manager = PromptManager(model="llama3.2", host="http://127.0.0.1:11434")
    
    # 設置默認參數
    prompt_manager.set_default_parameters(temperature=0.0, stream=False)

    # 生成唯一的對話ID
    conversation_id = str(uuid.uuid4())
    
    # 建立新的對話
    prompt_manager.create_conversation(conversation_id)

    # 提供一個系統提示詞 (system prompt)，用來指定摘要風格與要求
    system_prompt = """
    你是一個專業的文件摘要助手。請遵循以下準則：
    1. 保持摘要簡潔但完整
    2. 突出文檔的主要觀點
    3. 使用客觀的語氣
    4. 保留關鍵的數據和事實
    5. 按原文的結構組織摘要
    """

    # 呼叫摘要功能
    prompt = f"請幫我總結以下文檔內容：\n\n{text}"
    summary = prompt_manager.chat(
        conversation_id=conversation_id,
        user_input=prompt,
        system_prompt=system_prompt
    )
    
    print("\n最終摘要結果：")
    print(summary)
    
    # 如果需要查看對話歷史
    history = prompt_manager.get_conversation_history(conversation_id)
    print("\n對話歷史：")
    for msg in history:
        print(f"[{msg['role']}]: {msg['content'][:100]}...")  # 只顯示前100個字符

    # save result as json file
    with open("summary.json", "w") as f:
        json.dump(summary, f)
    
    # 清除對話歷史
    prompt_manager.clear_conversation(conversation_id)
    print(f"\n已清除對話歷史 (ID: {conversation_id})")

if __name__ == "__main__":
    main()