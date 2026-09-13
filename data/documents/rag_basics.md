# Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation, or RAG, is an AI design pattern used to ground a language
model's answers in a specific set of documents instead of relying only on what the model
memorized during training. RAG has three steps: retrieve relevant passages from a
knowledge base, augment the model's prompt with those passages as context, and generate an
answer using that context.

The main benefit of RAG is that it reduces hallucination and lets the model cite sources,
because the answer is grounded in text the application actually retrieved rather than in
the model's general knowledge. This is especially useful for domain-specific assistants,
such as a chatbot that answers questions about a company's internal documents or a
student's course notes, where a general-purpose model would otherwise guess or make
something up.

RAG relies on an embedding model to convert both the documents and the user's query into
numeric vectors, and on a similarity measure such as cosine similarity to find which
document chunks are closest in meaning to the query. The retrieved chunks are then inserted
into the prompt sent to the chat model, usually as part of a system or context message that
instructs the model to answer only from the supplied text.
