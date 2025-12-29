import httpx
import asyncio
import random

from app.utils.text.text import extract_first_author


async def fetch(doi: str, max_retries: int = 5):
    url = f"https://api.crossref.org/works/{doi}"
    timeout = httpx.Timeout(10.0)

    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                response.raise_for_status()  # Raise if HTTP 4xx/5xx

                return response.json()

        except httpx.ReadTimeout:
            print(f"[Retry {attempt}] Timeout fetching {doi}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} for {doi}")
            break  # Don't retry on permanent errors
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

        await asyncio.sleep(2 ** attempt + random.random())  # exponential backoff

    return None


async def get_doi_from_title(title: str, author: str, max_retries: int = 5):
    base_url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "query.author": author,
        "rows": 1,
        "sort": "relevance",
        "order": "desc",
    }

    timeout = httpx.Timeout(10.0)  # You can adjust the timeout

    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(base_url, params=params)
                response.raise_for_status()

                data = response.json()
                items = data.get("message", {}).get("items", [])
                if items:
                    top_result = items[0]
                    return top_result.get("DOI")

                return None

        except httpx.ReadTimeout:
            print(f"Timeout occurred. Retry {attempt} of {max_retries}...")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            break  # No point retrying on a 4xx or 5xx error
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

        await asyncio.sleep(2 ** attempt + random.random())  # exponential backoff

    return None


async def get_article_doi(article):
    title = article["title"]
    authors = article["authors"]
    first_author_last_name = extract_first_author(authors)
    doi = await get_doi_from_title(title, first_author_last_name)
    article["doi"] = doi
    return article

