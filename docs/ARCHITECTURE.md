# Architecture and boundaries

## Runtime flow

1. Streamlit receives XLSX/CSV, stores it in a quarantined temporary location and enforces file limits.
2. Profiling creates `WorkbookProfile`; retrieval returns `RetrievedContext` from approved documentation.
3. Planner receives question + profile + retrieved context + prior verified state and returns `AnalysisPlan`.
4. Executor validates the plan, dispatches allowlisted operations and writes scripts/result tables/charts into artifacts.
5. Deterministic verifier independently recomputes numbers and compares chart arrays with the result table.
6. Semantic Critic reviews intent/plan/chart. It returns ACCEPT, REPAIR, REPLAN or CLARIFY with evidence.
7. Orchestrator enforces action/retry limits, persists only verified reusable context, logs events and returns `AnswerResponse`.
8. UI renders answer/clarification/refusal, table/chart, verification status and trace details.

## Component boundary principles

- `schemas.py` is the stable cross-team API contract.
- `profile.py` owns upload inspection, not business reasoning.
- `retrieval.py` returns sourced definitions, not computed values.
- `planner.py` proposes operations, not calculations or executable code.
- `executor.py` runs only allowlisted structured operations.
- `tools/verify.py` recomputes independently and does not rely on Executor results as its source of truth.
- `critic.py` uses deterministic evidence plus separate Qwen semantic review.
- `orchestrator.py` owns state transitions and budgets.
- UI/observability consume public result/trace contracts and do not reimplement agent logic.

## Required state transitions

- ACCEPT: all required deterministic numeric/chart checks pass and semantic review is acceptable.
- REPAIR: local operation/chart/runtime defect; targeted failed step can be re-executed.
- REPLAN: incorrect metric/date/filter/join/aggregation/approach; Planner must issue a revised plan.
- CLARIFY: missing business definition, unavailable metric, ambiguous request or incompatible currency.

## Bounded execution

Maximum 10 agent/tool actions and maximum 2 repairs per request. Stop on action budget, repeated failure, clarification, or acceptance. Every transition must create a trace event.

## Model usage

Use Qwen3-8B for Planner and semantic Critic with separate versioned prompts. Use BGE-small-en-v1.5 for retrieval embeddings. Do not add another generative model to the baseline. Numerical calculation and verification are deterministic Python operations.
