from foundry_local_sdk import Configuration, FoundryLocalManager


MODEL_NAME = "phi-4-mini"


def main():
    print("Foundry Local RAG Assistant başlatılıyor...")

    config = Configuration(app_name="foundry_local_rag_assistant")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model(MODEL_NAME)

    print("Model hazırlanıyor...")
    model.download()
    model.load()

    try:
        client = model.get_chat_client()

        messages = [
            {
                "role": "system",
                "content": (
                    "Sen Türkçe cevap veren yardımcı bir yapay zekâ asistanısın. "
                    "Cevaplarını kısa, açık ve anlaşılır şekilde ver."
                ),
            },
            {
                "role": "user",
                "content": "RAG nedir? Tek paragrafta açıkla.",
            },
        ]

        response = client.complete_chat(messages)
        answer = response.choices[0].message.content

        print("\nModelin cevabı:")
        print(answer)

    finally:
        model.unload()
        print("\nModel GPU belleğinden çıkarıldı.")


if __name__ == "__main__":
    main()