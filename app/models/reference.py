from pydantic import BaseModel


class ReferenceItem(BaseModel):
    id: str
    text: str