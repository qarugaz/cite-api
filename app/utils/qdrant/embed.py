import asyncio
import random

from google.api_core.exceptions import ResourceExhausted

from app.config.config import GEMINI_EMBEDDING_MODEL
from app.init.google import get_genai_client

BATCH_SIZE = 10
MAX_CONCURRENT = 5
MAX_RETRIES = 5

async def embed_chunks(documents):

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    embeddings = []

    async def run_batch(batch):
        async with semaphore:
            return await embed_batch(batch)

    tasks = [
        run_batch(documents[i:i + BATCH_SIZE])
        for i in range(0, len(documents), BATCH_SIZE)
    ]

    for result in await asyncio.gather(*tasks):
        embeddings.extend(result)

    return embeddings

async def embed_batch(batch, attempt=1):
    client = get_genai_client()
    model = GEMINI_EMBEDDING_MODEL

    try:
        resp = await client.aio.models.embed_content(
            model=model,
            contents=batch
        )
        return [item.values for item in resp.embeddings]

    except ResourceExhausted as e:
        print(e)
        if attempt > MAX_RETRIES:
            raise
        wait_time = (2 ** attempt) + random.uniform(0, 1)
        print(f"Rate limited. Retrying in {wait_time:.2f}s (attempt {attempt})...")
        await asyncio.sleep(wait_time)
        return await embed_batch(batch, attempt + 1)