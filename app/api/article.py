from fastapi import APIRouter, Request, Depends

from app.auth.auth import validate_hmac_signature
from app.tasks.tasks import articles_metadata_task

from app.logging.logging_config import logger

router = APIRouter(
    prefix="/api/article",
    tags=["api/article"]
)

@router.post("/generate-metadata")
async def generate_document_metadata(request: Request,
                                     is_authenticated: bool = Depends(validate_hmac_signature)):
    data = await request.json()
    logger.info(f"Received request: {data}")
    user_id = data.get("user_id")
    articles = data.get("articles")

    task = articles_metadata_task.apply_async(
        args=[
            user_id,
            articles
        ]
    )

    return {"task_id": task.id, "message": "Processing Metadata"}