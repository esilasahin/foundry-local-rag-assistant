from typing import List, Tuple

from . import config
from .retrieval import get_top_chunks


def _build_context(chunks: List[Tuple[str, str, float]]) -> str:
    parts = [f"[Source: {source}]\n{content}" for source, content, _score in chunks]
    return "\n\n---\n\n".join(parts)


def answer_query(foundry_client, question: str) -> str:
    chunks = get_top_chunks(foundry_client, question)
    context = _build_context(chunks)

    messages = [
        {"role": "system", "content": config.SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]

    return foundry_client.chat(messages)
