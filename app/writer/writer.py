from app.config.config import GEMINI_MODEL
from app.gemini.writer import generate_topic_outline
from app.utils.citation.citation import generate_citation

model = GEMINI_MODEL


async def generate_outline_from_topic(topic, document_type, academic_level):
    prompt = f"""
    You are an expert academic writing assistant for higher education and research.
    You generate structured, publication-quality outlines tailored to different
    types of academic articles.
    
    You understand the conventions, structure, and expectations of:
    - Essays
    - Literature Reviews
    - Term Papers
    - Case Studies
    - Research Papers
    - Conceptual/Theoretical Papers
    
    You always adapt the outline structure to the requested article type.
    
    Generate a detailed academic outline using the following inputs:

    Topic:
    {topic}
    
    Article Type:
    {document_type}
    
    
    Academic Level:
    {academic_level}
    
    Requirements:
    - Use the standard structure appropriate for the specified Article Type
    - Apply clear hierarchical numbering (1, 1.1, 1.1.1)
    - Each section must include:
      - A short purpose/goal (1 sentence)
      - 3–6 bullet-point writing suggestions explaining what to cover
    - Maintain formal academic tone
    - Do NOT write full paragraphs
    - Do NOT include citations
    """

    response = await generate_topic_outline(model, prompt)
    return response

async def expand_section_from_prompt(
        section_header,
        section_goal,
        chunks,
        text_so_far,
        citation_style
        ):

    citation = await generate_citation(citation_style)

    inline_style = citation[0]
    reference_style = citation[1]

    prompt = f"""
    You are writing ONE section of a research paper.

    Section:
    - Heading: {section_header}
    - Goal: {section_goal}
    
    Available context:
    {{SOURCES_JSON}}
    
    Instructions:
    - Write 1–3 coherent academic paragraphs for THIS SECTION ONLY.
    - Every paragraph MUST include at least one citation.
    - Use in-text citation format: (SourceID).
    - Do NOT invent sources.
    - If evidence is insufficient, state this explicitly.
    - Follow the section goal and suggestions closely.
    - Do NOT repeat the section heading.
    - Do NOT summarize other sections.
    - Avoid speculative or unsupported claims.
    
    ### Citation Rules:
            **Citation Style:** Strictly follow the citation rules below**.
            - inline citation: {inline_style}
            - bibliography: {reference_style}
            - Every in-text citation must appear in the References section — no missing entries allowed.
            - Every entry in the References section must be cited at least once in the main text — no orphaned references.
            ** A reference entry must be unique and appear only once in the references section.**
        
    
    """



