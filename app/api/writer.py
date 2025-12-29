from fastapi import APIRouter, Depends

from app.auth.auth import validate_hmac_signature
from app.models.expand import ExpandItem
from app.models.writer import WriterItem
from app.utils.context.chunks import get_query_context_chunks
from app.writer.writer import expand_section_from_prompt, generate_outline_from_topic

router = APIRouter(
    prefix="/api/writer",
    tags=["api/writer"],
)

@router.post("/generate-outline")
async def generate_outline(item: WriterItem, is_authenticated: bool = Depends(validate_hmac_signature)):
    response = await generate_outline_from_topic(item.query, item.type, item.level)
    return response

@router.post("/expand-section")
async def expand_section(item: ExpandItem, is_authenticated: bool = Depends(validate_hmac_signature)):
    context_chunks = await get_query_context_chunks(item.user_id, item.query, 3)
    response = await expand_section_from_prompt(item.query, context_chunks, item.user_id, item.document_id)
    return response

