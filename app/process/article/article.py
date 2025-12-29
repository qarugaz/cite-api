import asyncio

from app.config.config import NEXT_URL, COLLECTION_PREFIX
from app.init.qdrant import get_qdrant_client
from app.logging.logging_config import logger
from app.process.article.pdf import process_pdf
from app.utils.article.event import send_metadata_event
from app.utils.qdrant.qdrant import create_collection


async def process_articles_metadata(user_id, articles):
    event_url = f"{NEXT_URL}/api/task/metadata"

    collection_name = f"{COLLECTION_PREFIX}-{user_id}"
    qdrant_client = get_qdrant_client()

    logger.info(f"UserId: {user_id} Processing Articles")

    send_metadata_event(event_url, user_id, "Started Processing", "")

    await create_collection(qdrant_client, collection_name)

    tasks = [process_pdf(user_id, article, collection_name, qdrant_client) for article in articles]

    items = []
    for i, coro in enumerate(asyncio.as_completed(tasks)):
        item = await coro
        msg = f"Processed PDF: {i}"
        logger.info(msg)
        send_metadata_event(event_url, user_id, msg, "")
        items.append(item)

    print("items")
    print(items)
    send_metadata_event(event_url, user_id, "Finished Processing", items)

    return "OK"


