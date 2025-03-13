from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from helper.query_helper import handle_query
from utils.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


class QueryRequest(BaseModel):
    query: str


@router.post("/")
def query_documents(request: QueryRequest):
    logger.info(f"Received query request: {request.query}")
    try:
        answer, references = handle_query(request.query)
        logger.info("Query processed successfully")
        logger.info(f"Answer: {answer}")
        return {"answer": answer, "references": references}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
