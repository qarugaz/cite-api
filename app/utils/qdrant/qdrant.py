import uuid

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client.http.models import VectorParams, Distance, PointStruct

from app.config.config import GEMINI_EMBEDDING_MODEL
from app.logging.logging_config import logger


def create_collection(async_client, collection_name: str):
    if not async_client.collection_exists(collection_name):
        async_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )

        return f"Collection {collection_name} created"
    return f"Collection {collection_name} already exists"


def insert_into_collection(async_client, collection_name, article_id, bibtex, meta, chunks, embeddings):
    points = []

    for doc, embedding in zip(chunks, embeddings):
        metadata = doc.metadata
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "section": metadata['section_title'],
                "chunk_id": metadata['chunk_id'],
                "content": doc.page_content,
                "article_id": article_id,
                "meta": meta,
                "bibtex": bibtex
            }
        )
        points.append(point)

    async_client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )

    logger.info(f"Embeddings from {article_id} inserted into the collection {collection_name}")

    return f"Embeddings from {article_id} inserted into the collection"


async def search_with_qdrant(async_client, collection_name, query_text, top_k=12):
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBEDDING_MODEL,
        task_type="RETRIEVAL_DOCUMENT"
    )

    query_embedding = embeddings_model.embed_query(query_text)

    results = await async_client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=top_k,
        score_threshold=0.7,
        with_payload=True
    )

    context_chunks = []

    for result in results.points:
        payload = result.payload
        content = payload.get("content")
        section = payload.get("section")
        source = payload.get("article_id")
        bibtex = payload.get("bibtex")
        meta = payload.get("meta")

        score = result.score

        chunk = {
            "content": content,
            "section": section,
            "article_id": source,
            "metadata": meta,
            "bibtex": bibtex,
            "score": score,
        }

        context_chunks.append(chunk)

    return context_chunks