from connector.db_connector import save_embeddings
from utils.file_parsers import parse_uploaded_files
from utils.embedding_utils import generate_embeddings
from utils.logger import get_logger

# Configure the logger
logger = get_logger(__name__)


def save_documents(files):
    logger.info(f"Starting to process {len(files)} files")
    try:
        documents = parse_uploaded_files(files)
        logger.info(f"Parsed {len(documents)} documents")

        embeddings, _ = generate_embeddings(documents)
        logger.info(f"Generated embeddings for {len(embeddings)} documents")

        save_embeddings(documents, embeddings)
        logger.info(f"Successfully saved {len(documents)} documents with embeddings")

        return len(documents)
    except Exception as e:
        logger.error(f"Error in save_documents: {str(e)}")
        raise
