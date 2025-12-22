from typing import List

from pydantic import BaseModel

from app.models.outline import Outline
from app.models.reference import ReferenceItem

class ExpandItem(BaseModel):
    user_id: str
    document_id: str
    title: str
    text: str
    outline: Outline
    references: List[ReferenceItem]