import argparse

from rag import config, db
from rag.foundry_client import FoundryClient
from rag.ingest import run_ingestion
from rag.qa import answer_query


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Offline local RAG assistant powered by Microsoft Foundry Local."
    )
    parser.add_argument(
        "--reingest",
        action="store_true",
        help="Re-run document ingestion even if the database already has data.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("Starting Foundry Local RAG Assistant...")
    foundry_client = None
    try:
        foundry_client = FoundryClient()
        foundry_client.load()

        db.init_db()
        chunk_count = db.count_chunks()
        if args.reingest or chunk_count == 0:
            print(f"Ingesting documents from {config.DOCUMENTS_DIR}...")
            chunk_count = run_ingestion(foundry_client)
            print(f"Ingested {chunk_count} chunk(s).")
        else:
            print(f"Using existing knowledge base ({chunk_count} chunk(s)).")

        print("\nAssistant ready. Ask a question, or type 'exit' to quit.\n")
        while True:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() in {"exit", "quit"}:
                break

            try:
                answer = answer_query(foundry_client, question)
            except Exception as exc:
                print(f"\nSorry, something went wrong answering that: {exc}\n")
                continue

            print(f"\nAssistant: {answer}\n")

    finally:
        if foundry_client is not None:
            foundry_client.unload()
            print("Models unloaded. Goodbye.")


if __name__ == "__main__":
    main()
