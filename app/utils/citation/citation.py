from io import BytesIO

import httpx
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem, formatter
from citeproc.source.json import CiteProcJSON


def warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography."
          .format(citation_item.key))

async def generate_citation(name:str):
    bib_entry = [
        {
            "id": "item1",
            "type": "article-journal",
            "author": [
                {"family": "Goodfellow", "given": "Ian"},
                {"family": "Bengio", "given": "Yoshua"},
                {"family": "Courville", "given": "Aaron"}
            ],
            "title": "Deep Learning",
            "container-title": "Nature",
            "volume": "521",
            "issue": "7553",
            "page": "436–444",
            "issued": {"date-parts": [[2015, 5, 28]]},
            "DOI": "10.1038/nature14539"
        }
    ]

    style_url = f"https://www.zotero.org/styles/{name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(style_url)
        response.raise_for_status()
        csl = CitationStylesStyle(BytesIO(response.content), validate=False)

    # Step 3: Create bibliography processor
    source = CiteProcJSON(bib_entry)
    bibliography = CitationStylesBibliography(csl, source, formatter.html)

    # Step 4: Inline citation
    try:
        citation = Citation([CitationItem("item1")])
        bibliography.register(citation)
        inline = bibliography.cite(citation, warn)
        if inline == "":
            inline = "[1]"

        output = [str(item) for item in bibliography.bibliography()]
        bib_output = normalize_text(output[0])
    except Exception as e:
        print(e)
        inline = "[1]"
        bib_output = "[1]I. Goodfellow, Y. Bengioand A. Courville, “Deep Learning”, <i>Nature</i>, vol. 521, no. 7553, pp. 436–444, May 2015, doi: 10.1038/nature14539."


    return inline, bib_output

def normalize_text(text):
    replacements = {
        '“': '"',   # Left double quote
        '”': '"',   # Right double quote
        '‘': "'",   # Left single quote
        '’': "'",   # Right single quote
        '–': '-',   # En dash
        '—': '-',   # Em dash
        '…': '...', # Ellipsis (optional)
    }

    for smart, ascii_equiv in replacements.items():
        text = text.replace(smart, ascii_equiv)
    return text