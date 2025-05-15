from prompt_core.prompt import PromptManager, PromptLibrary

if __name__ == "__main__":
    prompt_lib = PromptLibrary("run.json")
    pm = PromptManager()
    conversation_id = "myconv"
    pm.create_conversation(conversation_id)

    # 1. 讀取 input.txt
    with open("input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()

    # 2. intro
    intro = prompt_lib.get_prompt("intro")
    q = intro["template"].format(input=input_text)
    print(f"[Q] {q}")
    print(f"[AI] {pm.chat(conversation_id, q)}")

    # 3. has_children
    has_children = prompt_lib.get_prompt("has_children")
    q = has_children["question"]
    print(f"[Q] {q}")
    print(f"[AI] {pm.chat(conversation_id, q)}")

    # 4. children_names
    children_names = prompt_lib.get_prompt("children_names")
    q = children_names["question"]
    print(f"[Q] {q}")
    print(f"[AI] {pm.chat(conversation_id, q)}")

    # 5. 結束
    print("=== 對話歷史 ===")
    for msg in pm.get_conversation_history(conversation_id):
        print(f"[{msg['role']}] {msg['content']}")

    # 6. 清除所有對話
    pm.clear_conversation(conversation_id)




