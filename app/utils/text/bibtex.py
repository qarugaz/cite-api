import re


def generate_bibtex(metadata: dict) -> str:
    key = generate_key(metadata)

    bibtex = f"""@article{{{key},
      title={{ {metadata.get('title', '')} }},
      author={{ {metadata.get('authors', '')} }},
      journal={{ {metadata.get('journal', '')} }},
      year={{ {metadata.get('year', '')} }},
      volume={{ {metadata.get('volume', '')} }},
      number={{ {metadata.get('number', '')} }},
      pages={{ {metadata.get('pages', '')} }},
      doi={{ {metadata.get('doi', '')} }}
    }}"""
    return bibtex


def generate_key(metadata: dict) -> str:
    author = metadata.get("authors")
    authors = author.split(",")
    year = metadata.get("year", "n.d.")
    title = metadata.get("title", "")

    first_author_lastname = authors[0].split()[-1] if authors else "unknown"
    title_slug = re.sub(r'\W+', '', title.lower().split()[0])

    return f"{first_author_lastname}{year}{title_slug}"