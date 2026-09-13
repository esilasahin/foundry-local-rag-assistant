import math
from typing import List, Tuple

from . import config, db


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_top_chunks(
    foundry_client, query: str, top_k: int = config.TOP_K
) -> List[Tuple[str, str, float]]:
    """Embed the query and return the top-k most similar (source, content, score) chunks."""
    query_embedding = foundry_client.embed(query)

    scored = [
        (source, content, cosine_similarity(query_embedding, embedding))
        for source, content, embedding in db.get_all_chunks()
    ]
    scored.sort(key=lambda item: item[2], reverse=True)
    return scored[:top_k]
