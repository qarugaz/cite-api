from functools import lru_cache

from google import genai

from app.config.config import GOOGLE_API_KEY

@lru_cache(maxsize=1)
def get_genai_client():
    client = genai.Client(api_key=GOOGLE_API_KEY)
    return client
