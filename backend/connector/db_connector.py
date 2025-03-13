import sqlite3
import pickle
import faiss
import numpy as np
import os
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger(__name__)

# 載入 .env 環境變數
load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH", "/app/data/rag_db.sqlite")
logger.info(f"Database path set to {DB_PATH}")


def get_db_connection():
    """建立 SQLite 資料庫連線，確保資料夾存在"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    logger.info(f"Ensuring directory exists: {os.path.dirname(DB_PATH)}")
    conn = sqlite3.connect(DB_PATH)
    logger.info("Database connection established")
    return conn, conn.cursor()


def save_embeddings(documents, embeddings):
    """將文件嵌入向量儲存到 SQLite 資料庫"""
    logger.info(f"Saving {len(documents)} embeddings to database")
    conn, cur = get_db_connection()
    cur.execute("CREATE TABLE IF NOT EXISTS embeddings (id INTEGER PRIMARY KEY, filename TEXT, content TEXT, embedding BLOB)")
    for doc, emb in zip(documents, embeddings):
        cur.execute("INSERT INTO embeddings (filename, content, embedding) VALUES (?, ?, ?)", 
                    (doc["filename"], doc["content"], pickle.dumps(emb)))
    conn.commit()
    conn.close()
    logger.info("Embeddings saved successfully")


def get_embeddings():
    """從 SQLite 讀取所有嵌入向量並建立 FAISS 索引"""
    logger.info("Retrieving embeddings from database")
    conn, cur = get_db_connection()

    # Check if the embeddings table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'")
    if not cur.fetchone():
        logger.warning("Embeddings table does not exist yet")
        conn.close()
        return [], [], None

    cur.execute("SELECT filename, content, embedding FROM embeddings")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        logger.warning("No embeddings found in database")
        return [], [], None  # 避免當資料庫為空時發生錯誤

    documents = [{"filename": row[0], "content": row[1]} for row in rows]
    embeddings = [pickle.loads(row[2]) for row in rows]

    logger.info(f"Retrieved {len(documents)} embeddings, building FAISS index")
    # 確保索引大小與嵌入向量維度一致
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.vstack(embeddings))
    logger.info("FAISS index built successfully")

    return documents, embeddings, index
