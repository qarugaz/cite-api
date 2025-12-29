import random
import time

from app.init.google import get_genai_client
from app.logging.logging_config import logger
from app.models.metadata import Metadata
from google.genai import types


async def generate_article_metadata_with_text(model, prompt, json):
    client = get_genai_client()
    retries = 5

    for attempt in range(retries):
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=[json, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Metadata
                )
            )
            return response.text

        except Exception as e:
            logger.error(f"Exception on generate_article_metadata_with_text")
            wait = (2 ** attempt) + random.uniform(0, 1)
            logger.error(f"Exception on attempt {attempt + 1}: {e}. Retrying in {wait:.2f}s.")
            time.sleep(wait)

    else:
        print("Failed after all retries.")
        return ""
