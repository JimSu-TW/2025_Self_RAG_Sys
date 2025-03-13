# RAG 文件檢索問答系統

基於 RAG (Retrieval-Augmented Generation) 架構的文檔檢索和問答系統，能夠處理多種文檔格式，並通過大語言模型提供精確回答。

## 功能特點

- 支援多種文檔格式：PDF、DOCX、TXT、Markdown、CSV
- 使用向量數據庫儲存文檔嵌入向量
- 基於語義相似度的文檔檢索
- 使用 Ollama 本地大語言模型生成答案
- 完整的 Docker 容器化部署方案
- 簡潔直觀的 Web 介面

## 架構設計

系統由以下組件組成：

- **前端**：基於 Streamlit 的使用者介面，提供文檔上傳和問答功能
- **後端**：FastAPI 服務，處理文檔解析、向量化和檢索
- **數據庫**：SQLite 儲存文檔和向量嵌入
- **向量檢索**：使用 FAISS 進行高效相似度搜尋
- **模型**：通過 Ollama 介面連接大語言模型

## 快速開始

### 前提條件

- Docker 和 Docker Compose
- Ollama 在本地運行 (用於大語言模型推理)

### 使用步驟

1. Clone this repo

2. 配置環境變數（可選）：
    編輯 `.env` 文件以設置 Ollama URL 和模型名稱：
    ```
    DATABASE_PATH=/app/data/rag_db.sqlite
    OLLAMA_URL=http://host.docker.internal:11434
    OLLAMA_MODEL=llama3.2
    ```

3. 啟動系統：
    ```bash
    docker-compose up --build
    ```

4. 訪問 Web 介面：
    在瀏覽器中打開 `http://localhost:8501`

## 使用方法

1. 在側邊欄上傳文檔（支援 PDF、DOCX、TXT、Markdown、CSV）
2. 點擊"建立知識庫"按鈕處理文檔
3. 在主介面輸入問題並點擊"開始查詢"
4. 系統將顯示回答及相關的參考文檔

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI, Uvicorn
- **Embeddings**: Sentence-Transformers
- **Vector Search**: FAISS
- **Document Parsing**: PyPDF2, python-docx, pandas
- **LLM Integration**: Ollama API
- **Containerization**: Docker, Docker Compose

## 目錄結構

```
.
├── .env                    # 環境變數配置
├── docker-compose.yaml     # Docker Compose 配置
├── backend/                # 後端 Fast API 服務
│   ├── dockerfile          # 後端 Docker 構建文件
│   ├── main.py             # 主程式入口
│   ├── requirements.txt    # Python Package for BackEnd
│   ├── connector/          # 數據庫連接器
│   ├── helper/             # 業務邏輯輔助函數
│   ├── router/             # API 路由
│   └── utils/              # 工具函數
└── frontend/               # 前端應用
     ├── dockerfile          # 前端 Docker 構建文件
     ├── homepage.py         # Streamlit 主頁
     └── requirements.txt    # Python Package for FrontEnd
```