import json

from app.logging.logging_config import logger
from app.process.article.metadata import generate_metadata_text
from app.utils.crossref.ref import get_doi_from_title, fetch
from app.utils.gcs.gcs import generate_md_text_from_gcs_pdf
from app.utils.qdrant.qdrant import split_and_embed_documents_with_gemini
from app.utils.text.bibtex import generate_bibtex
from app.utils.text.text import get_cleaned_string, parse_metadata, extract_first_author, parse_crossref_data


async def process_pdf(user_id, article, collection_name, qdrant_client):
    article_id = article["articleId"]
    document_blob_name = article["blob"]

    logger.info(f"Processing PDF {article_id} and {document_blob_name}")

    md_blob_name, first_two_pages_text = generate_md_text_from_gcs_pdf(user_id, article_id, document_blob_name)

    metadata_text = await generate_metadata_text(first_two_pages_text)

    metadata_json = get_cleaned_string(metadata_text)

    metadata = parse_metadata(metadata_json)
    title = metadata["title"]
    meta_authors = metadata["authors"]
    authors = ", ".join(meta_authors)
    first_author_last_name = extract_first_author(authors)

    doi = metadata["doi"]
    if doi is None:
        doi = await get_doi_from_title(title, first_author_last_name)
        metadata["doi"] = doi

    if doi:
        crossref_data = await fetch(doi)

        crossref_json = json.dumps(crossref_data)
        logger.info(f"UserId: {user_id} Crossref Response: {crossref_data}")

        data = parse_crossref_data(crossref_json)
        if data is not None:
            metadata["publication"] = data["publication"]
            metadata["is_referenced_by_count"] = data["is_referenced_by_count"]
            metadata["reference_count"] = data["reference_count"]
            metadata["type"] = data["type"]
            metadata["pages"] = data["pages"]
            metadata["issue"] = data["issue"] if "issue" in data else ""
            metadata["volume"] = data["volume"] if "volume" in data else ""
            metadata["publisher"] = data["publisher"]
            metadata["year"] = data["year"] if "year" in data else "2020"
            metadata["month"] = data["month"] if "month" in data else ""

    metadata["authors"] = authors
    bibtex = generate_bibtex(metadata)

    await split_and_embed_documents_with_gemini(qdrant_client, article_id, bibtex, metadata, md_blob_name,
                                                collection_name)

    metadata["id"] = article_id
    metadata["hash"] = ""
    metadata["pdf"] = document_blob_name
    metadata["md"] = md_blob_name

    logger.info(f"Finished Processing PDF {article_id} and {document_blob_name}")
    logger.info(json.dumps(metadata, indent=4))
    return metadata
