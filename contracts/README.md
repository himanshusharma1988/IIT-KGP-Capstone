# Shared contracts

`src/verisheet/schemas.py` is the sole source of truth for the Pydantic contracts. Use `scripts/export_schemas.py` to emit JSON Schema for non-Python consumers.

## Contract ownership

- P2 produces: `WorkbookProfile`, `RetrievedContext`.
- P3 produces: `AnalysisPlan`.
- P4 produces: `ExecutionResult`.
- P5 produces: `VerificationReport`, `CriticDecision`, `AgentState`, `AnswerResponse`.
- P6 produces: `TraceEvent` and experiment result records.
- P1 produces dataset manifest/gold-task contracts documented in `docs/DATA_DICTIONARY.md`.

## Compatibility rules

- Required field additions or renames are breaking changes and require joint review.
- Prefer optional additive fields with defaults where possible.
- Reject extra/unknown fields in public payloads (`extra="forbid"`).
- Never put raw workbook content, secrets or gold answers into prompts or trace summaries.
- Use source references for retrieved definitions and artifact paths/hashes for large outputs.

## Canonical payload examples

See `contracts/examples/`. They are synthetic interface fixtures, not real dataset values.
