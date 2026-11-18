"""Build and load a local index of the demonstration manuals."""

import re
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import (
    Document,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANUAL_DIR = PROJECT_ROOT / "knowledge-manual"
INDEX_DIR = PROJECT_ROOT / "storage" / "knowledge"


def load_manual_sections() -> list[Document]:
    """Read Markdown manuals and preserve their topic boundaries."""
    documents = []

    for path in sorted(MANUAL_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")

        # Split at section headings rather than mixing unrelated topics.
        sections = re.split(r"(?m)(?=^## )", text)
        title = text.splitlines()[0].lstrip("# ").strip()

        for section in sections:
            if not section.strip():
                continue

            heading = section.splitlines()[0].lstrip("# ").strip()

            documents.append(
                Document(
                    text=section.strip(),
                    metadata={
                        "source": path.name,
                        "title": title,
                        "section": heading,
                        "status": "Fictional training material",
                    },
                )
            )

    if not documents:
        raise ValueError("No Markdown manuals found in knowledge-manual.")

    return documents


def get_index(rebuild: bool = False) -> VectorStoreIndex:
    """Load the saved index or build it from the local manuals."""
    load_dotenv(PROJECT_ROOT / ".env", override=True)

    embeddings = OpenAIEmbedding(model="text-embedding-3-small")

    if (INDEX_DIR / "docstore.json").exists() and not rebuild:
        storage = StorageContext.from_defaults(
            persist_dir=str(INDEX_DIR)
        )
        return load_index_from_storage(
            storage,
            embed_model=embeddings,
        )

    documents = load_manual_sections()

    # Keep sentences together when a section needs smaller chunks.
    splitter = SentenceSplitter(chunk_size=400, chunk_overlap=40)
    nodes = splitter.get_nodes_from_documents(documents)

    index = VectorStoreIndex(
        nodes,
        embed_model=embeddings,
        show_progress=True,
    )

    index.storage_context.persist(persist_dir=str(INDEX_DIR))

    print(f"Indexed {len(documents)} sections into {len(nodes)} chunks.")
    return index


if __name__ == "__main__":
    get_index()
    print("SUCCESS: Knowledge index is ready.")

    