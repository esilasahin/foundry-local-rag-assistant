# foundry-local-rag-assistant

An offline document question-answering assistant built with Microsoft Foundry Local, RAG,
Python, embeddings, and SQLite.

The assistant answers questions about a small local document collection
([data/documents](data/documents)) by embedding the documents, storing the embeddings in a
SQLite database, retrieving the most relevant chunks for each question via cosine
similarity, and feeding that context to a local chat model — all with zero network calls
once the models are downloaded.

## How it works

1. **Ingestion** ([rag/ingest.py](rag/ingest.py)) — every `.md`/`.txt` file in
   `data/documents/` is split into paragraph-sized chunks, embedded with the Foundry Local
   embedding model, and stored in SQLite ([rag/db.py](rag/db.py)).
2. **Retrieval** ([rag/retrieval.py](rag/retrieval.py)) — a question is embedded with the
   same model, compared against every stored chunk with cosine similarity, and the top-k
   matches are selected.
3. **Generation** ([rag/qa.py](rag/qa.py)) — the retrieved chunks are inserted into the
   prompt and sent to the local chat model, which is instructed to answer only from that
   context and to say when it doesn't know.

## Setup

```bash
pip install -r requirements.txt
```

Foundry Local downloads and manages the models automatically on first use — no separate
install step is required.

## Usage

```bash
python main.py
```

On first run this ingests the documents in `data/documents/` into `data/rag_assistant.db`
and then starts an interactive prompt. Type a question, or `exit` to quit.

To rebuild the knowledge base after changing the documents:

```bash
python main.py --reingest
```

## Configuration

Model aliases, chunk size, top-k, and the system prompt live in
[rag/config.py](rag/config.py).
