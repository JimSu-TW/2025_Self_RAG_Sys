from fastapi import APIRouter, UploadFile, File, HTTPException
from helper.documents_helper import save_documents
from utils.logger import get_logger

# Set up logger
logger = get_logger(__name__)

router = APIRouter()


@router.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    try:
        logger.info(f"Received upload request with {len(files)} files")
        save_count = save_documents(files)
        logger.info(f"Successfully saved {save_count} documents")
        return {"status": "success", "saved_count": save_count}
    except Exception as e:
        logger.error(f"Error during document upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
