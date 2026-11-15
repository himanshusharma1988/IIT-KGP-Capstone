"""Person 2 retrieval tests; use a tiny local corpus and avoid network-dependent tests in CI."""
import pytest

@pytest.mark.skip(reason="Person 2: implement deterministic tiny-corpus retrieval and enable")
def test_retriever_returns_relevant_source_with_provenance():
    """Implementation test for retriever returns relevant source with provenance; enable after its owning  task is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 2: implement save/load index and enable")
def test_retriever_persists_and_reloads_index():
    """Implementation test for retriever persists and reloads index; enable after its owning  task is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 2: ensure gold directory excluded from corpus and enable")
def test_approved_corpus_excludes_gold_and_secrets():
    """Implementation test for approved corpus excludes gold and secrets; enable after its owning  task is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 2: implement query/document embedding convention and enable")
def test_bge_query_returns_expected_definition_top_k():
    """Implementation test for bge query returns expected definition top k; enable after its owning  task is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 2: validate unknown corpus state and enable")
def test_retriever_returns_clear_error_when_index_missing():
    """Implementation test for retriever returns clear error when index missing; enable after its owning  task is implemented."""
    # ####CODE HERE
    raise NotImplementedError
