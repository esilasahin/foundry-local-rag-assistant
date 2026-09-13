import re
from pathlib import Path
from typing import List, Tuple

from . import config, db


def _split_into_chunks(text: str, max_chars: int = config.CHUNK_MAX_CHARS) -> List[str]:
    """Group paragraphs into passage-sized chunks, keeping paragraphs intact."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    chunks: List[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) > max_chars and current:
            chunks.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def _load_documents(documents_dir: Path) -> List[Tuple[str, str]]:
    paths = sorted(documents_dir.glob("*.md")) + sorted(documents_dir.glob("*.txt"))
    return [(path.name, path.read_text(encoding="utf-8")) for path in paths]


def run_ingestion(foundry_client, documents_dir: Path = config.DOCUMENTS_DIR) -> int:
    """Chunk every document in `documents_dir`, embed each chunk, and store it in SQLite.

    All embeddings are computed and collected in memory first, and the database is
    only touched once everything succeeded, via a single atomic replace. This way a
    failure partway through (e.g. the embedding service erroring on one document)
    leaves the previous, complete knowledge base in place instead of a partially
    ingested one.
    """
    db.init_db()

    documents = _load_documents(documents_dir)
    if not documents:
        raise RuntimeError(f"No documents found in {documents_dir}")

    rows: List[Tuple[str, str, List[float]]] = []
    for source, text in documents:
        chunks = _split_into_chunks(text)
        if not chunks:
            continue
        embeddings = foundry_client.embed_many(chunks)
        rows.extend(
            (source, chunk_text, embedding) for chunk_text, embedding in zip(chunks, embeddings)
        )

    if not rows:
        raise RuntimeError(f"No chunks produced from documents in {documents_dir}")

    db.replace_all_chunks(rows)
    return len(rows)
