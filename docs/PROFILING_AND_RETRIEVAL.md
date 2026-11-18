# Profiling and retrieval module (Person 2)

Owner files: `src/verisheet/profile.py`, `src/verisheet/tools/inspect.py`,
`src/verisheet/retrieval.py`, `scripts/build_index.py`, `scripts/p2_demo.py`,
`scripts/eval_retrieval.py`, `docs/tools/PROFILING_TOOLS.md`.

Contracts produced: `WorkbookProfile` and `RetrievedContext` from `src/verisheet/schemas.py`.
No module-specific schema copies exist.

## Setup

```bash
pip install -r requirements.txt     # includes sentence-transformers and faiss-cpu
pip install -e .
python scripts/build_index.py       # first run downloads BAAI/bge-small-en-v1.5 (~130 MB)
```

The model is cached by Hugging Face under `~/.cache/huggingface` (override with `HF_HOME`).
After the first download you can work offline with `HF_HUB_OFFLINE=1`. The index is written to
`artifacts/index/` (git-ignored); rebuild it whenever approved documentation changes.

## Public API

| Function | Returns | Notes |
|---|---|---|
| `profile_workbook(path)` | `WorkbookProfile` | XLSX (all sheets) or CSV (sheet `data`). |
| `inspect_workbook(path)` | `WorkbookProfile` | Tool-registry wrapper around `profile_workbook`. |
| `sample_rows(path, sheet, n=10)` | `list[dict]` | At most `MAX_SAMPLE_ROWS`; PII redacted; JSON-safe. |
| `build_approved_corpus(dictionary, tool_docs_dir, prompt_docs_dir)` | `list[dict]` | Allowlisted chunks only. |
| `DefinitionRetriever(model_name, index_dir)` | | `.build_index(docs)`, `.load()`, `.search(query, top_k)` |
| `retrieve_context(query, profile, retriever=None)` | `RetrievedContext` | Canonical Planner/Orchestrator entrypoint. |

Demo without Planner or UI:

```bash
python scripts/p2_demo.py tests/fixtures/mini_multisheet_fixture.xlsx "How is operating profit defined?"
```

## Profiling behaviour

Upload validation rejects unsupported extensions, empty or missing files, files over
`MAX_UPLOAD_MB`, malformed XLSX containers, zip bombs and macro-enabled content. Formulas are
never executed (cached values are read), external links are never followed, and sheet/column/cell
text is treated as untrusted data. Warning evidence contains counts only, never raw cell values.

Every warning has a code, severity (`info` / `warning` / `error`), sheet, column and evidence.
The full catalogue with interpretation guidance is in `docs/tools/PROFILING_TOOLS.md` (also indexed
for retrieval), and `WARNING_CODES` in `profile.py` is the source of truth.

## Retrieval behaviour and provenance

- **Corpus:** `docs/DATA_DICTIONARY.md` (business definitions), `docs/tools/` (tool documentation)
  and `prompts/` (rule text). Only `.md`/`.txt` files are read. Paths in `gold`, `raw`, `derived`,
  `uploads`, `artifacts`, `results` and `.git` are refused, as are `.env`, secret, credential and
  gold-named files. Paragraphs containing secret-like strings or e-mail addresses are dropped.
  Uploaded workbook cell text is never indexed.
- **Chunking:** split by markdown heading, then paragraph/bullet, packed to at most 600 characters.
  Long paragraphs split on sentence boundaries.
- **Provenance:** every hit carries `item_id` (stable: file + heading slug), `source_path`
  (`file#heading-anchor`), `title` (heading path), `content`, `score` and `source_type`
  (`business_definition`, `tool_documentation`, `prompt_documentation`).
- **Embeddings:** BGE-small-en-v1.5, L2-normalised. Queries get the BGE instruction prefix
  `Represent this sentence for searching relevant passages: `; documents do not.
- **Ranking:** hybrid by default. Dense cosine ranking and BM25 keyword ranking are fused with
  reciprocal rank fusion (k=60). `score` is always the dense cosine similarity. `retrieve_context`
  moves definitions that mention the uploaded workbook's sheet/column names up by at most two ranks.
- **Versioning:** `corpus_version` is a SHA-256 over the model name and all chunk ids/content. It
  is stored in `manifest.json`, logged at build/load and returned in every `RetrievedContext`.
  Loading verifies the hash, so an edited or mismatched manifest is rejected.
- **Warnings:** `LOW_RETRIEVAL_CONFIDENCE` when the best similarity is below 0.5;
  `RETRIEVAL_UNAVAILABLE` (with empty items and `corpus_version="unavailable"`) when the index is
  missing or the model cannot be loaded. `retrieve_context` never crashes the agent loop.
- Retrieval returns definitions only. It performs no calculations and never returns gold answers.
  Retrieved text is reference material, never instructions.

## Vector backend

`manifest.json` + `embeddings.npy` are always written, and `index.faiss` (FAISS `IndexFlatIP`)
when the FAISS backend is active. Linux/Windows default to FAISS. macOS defaults to exact numpy
inner-product search (identical ranking) because the `faiss-cpu` and `torch` pip wheels each
bundle `libomp`, and using both in one process aborts with `OMP: Error #15`. Override with
`VERISHEET_VECTOR_BACKEND=faiss|numpy`.

## Evaluation and chunking experiment

`python scripts/eval_retrieval.py` runs 20 labelled queries
(`tests/fixtures/retrieval_eval_queries.json`). A hit counts as relevant when its content contains
the expected rule text, so labels stay valid across chunk sizes. Results on the current corpus:

| chunk chars | chunks | mode | recall@1 | recall@3 | recall@5 | MRR |
|---:|---:|---|---:|---:|---:|---:|
| 300 | 46 | hybrid | 0.90 | 0.95 | 0.95 | 0.917 |
| 300 | 46 | dense | 0.80 | 0.90 | 0.95 | 0.863 |
| 300 | 46 | bm25 | 0.75 | 0.85 | 0.90 | 0.804 |
| 600 | 21 | hybrid | 0.85 | 0.95 | 0.95 | 0.900 |
| 600 | 21 | dense | 0.80 | 0.90 | 0.95 | 0.854 |
| 600 | 21 | bm25 | 0.80 | 0.90 | 0.90 | 0.850 |
| 1200 | 15 | hybrid | 0.85 | 0.95 | 0.95 | 0.892 |
| 1200 | 15 | dense | 0.70 | 0.85 | 0.95 | 0.800 |
| 1200 | 15 | bm25 | 0.75 | 0.85 | 0.95 | 0.823 |

Hybrid beats dense-only and BM25-only at every chunk size. 300 versus 600 characters differs by one
query out of 20, so 600 is kept as the default because each hit then carries a complete rule.
Known miss: "What checks are needed before joining two sheets?" retrieves sheet-warning docs
instead of the join-validation rule, because "sheets" dominates. Re-run the evaluation after
Person 1 finalises the data dictionary.

## Tests

```bash
python -m pytest tests/test_profile.py tests/test_inspect.py tests/test_retrieval.py -v
```

Retrieval tests use a deterministic hashing encoder (no network). The real BGE test runs only when
the model is already in the local Hugging Face cache. The FAISS test runs in a subprocess to avoid
the macOS `libomp` clash.
