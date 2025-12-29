import calendar
from datetime import datetime
import hashlib
import json
import re
import unicodedata

from app.logging.logging_config import logger


def get_cleaned_string(text) -> str:
    cleaned_json_string = text.replace("```json", "").replace("```", "").strip()
    return cleaned_json_string


def get_cleaned_md_string(text) -> str:
    cleaned_json_string = text.replace("```markdown", "").replace("```", "").strip()
    return cleaned_json_string

def parse_metadata(metadata_json):
    try:
        data = json.loads(metadata_json)
        return data
    except json.decoder.JSONDecodeError:
        clean_json = remove_escape_sequences(metadata_json)
        data = json.loads(clean_json)
        return data


def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


def remove_escape_sequences(string):
    return string.encode('utf-8').decode('unicode_escape')


# Normalize text
def normalize(text):
    text = strip_accents(text.lower())
    text = re.sub(r'[^a-z0-9\s]', '', text)  # keep only letters and numbers
    return text.strip()


def extract_first_author(authors):
    authors_normalized = normalize(authors)
    first_author = authors_normalized.split('and')[0].strip()
    last_name = first_author.split(',')[0]
    return last_name


def extract_significant_title_words(title, max_words=6):
    stopwords = {'the', 'a', 'an', 'of', 'and', 'in', 'on', 'for', 'with', 'to', 'by', 'at'}
    words = normalize(title).split()
    significant = [w for w in words if w not in stopwords]
    return ' '.join(significant[:max_words])


def create_smarter_hash(title, authors, year):
    if not title or not authors or not year:
        return None
    first_author = extract_first_author(authors)
    title_part = extract_significant_title_words(title)
    combined = f"{first_author}{year}{title_part}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()


def parse_crossref_data(crossref_json):
    try:
        data = {}
        crossref_data = json.loads(crossref_json)
        metadata = crossref_data['message']

        is_referenced_by_count = metadata.get("is-referenced-by-count", None)
        reference_count = metadata.get("reference-count", None)
        publisher = metadata["publisher"]
        doctype = metadata["type"]
        pages = metadata.get("page", None)
        issue = metadata.get("issue", None)
        volume = metadata.get("volume", None)
        publication = metadata["container-title"][0] if metadata.get("container-title") else None

        data["reference_count"] = reference_count
        data["is_referenced_by_count"] = is_referenced_by_count
        data["publisher"] = publisher
        data["type"] = doctype
        data["pages"] = pages
        data["issue"] = issue if "issue" in metadata else None
        data["volume"] = volume if "volume" in metadata else None
        data["publication"] = publication

        date = get_formatted_year_month(metadata)
        if date:
            data["month"] = date[0]
            data["year"] = date[1]

        return data
    except json.decoder.JSONDecodeError:
        logger.error(f"Could not parse crossref data from {crossref_json}")
        return None
    except Exception as e:
        logger.error(f"Could not parse crossref data {e}")
        return None


def get_formatted_year_month(metadata):
    date_parts = metadata.get('published', {}).get('date-parts')

    if date_parts:
        year = date_parts[0][0]
        month = date_parts[0][1] if len(date_parts[0]) > 1 else None

        if month:
            month_name = calendar.month_name[month]
            return month_name, str(year)
        else:
            return "January", str(year)
    return None


def get_year_from_date(date_str: str):
    date_obj = datetime.strptime(date_str, "%d %B %Y")
    year = date_obj.year

    return year


def get_references_with_hash(references_json):
    try:
        references = json.loads(references_json)
        for ref in references:
            title = ref['title']
            year = ref['year'] if ref['year'] else "2000"
            author = ref['author']
            ref_hash = create_smarter_hash(title, author, year)
            ref['hash'] = ref_hash
        return json.dumps(references)
    except json.decoder.JSONDecodeError:
        print("JSON Decode Error")
        return None
    except Exception as e:
        print(e)
        return None


def replace_double_backlash(markdown):
    new_markdown = markdown.replace("\\\\", "\\")
    return new_markdown


def replace_single_backlash(markdown):
    new_markdown = markdown.replace("\\", "")
    return new_markdown