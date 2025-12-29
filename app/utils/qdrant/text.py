import re
from typing import List, Dict

import tiktoken
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_markdown_by_headers(md_text: str) -> List[Dict]:
    pattern = r"(#{1,6})\s+(.*)"
    matches = list(re.finditer(pattern, md_text))
    chunks = []

    for i, match in enumerate(matches):
        header = f"{match.group(1)} {match.group(2).strip()}"
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        content = md_text[start:end].strip()
        chunks.append({
            "text": f"{header}\n{content}".strip(),
            "section_title": header,
        })

    return chunks


def tokenize_split_long_chunks(
        header_chunks: List[Dict],
        max_tokens: int = 1024,
        overlap: int = 256,
        model_encoding="cl100k_base") -> List[Document]:
    tokenizer = tiktoken.get_encoding(model_encoding)
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=max_tokens,
        chunk_overlap=overlap
    )

    docs = []
    for i, chunk in enumerate(header_chunks):
        text = chunk["text"]
        section = chunk["section_title"]
        token_count = len(tokenizer.encode(text))

        doc = Document(
            page_content=text,
            metadata={
                "section_title": section,
                "orig_token_count": token_count,
                "chunk_id": i
            }
        )

        if token_count > max_tokens:
            split_docs = splitter.split_documents([doc])
            docs.extend(split_docs)
        else:
            docs.append(doc)

    return docs
