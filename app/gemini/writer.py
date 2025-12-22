import random
import time

from google.genai import types
from app.init.google import get_genai_client
from app.logging.logging_config import logger
from app.models.outline import Outline

async def generate_topic_outline(model, prompt):
    client = get_genai_client()
    retries = 5

    for attempt in range(retries):
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Outline
                )
            )
            return response.text

        except Exception as e:
            logger.error(f"Exception on generate_queries_with_text")
            wait = (2 ** attempt) + random.uniform(0, 1)
            logger.error(f"Exception on attempt {attempt + 1}: {e}. Retrying in {wait:.2f}s.")
            time.sleep(wait)

    else:
        logger.error(f"Failed generate_queries_with_text after all retries")
        return "Error"
