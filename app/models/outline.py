from pydantic import BaseModel, Field
from typing import List, Optional

class Subsection(BaseModel):
    id: str = Field(
        ...,
        description="Stable identifier used for UI actions and AI follow-ups"
    )
    heading: str = Field(
        ...,
        description="Subsection title"
    )
    goal: str = Field(
        ...,
        description="One-sentence description of the subsection's purpose"
    )


class Section(BaseModel):
    id: str = Field(
        ...,
        description="Stable identifier used for UI actions and AI follow-ups"
    )
    heading: str = Field(
        ...,
        description="Section title"
    )
    goal: str = Field(
        ...,
        description="One-sentence description of the section's purpose"
    )
    subsections: Optional[List[Subsection]] = Field(
        default_factory=list,
        description="Optional nested subsections"
    )


class Outline(BaseModel):
    title: str = Field(
        ...,
        description="Full working title of the paper or document"
    )
    sections: List[Section]