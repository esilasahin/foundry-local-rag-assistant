# Microsoft Foundry Local

Foundry Local is an end-to-end local AI solution that provides a lightweight runtime and
SDK for running large language models completely on a user's device. It ships with a
curated catalog of optimized models so developers do not have to search for or convert
models themselves.

No cloud account and no GPU are required to use Foundry Local. It automatically downloads
and manages models, and runs inference using whatever hardware acceleration is available
on the device, including CPU, GPU, or NPU. This lets applications deliver local, offline AI
with zero network calls once the model has been downloaded.

Foundry Local exposes an OpenAI-compatible API surface. A Python application first
initializes a `FoundryLocalManager`, looks up a model by its catalog alias (for example
`phi-4-mini` for chat or `qwen3-embedding-0.6b` for embeddings), downloads and loads that
model, and then obtains a chat client or an embedding client from it. Those clients mirror
the familiar OpenAI `chat.completions` and `embeddings` request shapes, which makes it easy
to reuse existing prompt-engineering knowledge.

Foundry Local supports Windows, macOS, and Linux, which makes it a good fit for classroom
and workshop settings where students bring a mix of laptops.
