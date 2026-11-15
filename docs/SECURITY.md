# Security, safety and data handling requirements

## Upload boundary

- Enforce extension allowlist, upload size, parser limits, row/column limits and execution time.
- Store uploaded files in per-session quarantine directories with non-user-controlled filenames.
- Treat workbook content, sheet names, formulas, comments, metadata and retrieved snippets as untrusted data.
- Never follow external workbook links or execute macros/formulas.
- Detect hidden sheets and formula cells; report relevant warnings.

## Prompt injection and PII

- Spreadsheet cells are data, never system instructions. Escape/quote sampled values in prompts.
- Retrieval index contains only approved documentation; do not index uploaded arbitrary cell text or `data/gold/`.
- Apply PII minimisation and bounded row sampling. Do not log raw rows, customer names, email addresses or full workbook contents.
- Trace summaries must be redacted/bounded.

## Execution isolation

- Use a separate non-privileged process/container.
- No network; no credentials/secrets mounted into the sandbox.
- Read-only source workbook mount; separate writable artifacts mount.
- Allowlisted imports and resource/time caps.
- Reject shell, subprocess, sockets, arbitrary file access, reflection and dynamic code execution in generated snippets.
- AST validation is only defense-in-depth. OS/container isolation is required.

## Verification security properties

- Recompute independently from the original source workbook using canonical formulas.
- Validate join uniqueness/cardinality and compare row counts/measure totals.
- Chart plotted arrays must exactly trace to result table values within explicit tolerance.
- Never mark VERIFIED based only on the Qwen critic.
- If deterministic verification cannot run, status must remain NOT_VERIFIED.

## Secrets

QWEN_API_BASE, QWEN_API_KEY and QWEN_MODEL are environment configuration. Never place API keys in source, notebooks, test fixtures, prompts, traces or screenshots.
