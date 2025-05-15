from prompt_core.prompt import PromptManager
from typing import List, Dict, Optional
import json
import uuid

# 問題模組基底
class QuestionModule:
    def __init__(self, prompt_template: str):
        self.prompt_template = prompt_template

    def ask(self, prompt_manager: PromptManager, conversation_id: str, context: str, **kwargs) -> str:
        prompt = self.prompt_template.format(**kwargs)
        return prompt_manager.chat(conversation_id, user_input=prompt, system_prompt=context)

# 各類問題模組
class NameQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{target}的名字（如未提及請回覆「沒有資料」）')

class AliveQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{target}的存歿狀態（請回覆「存」、「歿」或「沒有資料」）')

class GenderQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{target}的性別（請回覆「男」、「女」或「沒有資料」）')

class AgeQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{target}的年齡（請回覆數字或「沒有資料」）')

class MarriageStatusQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{target}的婚姻狀態（請回覆「已婚」、「未婚」、「離異」或「沒有資料」）')

class CountQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{target}有幾位{relation}（請回覆數字或「沒有資料」）')

class RelationNameQuestion(QuestionModule):
    def __init__(self):
        super().__init__('請回覆{person}的{relation}是誰？（請回覆名字或「沒有資料」）')

# 人物資料結構
class Person:
    def __init__(self, name: str, pid: str):
        self.id = pid
        self.name = name
        self.gender: Optional[str] = None
        self.age: Optional[str] = None
        self.alive: Optional[str] = None
        self.marriage: Optional[str] = None
        self.relations: Dict[str, List[str]] = {}  # 如 {'father': ['2'], 'children': ['5','6']}

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'alive': self.alive,
            'marriage': self.marriage,
            'relations': self.relations
        }

