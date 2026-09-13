# Prompt Engineering for Q&A Assistants

Retrieving the right document chunks is only half of a good RAG answer; how the retrieved
text is presented to the model matters just as much. Chat-style models accept a list of
messages with roles. The `system` role is used for instructions about how the model should
behave, while the `user` role carries the actual question and any retrieved context.

For a document Q&A assistant, a good system prompt tells the model to answer using only the
provided context, to cite which source document it used, and to say it does not know the
answer when the context does not contain enough information. This last instruction is
important: without it, a model will often try to answer anyway using its own general
knowledge, which defeats the purpose of grounding the answer in the local documents.

Simple, explicit instructions work better than vague ones. Phrases like "answer only from
the context below" and "if you are not sure, say you don't know" are more reliable than
open-ended instructions like "be helpful." Testing the same question with and without
supplied context is a good way to see how much the prompt design changes the model's
behavior.
