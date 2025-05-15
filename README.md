# Ollama Prompt Application

本專案是一個基於 Ollama API 的自動化問答/摘要應用，核心邏輯集中於 `prompt_core`，主程式為 `run.py`，並透過 `run.json` 定義提示詞流程，`input.txt` 作為輸入資料來源。

## 目標

- 自動化處理訪談或個案報告等文本，根據自訂提示詞流程進行多輪問答。
- 支援自定義 prompt 流程，靈活擴展。

## 目錄結構

```
├── run.py           # 主應用程式，執行問答流程
├── run.json         # 問答流程與提示詞設定
├── input.txt        # 輸入文本（如個案報告）
├── prompt_core/
│   ├── prompt.py    # Prompt 管理與對話歷史
│   ├── chat.py      # 與 Ollama API 溝通
│   └── __init__.py
├── requirements.txt # 依賴套件
```

## 安裝方式

1. 安裝 Python 3.8 以上
2. 安裝 Ollama 並啟動服務：
   ```bash
   curl https://ollama.ai/install.sh | sh
   ollama serve
   ```
3. 安裝 Python 依賴：
   ```bash
   pip install -r requirements.txt
   ```

## 快速開始

1. 準備你的輸入文本，放在 `input.txt`
2. 設定你的問答流程與提示詞於 `run.json`
3. 執行主程式：
   ```bash
   python run.py
   ```

### 範例 `run.json`

```json
[
  {
    "label": "intro",
    "type": "chat",
    "template": "請根據以下內容開始問診：{input}"
  },
  {
    "label": "has_children",
    "type": "choice",
    "question": "個案有沒有孩子？",
    "choices": ["yes", "no"]
  },
  {
    "label": "children_names",
    "type": "text",
    "question": "請輸入所有孩子的名字，用逗號分隔。",
    "format": "name1,name2,name3"
  }
]
```

### 範例 `input.txt`

（請參考專案內現有 input.txt 範例）

### 執行結果

程式會依序根據 `run.json` 的流程，對 `input.txt` 內容進行多輪問答，並將每輪問題與 AI 回答印出，最後顯示完整對話歷史。

## 核心說明

### prompt_core
- `prompt.py`：
  - `PromptManager` 管理對話歷史、與 AI 互動、參數設定。
  - `PromptLibrary` 載入/查詢 prompt 流程（如 run.json）。
- `chat.py`：
  - `ChatBot` 負責與 Ollama API 進行對話。

### 問答流程
- `run.py` 會：
  1. 載入 `run.json` 取得問答流程
  2. 讀取 `input.txt` 作為初始輸入
  3. 依序執行每個 prompt，將問題送給 AI 並取得回應
  4. 印出每輪問答與完整對話歷史

## 自訂/擴充
- 你可以編輯 `run.json`，新增/修改/刪除 prompt 流程與問題。
- 支援 `template`（可帶入 input）、`question`、`choices` 等欄位。

## 依賴
- Python 3.8+
- [Ollama](https://ollama.ai/) 服務
- Python 套件：ollama==0.1.6

## 注意事項
- 請確保 Ollama 服務已啟動
- 輸入檔案與 prompt 流程需正確設定
- 目前僅支援單一對話流程（可自行擴充） 