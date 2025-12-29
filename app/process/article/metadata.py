from app.config.config import GEMINI_MODEL
from app.gemini.article import generate_article_metadata_with_text

model = GEMINI_MODEL

async def generate_metadata_text(text):
    prompt = f"""
    You are an academic assistant specialized in text analysis.
    You will be given the first few pages of an academic article.
    Your task is to extract metadata from the text. 
    The metadata to be extracted from the article text should include if available:
    1. Title
    2. Abstract
    3. Authors
    4. Keywords
    5. Journal
    6. Issue
    7. Volume
    8. Publication Date
    9. DOI
    """

    response = await generate_article_metadata_with_text(model, prompt, text)
    return response