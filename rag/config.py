from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Model aliases from the Foundry Local catalog.
CHAT_MODEL_ALIAS = "phi-4-mini"
EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b"

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
DB_PATH = BASE_DIR / "data" / "rag_assistant.db"

CHUNK_MAX_CHARS = 800
TOP_K = 3

SYSTEM_PROMPT = (
    "You are an offline document assistant. Answer the user's question using ONLY "
    "the context passages provided below. Each passage is labeled with its source "
    "document. Cite the source document name(s) you used in your answer. "
    "If the context does not contain enough information to answer, say "
    "\"I don't have that information in my documents.\" Do not use outside knowledge."
)
