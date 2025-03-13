import os
import requests
import json
from connector.db_connector import get_embeddings
from utils.retrieval_utils import search_documents
from utils.logger import get_logger
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3")

# 設定 logger
logger = get_logger(__name__)


def handle_query(query: str):
    logger.info(f"Processing query: {query}")
    try:
        documents, embeddings, index = get_embeddings()
        logger.info(f"Retrieved {len(documents)} documents from database")

        retrieved_docs, prompt = search_documents(query, documents, index)
        logger.info(f"Generated prompt: {prompt}")
        logger.info(f"Found {len(retrieved_docs)} relevant documents")

        url = f"{OLLAMA_URL}/api/generate"
        payload = {
            "prompt": prompt,
            "model": OLLAMA_MODEL,
            "format": {  # 強制 Ollama 回傳 JSON 格式
                "type": "object",
                "properties": {
                    "response": {"type": "string"}
                },
                "required": ["response"]
            }
        }

        logger.info(f"Calling Ollama API with model: {OLLAMA_MODEL}")
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        generated_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    generated_text += data.get("response", "")
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response line")
                    continue  # 跳過解析失敗的行

        result = generated_text.strip() or "未取得答案"
        logger.info("Query processing completed successfully")
        return result, retrieved_docs

    except requests.exceptions.RequestException as e:
        error_msg = f"Ollama API 錯誤: {str(e)}"
        logger.error(error_msg)
        return error_msg, []
    except Exception as e:
        error_msg = f"處理查詢時發生錯誤: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg, []
