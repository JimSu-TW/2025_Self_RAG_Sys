from sentence_transformers import SentenceTransformer
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


def search_documents(query, documents, index, k=3, distance_threshold=1.45):
    """從文件庫中搜尋最相關的文件，並生成提示

    Args:
        query: 使用者查詢
        documents: 文件列表
        index: 向量索引
        k: 要檢索的文件數量
        distance_threshold: 相似度閾值，大於此值的文件將被視為不相關（0-1之間，越小要求越嚴格）
    """
    if not documents or index is None:
        logger.warning("No documents available in database")
        return [], "資料庫中無可用文件，請先上傳文件。"

    logger.info(f"Searching for query: {query}")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vec = model.encode([query])

    # 確保 k 不超過文件數量，避免索引錯誤
    k = min(k, len(documents))
    logger.info(f"Using k={k} for retrieval")
    distances, indices = index.search(query_vec, k=k)
    logger.info(f"Found indices: {indices}")
    logger.info(f"Found distances: {distances}")

    # 使用距離閾值過濾結果
    filtered_results = [(i, dist) for i, dist in zip(indices[0], distances[0])
                        if i < len(documents) and dist <= distance_threshold]
    logger.info(f"After filtering by distance threshold {distance_threshold}: {len(filtered_results)} documents")

    # 如果過濾後沒有文件，返回適當的消息
    if not filtered_results:
        logger.warning("No relevant documents found after filtering by distance threshold")
        return [], "找不到與查詢相關的文件。"

    # 從過濾後的結果中獲取文件
    retrieved_docs = [documents[i] for i, _ in filtered_results]
    logger.info(f"Retrieved {len(retrieved_docs)} documents")

    # 從文件字典中提取內容用於生成提示
    contents = [doc["content"] for doc in retrieved_docs]
    context = "\n\n".join(contents) if contents else "無相關文件"
    prompt = f"以下為參考資訊：\n{context}\n\n請根據以上內容回答問題：{query}"
    return retrieved_docs, prompt
