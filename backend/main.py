# main.py
from fastapi import FastAPI
from router import documents_router, query_router
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
        title="RAG Backend API",
        version="1.0",
        description="Backend API for RAG Document Retrieval System",
        docs_url="/",
        redoc_url=None,
        openapi_url="/api/v1/openapi.json",
    )

# 註冊路由
app.include_router(documents_router.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(query_router.router, prefix="/api/v1/query", tags=["Query"])


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "RAG Backend API is running"}
