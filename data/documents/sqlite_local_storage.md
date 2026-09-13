# SQLite for Local Data Storage

SQLite is a serverless, self-contained SQL database engine where an entire database lives
in a single file on disk. It is the most widely deployed database engine in the world and
requires no separate server process, no network configuration, and almost no setup, which
makes it well suited for small, local applications such as an offline RAG assistant.

In a local RAG project, SQLite is typically used as a lightweight vector store: a table
holds each document chunk's source name, its text content, and its embedding vector. The
embedding vector can be stored as a JSON-serialized list of floats in a text column, or as
a binary blob, since SQLite does not have a native vector type.

For small collections of documents, the common retrieval approach is to load every stored
embedding into memory and compute cosine similarity against the query embedding in Python,
then sort and take the top few matches. This brute-force approach is fast enough for
collections of a few hundred chunks. For much larger collections, a dedicated vector
database or a SQL extension with native vector search would be a better choice.
