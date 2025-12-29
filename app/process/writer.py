from app.config.config import GEMINI_MODEL
from app.gemini.writer import generate_topic_outline

model = GEMINI_MODEL

async def process_generate_outline_from_prompt(topic):
    prompt = f"""
    Generate a structured research outline for the following topic:

    Topic: {topic}

    Requirements:
    - The outline must be suitable for an academic or research-oriented paper.
    - Use clear section and subsection hierarchy.
    - Each section must include:
      - A short purpose/goal (1 sentence)
      - 3–6 bullet-point writing suggestions explaining what to cover
    - Do NOT write full paragraphs or citations.
    - Be neutral, precise, and academically appropriate.
    """

    response = await generate_topic_outline(model, prompt)
    return response