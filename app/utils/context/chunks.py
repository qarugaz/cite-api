from collections import defaultdict
from app.config.config import GEMINI_MODEL, COLLECTION_PREFIX
from app.init.qdrant import get_qdrant_client
from app.utils.qdrant.qdrant import search_with_qdrant

model = GEMINI_MODEL


def format_context_for_llm(context_chunks) -> str:
    """
    Formats the list of context chunks into a single string suitable for the LLM prompt.
    You might want to add delimiters or specific instructions for the LLM.
    """
    context_texts = []

    if not context_chunks:
        return "No specific context found."
    # Join chunks, perhaps adding some markers
    for chunk in context_chunks:
        label = f"{chunk['article_id']} > {chunk['section']}"
        bibtex = f"{chunk['bibtex']}"
        context_texts.append(f"[{label}]: [{bibtex}]: {chunk['content']}")

    formatted_context = "\n\n".join(context_texts)
    return f"Retrieved Context:\n{formatted_context}\n\n"


async def get_query_context_chunks(user_id, query, k):
    qdrant_client = get_qdrant_client()
    collection_name = f"{COLLECTION_PREFIX}-{user_id}"
    context_chunks = await search_with_qdrant(qdrant_client, collection_name, query, k)
    return context_chunks


async def get_context_chunks(user_id, queries):
    qdrant_client = get_qdrant_client()
    collection_name = f"{COLLECTION_PREFIX}-{user_id}"
    context_chunks = []
    for query in queries:
        chunks = await search_with_qdrant(qdrant_client, collection_name, query, 12)
        context_chunks.extend(chunks)
    return context_chunks


def format_chunks_for_llm(chunks) -> str:
    papers = defaultdict(list)

    for chunk in chunks:
        meta = chunk["metadata"]
        paper_key = chunk["article_id"]

        # Metadata fallback
        title = meta.get("title", "Unknown Title")
        authors = meta.get("authors", "Unknown Authors")
        year = meta.get("year", "n.d.")
        journal = meta.get("journal", "")
        vol = meta.get("volume", "")
        num = meta.get("number", "")
        pages = meta.get("pages", "")
        doi = meta.get("doi", "")

        # Clean section and content
        section = chunk.get("section", "").replace("##", "").strip() or "Unknown Section"
        content = chunk["content"].strip()

        # Append formatted section
        papers[paper_key].append({
            "section": section,
            "content": content,
            "meta": {
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "volume": vol,
                "number": num,
                "pages": pages,
                "doi": doi,
            }
        })

    # Format the grouped content
    formatted_output = ""

    for paper_id, sections in papers.items():
        meta = sections[0]["meta"]
        formatted_output += (
            f"\n\n## Paper: {meta['authors']} ({meta['year']}), *{meta['title']}*\n"
            f"### Source: {meta['journal']}, Vol. {meta['volume']}, No. {meta['number']}, pp. {meta['pages']}\n"
            f"### DOI: {meta['doi']}\n"
        )

        for section in sections:
            formatted_output += f"\n### Section: {section['section']}\n{section['content']}\n"

    return formatted_output.strip()