# 主流程
class FamilyTreeBuilder:
    def __init__(self, txt_path: str, model: str = "llama3.2", host: str = "http://127.0.0.1:11434"):
        self.txt_path = txt_path
        self.prompt_manager = PromptManager(model=model, host=host)
        self.persons: Dict[str, Person] = {}
        self.next_id = 1
        self.context = "請讀取文本資料，並你只能用最簡短、符合要求的方式回答，以保證程式看得懂你的回應。"
        self.text = self._load_txt()

    def _load_txt(self) -> str:
        with open(self.txt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _new_person(self, name: str) -> Person:
        pid = str(self.next_id)
        self.next_id += 1
        person = Person(name, pid)
        self.persons[pid] = person
        return person

    def build(self):
        conversation_id = str(uuid.uuid4())
        self.prompt_manager.create_conversation(conversation_id)
        # 1. 問案主基本資料
        main_person = self._new_person("案主")
        main_person.name = NameQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主")
        print(f"[AI][案主姓名]: {main_person.name}")
        main_person.age = AgeQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主")
        print(f"[AI][案主年齡]: {main_person.age}")
        main_person.gender = GenderQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主")
        print(f"[AI][案主性別]: {main_person.gender}")
        main_person.alive = AliveQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主")
        print(f"[AI][案主存歿]: {main_person.alive}")
        main_person.marriage = MarriageStatusQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主")
        print(f"[AI][案主婚姻]: {main_person.marriage}")

        # 2. 問父母
        father = self._new_person("父親")
        father.name = NameQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主父親")
        print(f"[AI][父親姓名]: {father.name}")
        father.alive = AliveQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主父親")
        print(f"[AI][父親存歿]: {father.alive}")
        main_person.relations['father'] = [father.id]

        mother = self._new_person("母親")
        mother.name = NameQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主母親")
        print(f"[AI][母親姓名]: {mother.name}")
        mother.alive = AliveQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主母親")
        print(f"[AI][母親存歿]: {mother.alive}")
        main_person.relations['mother'] = [mother.id]

        # 3. 父親兄弟姐妹
        father_sibling_count = CountQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主父親", relation="兄弟姐妹")
        print(f"[AI][父親兄弟姐妹數]: {father_sibling_count}")
        try:
            n_father_sibling = int(father_sibling_count)
        except:
            n_father_sibling = 0
        if n_father_sibling > 0:
            for rel in ["兄長", "弟弟", "姊姊", "妹妹"]:
                count = CountQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主父親", relation=rel)
                print(f"[AI][父親{rel}數]: {count}")
                # 可選擇記錄於 father.relations[rel] = 數字

        # 4. 母親兄弟姐妹
        mother_sibling_count = CountQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主母親", relation="兄弟姐妹")
        print(f"[AI][母親兄弟姐妹數]: {mother_sibling_count}")
        try:
            n_mother_sibling = int(mother_sibling_count)
        except:
            n_mother_sibling = 0
        if n_mother_sibling > 0:
            for rel in ["兄長", "弟弟", "姊姊", "妹妹"]:
                count = CountQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主母親", relation=rel)
                print(f"[AI][母親{rel}數]: {count}")
                # 可選擇記錄於 mother.relations[rel] = 數字

        # 5. 配偶
        spouse_status = MarriageStatusQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主")
        print(f"[AI][案主婚姻狀態]: {spouse_status}")
        if spouse_status == "已婚":
            spouse = self._new_person("配偶")
            spouse.name = NameQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主配偶")
            print(f"[AI][配偶姓名]: {spouse.name}")
            spouse.gender = GenderQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主配偶")
            print(f"[AI][配偶性別]: {spouse.gender}")
            main_person.relations['spouse'] = [spouse.id]
            spouse.relations['spouse'] = [main_person.id]
        else:
            spouse = None

        # 6. 年齡分流：祖父母或子女
        try:
            age = int(main_person.age)
        except:
            age = 0
        if age < 50:
            # 問祖父母
            for parent, parent_obj in [("父親", father), ("母親", mother)]:
                for gp, gp_label in [("父親", "祖父"), ("母親", "祖母")]:
                    gp_obj = self._new_person(f"{parent}{gp_label}")
                    gp_obj.name = NameQuestion().ask(self.prompt_manager, conversation_id, self.text, target=f"案主{parent}{gp_label}")
                    print(f"[AI][{parent}{gp_label}姓名]: {gp_obj.name}")
                    gp_obj.alive = AliveQuestion().ask(self.prompt_manager, conversation_id, self.text, target=f"案主{parent}{gp_label}")
                    print(f"[AI][{parent}{gp_label}存歿]: {gp_obj.alive}")
                    parent_obj.relations[gp] = [gp_obj.id]
        else:
            # 問子女
            children_count = CountQuestion().ask(self.prompt_manager, conversation_id, self.text, target="案主", relation="孩子")
            print(f"[AI][案主孩子數]: {children_count}")
            try:
                n_children = int(children_count)
            except:
                n_children = 0
            children_ids = []
            for i in range(n_children):
                child = self._new_person(f"孩子{i+1}")
                child.name = NameQuestion().ask(self.prompt_manager, conversation_id, self.text, target=f"案主孩子{i+1}")
                print(f"[AI][孩子{i+1}姓名]: {child.name}")
                child.gender = GenderQuestion().ask(self.prompt_manager, conversation_id, self.text, target=f"案主孩子{i+1}")
                print(f"[AI][孩子{i+1}性別]: {child.gender}")
                child.alive = AliveQuestion().ask(self.prompt_manager, conversation_id, self.text, target=f"案主孩子{i+1}")
                print(f"[AI][孩子{i+1}存歿]: {child.alive}")
                children_ids.append(child.id)
            if children_ids:
                main_person.relations['children'] = children_ids

    def export_json(self, out_path: str):
        data = {'persons': [p.to_dict() for p in self.persons.values()]}
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 用法範例
if __name__ == "__main__":
    builder = FamilyTreeBuilder('input.txt')
    builder.build()
    builder.export_json('familytree.json')
