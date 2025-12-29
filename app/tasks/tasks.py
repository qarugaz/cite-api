import asyncio
import json

from app.celery_app import celery
from app.logging.logging_config import logger
from app.process.article.article import process_articles_metadata

@celery.task(queue="priority")
def articles_metadata_task(user_id, articles):
    logger.info("Processing articles metadata task")
    logger.info(json.dumps(articles, indent=4))
    result = asyncio.run(
        process_articles_metadata(user_id, articles)
    )
    return result