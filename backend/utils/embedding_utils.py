from sentence_transformers import SentenceTransformer
import faiss
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


def generate_embeddings(documents):
    logger.info(f"Starting to generate embeddings for {len(documents)} documents")

    logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    logger.info("Encoding documents to embeddings")
    # 提取文件內容進行嵌入
    contents = [doc["content"] for doc in documents]
    embeddings = model.encode(contents)
    logger.info(f"Generated embeddings with shape: {embeddings.shape}")

    logger.info("Creating FAISS index")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    logger.info(f"FAISS index created with {index.ntotal} vectors")

    return embeddings, index
