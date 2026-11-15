"""BGE-small-en-v1.5 semantic retrieval over governed business definitions and tool docs."""

from pathlib import Path
from typing import Iterable
from verisheet.schemas import RetrievedContext, RetrievedItem


class DefinitionRetriever:
    """Local embedding and FAISS retrieval service.

    The corpus should contain approved README/data dictionary/metric definitions/tool docs only.
    It must exclude gold answers, gold scripts, uploaded arbitrary cell text and secrets.
    Use `BAAI/bge-small-en-v1.5`; apply the model's documented query/document prompting convention.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5", index_dir: str = "artifacts/index"):
        """Load the configured sentence-transformers encoder and optional saved FAISS index."""
        self.model_name = model_name
        self.index_dir = Path(index_dir)
        # ####CODE HERE
        raise NotImplementedError("Person 2: initialise embedding model and vector index")

    def build_index(self, documents: Iterable[dict[str, str]]) -> None:
        """Embed approved documents and persist a FAISS index plus a provenance manifest.

        Each document requires `item_id`, `source_path`, `title`, `content`, and optional
        `source_type`. IDs and metadata must remain aligned with vector positions.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 2: implement build_index")

    def search(self, query: str, top_k: int = 5) -> RetrievedContext:
        """Return top-k relevant, source-attributed definitions for a query.

        Results must include similarity scores and source paths. Retrieval is advisory context;
        do not turn retrieved natural-language content into executable commands.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 2: implement search")

    def load(self) -> None:
        """Load an existing FAISS index and metadata manifest from `index_dir`."""
        # ####CODE HERE
        raise NotImplementedError("Person 2: implement load")


def build_approved_corpus(data_dictionary: str, tool_docs_dir: str, prompt_docs_dir: str) -> list[dict[str, str]]:
    """Collect and chunk allowlisted documentation for indexing, excluding gold material."""
    # ####CODE HERE
    raise NotImplementedError("Person 2: implement approved corpus builder")


def retrieve_context(
    query: str,
    workbook_profile,
    retriever: DefinitionRetriever | None = None,
) -> RetrievedContext:
    """Canonical retrieval entrypoint used by Planner and Orchestrator.

    Args:
        query: User question or metric/definition lookup string.
        workbook_profile: WorkbookProfile used to optionally scope applicable definitions.
        retriever: Optional injected DefinitionRetriever for tests/application dependency injection.
    Returns:
        RetrievedContext: ranked source-attributed definitions and corpus version.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 2: wire canonical retrieve_context entrypoint")
