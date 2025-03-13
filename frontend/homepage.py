import os
import streamlit as st
import requests

st.set_page_config(page_title="📚 RAG 檢索問答系統", layout="wide")

st.title("📚 RAG 文件檢索問答系統")

# 設定 Backend URL（在 Docker 內是 'backend'，本機測試時用 'localhost'）
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
if os.getenv("RUNNING_LOCALLY"):
    BACKEND_URL = "http://localhost:8000"

# Sidebar for file upload and knowledge base management
st.sidebar.header("知識庫管理")
uploaded_files = st.sidebar.file_uploader(
    "上傳文件 (.txt, .pdf, .docx, .md, .csv)", type=["txt", "pdf", "docx", "md", "csv"], accept_multiple_files=True
)

if st.sidebar.button("建立知識庫"):
    if uploaded_files:
        files = [
            (
                "files", (
                    file.name, file.getvalue(), file.type if hasattr(file, "type") else "application/octet-stream"
                )
            ) for file in uploaded_files
        ]
        response = requests.post(f"{BACKEND_URL}/api/v1/documents/upload", files=files)
        if response.ok:
            st.sidebar.success("成功建立知識庫！")
        else:
            st.sidebar.error("建立知識庫失敗：" + response.text)
    else:
        st.sidebar.warning("請先上傳文件！")

# Main content for querying
st.header("🔎 查詢文件")
query = st.text_input("輸入你的問題")
if st.button("開始查詢"):
    if query:
        with st.spinner("正在處理您的問題..."):
            response = requests.post(f"{BACKEND_URL}/api/v1/query", json={"query": query})
            if response.ok:
                data = response.json()

                # 處理不同的回應格式
                if "response" in data and isinstance(data["response"], str):
                    # 檢查是否為錯誤訊息
                    if "失敗" in data["response"]:
                        st.error(data["response"])
                    else:
                        # 正常的回應格式
                        answer = data["response"]
                        references = data.get("references", [])

                        st.subheader("✨ 回答：")
                        st.write(answer)

                        if references:
                            st.subheader("📖 參考文件：")
                            for i, doc in enumerate(references, 1):
                                st.expander(f"文件 {i} - {doc['filename']}").write(doc['content'])
                else:
                    # 回到原始結構
                    answer = data.get("answer", "無法提供回答")

                    # 處理 answer 可能是 JSON 字串的情況
                    if isinstance(answer, str) and answer.strip().startswith("{"):
                        try:
                            import json
                            answer_json = json.loads(answer)
                            if "response" in answer_json:
                                answer = answer_json["response"]
                        except Exception as e:
                            # 如果解析失敗，使用原始回答
                            st.warning(f"解析回答時發生錯誤：{str(e)}")
                            pass

                    references = data.get("references", [])

                    st.subheader("✨ 回答：")
                    st.write(answer)

                    if references:
                        st.subheader("📖 參考文件：")
                        for i, doc in enumerate(references, 1):
                            st.expander(f"文件 {i} - {doc['filename']}").write(doc['content'])
            else:
                st.error(f"查詢失敗：{response.text}")
    else:
        st.warning("請輸入問題後再查詢")
