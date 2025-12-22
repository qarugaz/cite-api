from pydantic import BaseModel

class WriterItem(BaseModel):
    user_id: str
    document_id: str
    query: str



