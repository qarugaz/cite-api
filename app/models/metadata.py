from typing import List, Optional

from pydantic import BaseModel, Field

class Metadata(BaseModel):
    title: str = Field(description="The title of the document")
    abstract: str = Field(description="The abstract of the document")
    authors: List[str] = Field(description="The authors of the document")
    journal: Optional[str] = Field(description="The journal of the document")
    issue: Optional[str] = Field(description="The issue of the document")
    volume: Optional[str] = Field(description="The volume of the document")
    publicationDate: Optional[str] = Field(description="The publication date of the document")
    doi: Optional[str] = Field(description="The DOI of the document")