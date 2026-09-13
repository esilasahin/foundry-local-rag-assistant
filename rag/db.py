import json
import sqlite3
from contextlib import closing
from typing import List, Optional, Tuple

from . import config

# In-memory cache of (source, content, embedding) rows, populated lazily by
# get_all_chunks() and invalidated whenever the table is written to. Retrieval
# runs this query on every question, so caching avoids re-reading and
# re-JSON-decoding the whole table each turn.
_chunks_cache: Optional[List[Tuple[str, str, List[float]]]] = None


def get_connection() -> sqlite3.Connection:
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(config.DB_PATH)


def init_db() -> None:
    with closing(get_connection()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
            """
        )
        conn.commit()


def _invalidate_cache() -> None:
    global _chunks_cache
    _chunks_cache = None


def replace_all_chunks(rows: List[Tuple[str, str, List[float]]]) -> None:
    """Atomically swap the knowledge base for `rows` in a single transaction.

    If anything fails partway (e.g. bad data), the transaction rolls back and
    the previous knowledge base is left untouched instead of ending up half
    replaced.
    """
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("DELETE FROM chunks")
            conn.executemany(
                "INSERT INTO chunks (source, content, embedding) VALUES (?, ?, ?)",
                [(source, content, json.dumps(embedding)) for source, content, embedding in rows],
            )
    _invalidate_cache()


def count_chunks() -> int:
    with closing(get_connection()) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM chunks")
        return cursor.fetchone()[0]


def get_all_chunks() -> List[Tuple[str, str, List[float]]]:
    global _chunks_cache
    if _chunks_cache is None:
        with closing(get_connection()) as conn:
            cursor = conn.execute("SELECT source, content, embedding FROM chunks")
            _chunks_cache = [
                (source, content, json.loads(embedding))
                for source, content, embedding in cursor.fetchall()
            ]
    return _chunks_cache
