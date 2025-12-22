from functools import lru_cache

from qdrant_client import AsyncQdrantClient

from app.config.config import QDRANT_URL


@lru_cache(maxsize=1)
def get_qdrant_client() -> AsyncQdrantClient:
    client = AsyncQdrantClient(
        url=QDRANT_URL,
        timeout=120,
        port=443,
        https=True,
        prefer_grpc=False
    )

    return client
