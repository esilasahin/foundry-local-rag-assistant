from typing import List

from foundry_local_sdk import Configuration, FoundryLocalManager

from . import config


class FoundryClient:
    """Resolves the chat and embedding models and exposes ready-to-use clients."""

    def __init__(self):
        if FoundryLocalManager.instance is None:
            FoundryLocalManager.initialize(Configuration(app_name="foundry_local_rag_assistant"))
        self._manager = FoundryLocalManager.instance

        self._chat_model = self._manager.catalog.get_model(config.CHAT_MODEL_ALIAS)
        self._embedding_model = self._manager.catalog.get_model(config.EMBEDDING_MODEL_ALIAS)

        if self._chat_model is None:
            raise RuntimeError(f"Chat model alias '{config.CHAT_MODEL_ALIAS}' not found in catalog.")
        if self._embedding_model is None:
            raise RuntimeError(
                f"Embedding model alias '{config.EMBEDDING_MODEL_ALIAS}' not found in catalog."
            )

    def load(self) -> None:
        print(f"Loading embedding model '{config.EMBEDDING_MODEL_ALIAS}'...")
        self._embedding_model.download()
        self._embedding_model.load()

        print(f"Loading chat model '{config.CHAT_MODEL_ALIAS}'...")
        self._chat_model.download()
        self._chat_model.load()

    def unload(self) -> None:
        """Unload both models, best-effort: a failure on one still lets the other unload."""
        errors = []
        for alias, model in (
            (config.EMBEDDING_MODEL_ALIAS, self._embedding_model),
            (config.CHAT_MODEL_ALIAS, self._chat_model),
        ):
            try:
                model.unload()
            except Exception as exc:
                errors.append(f"{alias}: {exc}")
        if errors:
            print("Warning: failed to unload some models -> " + "; ".join(errors))

    def embed(self, text: str) -> List[float]:
        client = self._embedding_model.get_embedding_client()
        response = client.generate_embedding(text)
        return response.data[0].embedding

    def embed_many(self, texts: List[str]) -> List[List[float]]:
        client = self._embedding_model.get_embedding_client()
        response = client.generate_embeddings(texts)
        return [item.embedding for item in response.data]

    def chat(self, messages: list) -> str:
        client = self._chat_model.get_chat_client()
        response = client.complete_chat(messages)
        return response.choices[0].message.content
