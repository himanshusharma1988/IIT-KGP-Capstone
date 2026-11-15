# Six-person assignment sheet

This is the quick assignment page. The detailed implementation tickets and acceptance criteria are in `/TASK_ASSIGNMENTS.md`.

| Owner | Primary outcome | Files owned | Must hand over |
|---|---|---|---|
| Person 1 — Data/domain/evaluation | Reproducible public/synthetic/corrupt workbooks, business definitions, 100 frozen question tasks and gold answers | `scripts/`, `data/`, `config/tasks.yaml`, data docs | Manifest, hashes, clean + 20 corrupt files, 20 dev + 80 test JSONL, gold generation code and hidden master key |
| Person 2 — Profiling/RAG | Reusable workbook profile + BGE semantic retrieval | `src/verisheet/profile.py`, `retrieval.py`, `tools/inspect.py` | `WorkbookProfile`, `RetrievedContext`, profiling/RAG tests, index build instructions |
| Person 3 — Planner | Qwen3-8B planner producing valid `AnalysisPlan` and clarification decisions | `planner.py`, `qwen_client.py` (shared wrapper), `prompts/planner.txt` | Prompt version, structured plan examples, tests for metric/period/joins/refusals/follow-up |
| Person 4 — Executor | Approved operations, isolated execution, result tables and chart artifacts | `executor.py`, `sandbox.py`, `tools/analysis.py`, `tools/chart.py` | `ExecutionResult`, scripts + hashes, tables, chart images + plotted arrays, sandbox evidence |
| Person 5 — Critic/orchestrator | Independent verification and bounded state machine | `schemas.py` (shared contract owner), `critic.py`, `orchestrator.py`, `state.py`, `tools/verify.py` | `VerificationReport`, `CriticDecision`, `AnswerResponse`, repair/replan/clarify tests |
| Person 6 — UI/observability/evaluation/deployment | End-user application, trace dashboard, five experiment variants, score report and deployment | `app.py`, `observability/`, `experiments/`, root `experiments/`, Docker/deployment docs | Working upload/chat UI, real traces, five-variant score, 20 robustness cases, report/demo |