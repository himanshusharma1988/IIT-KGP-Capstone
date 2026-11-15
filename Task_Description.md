

## task map

| task | Owner | Outcome | Depends on |
|---|---|---|---|
| VS-P1 — Data, domain rules and evaluation | Person 1 | Frozen, reproducible datasets and gold benchmark | None |
| VS-P2 — Workbook profiling and retrieval | Person 2 | WorkbookProfile and RetrievedContext services | P1 for full acceptance; fixtures unblock development |
| VS-P3 — Planner and prompt engineering | Person 3 | Schema-valid plans from Qwen3-8B | P1/P2 contracts; mock fixtures unblock development |
| VS-P4 — Executor and analytical tools | Person 4 | Safe computations, result tables and charts | P1 data and P3 plan contract; fixtures unblock development |
| VS-P5 — Critic, verification and orchestration | Person 5 | Genuine bounded agent loop and independent verification | P2/P3/P4 contracts; mock fixtures unblock development |
| VS-P6 — UI, observability and evaluation runner | Person 6 | Usable app, trace dashboard and five-variant experiments | AnswerResponse/TraceEvent contracts; mock fixtures unblock development |

## Global Definition of Ready

A task is ready when its owner, public interface, input/output schema, dependencies, fixture and acceptance criteria are known. If an upstream module is incomplete, use the relevant fixture in `contracts/examples/` and a local mock.

## Global Definition of Done

- Code is merged through a reviewed pull request to the assigned module path.
- Public classes/functions have type hints and docstrings that explain purpose, parameters, return type, errors and schema.
- No unexplained `####CODE HERE` remains in the task's scope.
- Unit tests cover normal, boundary and failure paths; contract tests use shared fixtures.
- No secrets, gold answers/scripts, raw PII or unrestricted workbook content are exposed in prompts, logs or retrieval.
- Module instructions allow another contributor to install, run and test it without author assistance.
- Interface changes are approved by affected module owners.

---

# VS-P1 — Data, domain rules and evaluation (Person 1)

## VS-P1-01 — Acquire and manifest the public datasets
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** None

**task:** As the data owner, I need the original Sample Superstore and UCI Online Retail datasets acquired and fingerprinted so all teams and evaluation runs use known, reproducible inputs.

**Technical tasks**
- Acquire the full Sample Superstore workbook/table with the required fields, including order/customer/product identifiers where available.
- Download the original UCI Online Retail.xlsx from the UCI dataset page.
- Preserve original source files immutably under `data/raw/`; write standardised copies only to `data/derived/`.
- Create `data_manifest.json` with exact source URL, retrieval date, licence notice, filename, SHA-256, byte size, detected sheets/row count and verified field names.
- Verify field names/types on the actual downloaded version; do not hard-code a presumed file name/date format.

**Acceptance criteria**
- [ ] Both public sources are present and readable by openpyxl/Pandas.
- [ ] Manifest has source, retrieval date, licence notice, SHA-256 and verified row count for every source.
- [ ] Raw copies are not modified during standardisation.
- [ ] Data caveat is recorded: Online Retail has no Profit/COGS; Superstore Profit is recorded profit, not full accounting P&L.

**Outputs:** `data/raw/`, `data/derived/`, `data_manifest.json`, `docs/DATA_DICTIONARY.md` updates.

## VS-P1-02 — Generate FinanceOps synthetic multi-sheet workbook
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P1-01

**task:** As the evaluation owner, I need a reproducible finance workbook to test multi-sheet joins, effective-dated costs, returns, expenses and business definitions that are not present in public sources.

**Technical tasks**
- Build `FinanceOps_Synthetic.xlsx` from a fixed seed (default 42).
- Generate sheets and exact columns described in `docs/DATA_DICTIONARY.md`: Orders, Product_Costs, Expenses, Returns, Budget, Definitions, plus README.
- Include at least four completed quarters and a partial fifth quarter.
- Apply effective-dated product costs using latest applicable date.
- Aggregate Returns by Order_ID before joining; document return-cost treatment.
- Define operating profit as net sales − COGS − operating expenses; define net sales as gross sales − refunds.
- Record currency, unit conventions, fiscal-year start and Data_Through/reporting close.

**Acceptance criteria**
- [ ] Re-running with the same seed produces identical logical data and stable output checksums.
- [ ] Sales = Qty × Unit_Price.
- [ ] Every cost join uses the latest applicable Effective_From date.
- [ ] Returns do not multiply order-line rows.
- [ ] README sheet documents all business rules and simplifications.
- [ ] At least four complete quarters plus a partial fifth quarter exist.

**Outputs:** `scripts/prepare_data.py`, `data/derived/FinanceOps_Synthetic.xlsx`, generator metadata.

## VS-P1-03 — Create 20 controlled corruption variants
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P1-02

**task:** As the robustness-test owner, I need controlled workbook faults with expected outcomes so error detection and repair can be evaluated reproducibly.

**Technical tasks**
- Produce `corrupt_01.xlsx` … `corrupt_20.xlsx` from a clean baseline.
- Include distinct documented perturbation types (e.g. renamed metric, missing cost sheet, duplicated join keys, date shift, nulls, duplicate rows, incorrect data type, altered chart expectation, currency ambiguity).
- Create a master key mapping workbook fingerprint → injected fault → expected detection/transition → expected correct/refusal outcome.
- Keep the master key outside model context and retrieval.

**Acceptance criteria**
- [ ] Exactly 20 corruption workbooks exist.
- [ ] Each has one primary labelled fault and deterministic expected outcome.
- [ ] Clean baseline and each corrupt workbook have hashes in master key.
- [ ] Corruption scripts regenerate the cases from the same clean base.

**Outputs:** `data/derived/clean.xlsx`, `corrupt_01.xlsx` … `corrupt_20.xlsx`, `data/gold/corruption_master_key.json`.

## VS-P1-04 — Freeze 100 question-workbook tasks and gold answers
**Priority:** P0 · **Estimate:** 8 SP · **Dependencies:** P1-01, P1-02, P1-03

**task:** As the benchmark owner, I need a frozen, stratified task bank and independently generated gold answers so system variants are compared fairly.

**Technical tasks**
- Build exactly 100 unique question-workbook pairs: 40 Superstore, 40 Online Retail, 20 synthetic/corrupted.
- Build five families with 20 tasks each: aggregation/ranking, time/growth, joins/grouping, multi-step explanation, ambiguity/corruption/refusal.
- Allocate exactly 20 stratified dev tasks and 80 held-out test tasks.
- Freeze IDs, source workbook hashes, gold values/tables, accepted chart types, refusal expectations and acceptance checks before agent development/evaluation.
- Generate gold answers using independent reference scripts, not Planner/Executor implementations.
- Keep `data/gold/` out of prompts, retrieval and application context.

**Acceptance criteria**
- [ ] Exactly 100 tasks; split is exactly 20 dev / 80 test.
- [ ] Dataset allocation and question-family counts match the project brief.
- [ ] Every task has a unique ID, workbook hash, question, expected intent/metric, output checks and refusal flag.
- [ ] Gold values are computed from the downloaded, hashed dataset version, not invented.
- [ ] Gold files cannot be reached by application retrieval or model prompts.

**Outputs:** `data/questions_dev.jsonl`, `data/questions_test.jsonl`, `scripts/generate_gold.py`, `data/gold/`.

---

# VS-P2 — Workbook profiling and RAG (Person 2)

## VS-P2-01 — Implement safe XLSX/CSV ingestion and workbook profiling
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P1 fixtures available; full P1 data later

**task:** As the Planner, I need a canonical WorkbookProfile for an unfamiliar upload so I can select valid sheets, columns, dates and operations.

**Technical tasks**
- Implement `profile_workbook(file_path) -> WorkbookProfile` in `src/verisheet/profile.py`.
- Support CSV and multi-sheet XLSX; preserve sheet names.
- Fingerprint source bytes with SHA-256.
- Return row counts, column names/dtypes, null counts, unique counts, duplicate row counts, candidate date ranges, hidden-sheet and formula metadata.
- Validate extension, size, malformed files and parser limits.
- Emit Pydantic `WorkbookProfile` using `schemas.py` only.

**Acceptance criteria**
- [ ] Profiles multi-sheet XLSX and CSV.
- [ ] Identifies schema and candidate dates without assuming specific business column names.
- [ ] Detects hidden sheets/formula cells in XLSX and adds quality warnings.
- [ ] Handles empty sheets, malformed files and invalid date values explicitly.
- [ ] Output validates as `WorkbookProfile` and matches the fixture contract.

**Outputs:** `profile.py`, `tools/inspect.py`, `tests/test_profile.py`.

## VS-P2-02 — Implement safe sample_rows and quality warnings
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P2-01

**task:** As the Planner/Executor, I need bounded typed samples and quality warnings so I can understand schema ambiguity without sending excessive or unsafe workbook data to the LLM.

**Technical tasks**
- Implement `sample_rows(file_path, sheet_name, n)`.
- Enforce configured maximum sample rows.
- Convert dates/numbers to JSON-safe types.
- Minimise/redact PII and neutralise formula-like strings.
- Warn on missing columns, all-null columns, duplicate rows, date parse failures and formula presence.

**Acceptance criteria**
- [ ] Requests above configured sample cap are rejected or capped consistently.
- [ ] Unknown sheet raises a structured safe error.
- [ ] Cell strings are represented as data and never executed/injected as prompt instruction.
- [ ] No unbounded/raw dataset is included in a tool response.

**Outputs:** `tools/inspect.py`, quality warning fixtures and tests.

## VS-P2-03 — Build BGE-small-en-v1.5 document embeddings and FAISS index
**Priority:** P1 · **Estimate:** 5 SP · **Dependencies:** P1 data dictionary; P2-01 may proceed with mock docs

**task:** As the Planner, I need semantic retrieval over approved definitions and tool documentation so the selected metric/assumptions are grounded in source material.

**Technical tasks**
- Load `BAAI/bge-small-en-v1.5` using sentence-transformers.
- Chunk approved data dictionary, workbook README, metric definitions and tool documentation.
- Store stable chunk IDs, source paths, titles, corpus version and embedding positions.
- Build/save/load FAISS CPU index and metadata manifest.
- Implement top-k search returning `RetrievedContext` with score and source provenance.
- Exclude gold directory, uploaded arbitrary cell content, secrets and PII.

**Acceptance criteria**
- [ ] Index can be built and reloaded after process restart.
- [ ] Relevant metric/business-rule document appears in top-k for representative queries.
- [ ] Each hit returns source path/title/item ID and score.
- [ ] Corpus manifest/version is logged.
- [ ] Retrieval does not perform numeric calculations or return gold answers.

**Outputs:** `retrieval.py`, `index_builder.py` (if split), index artefacts, retrieval tests.

## VS-P2-04 — Publish profiling/retrieval contract and integration demo
**Priority:** P0 · **Estimate:** 2 SP · **Dependencies:** P2-01, P2-02, P2-03

**task:** As the Planner owner, I need a reproducible module handover matching shared contracts so it can be integrated without custom adapters.

**Technical tasks**
- Validate output against WorkbookProfile/RetrievedContext models.
- Add mock and real test cases; document setup/model download/cache behavior.
- Add provenance and warning behavior to README.
- Demonstrate `profile_workbook` and `retrieve_context` without Planner or UI.

**Acceptance criteria**
- [ ] Another person can run the module from README instructions.
- [ ] Contract fixtures validate without field renaming.
- [ ] No module-specific schema duplicates exist.
- [ ] All P2-owned `####CODE HERE` markers are resolved.

---

# VS-P3 — Prompt engineering and Planner (Person 3)

## VS-P3-01 — Validate Qwen3-8B endpoint and shared client
**Priority:** P0 · **Estimate:** 2 SP · **Dependencies:** Qwen endpoint credentials; shared schema available

**task:** As the Planner/Critic, I need a tested OpenAI-compatible Qwen API client so both agent roles use the same model/version and observable usage metadata.

**Technical tasks**
- Validate endpoint compatibility with chat completions.
- Use environment variables `QWEN_API_BASE`, `QWEN_API_KEY`, `QWEN_MODEL`.
- Use timeout, bounded token configuration and error translation.
- Return LLMResponse with content, model, input/output token counts and latency.
- Ensure API key is never logged or inserted into prompts.

**Acceptance criteria**
- [ ] A smoke-test chat completion succeeds against configured endpoint.
- [ ] Missing credentials fail with a useful configuration error.
- [ ] Response captures token usage when provider returns it.
- [ ] No credential appears in logs or trace payload.

**Outputs:** `qwen_client.py`, `.env.example` validation/documentation.

## VS-P3-02 — Design Planner system prompt and strict JSON output
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P2 contracts/fixtures; Qwen client

**task:** As a user, I need natural-language analytical questions converted into a valid plan so the analysis is explicit, reviewable and executable.

**Technical tasks**
- Finalise versioned `prompts/planner.txt`.
- Build prompt composer with question, WorkbookProfile, RetrievedContext, previous verified AgentState and action budget.
- Request JSON only; parse and validate against `AnalysisPlan`.
- Include goal, metric, source sheets, filters, time policy, joins/cardinality, ordered steps/dependencies, expected outputs, checks, chart spec and assumptions.
- Reject unknown columns/invalid schemas and malformed JSON.

**Acceptance criteria**
- [ ] Valid AnalysisPlan returned for representative aggregation/time/group/join/chart questions.
- [ ] Planner does not output calculated numeric answers or arbitrary Python.
- [ ] Planner identifies the correct source metric and aggregation.
- [ ] The plan is dependency ordered and names validation checks.
- [ ] All outputs pass Pydantic validation.

**Outputs:** `planner.py`, `prompts/planner.txt`, JSON parsing tests.

## VS-P3-03 — Implement answerability, date and metric policies
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P3-02, P2-01/03

**task:** As a user, I need the Planner to recognise when requested data/definitions are absent so it asks for clarification rather than fabricating an answer.

**Technical tasks**
- Detect unavailable metrics, especially Online Retail profit/COGS.
- Apply documented margin and completed-quarter conventions.
- Require explicit currency conversion information before combining currencies.
- Ask clarification for ambiguous dual-criterion requests or missing definitions.
- Add plan assumptions and sources.

**Acceptance criteria**
- [ ] Online Retail “profit” produces CLARIFY/unanswerable, not sales substitution.
- [ ] Last-completed-quarter policy uses Data_Through when available; otherwise uses documented observed-date assumption.
- [ ] Margin uses sum(Profit)/sum(Sales).
- [ ] Conflicting currency context produces clarification.
- [ ] Ambiguous query has a specific clarification question.

**Outputs:** Planner policy tests and prompt failure analysis.

## VS-P3-04 — Support follow-up context and targeted REPLAN
**Priority:** P1 · **Estimate:** 3 SP · **Dependencies:** P3-02, P5 AgentState contract

**task:** As a user, I need follow-up questions to preserve the prior verified metric, period and filters without re-uploading/re-specifying them.

**Technical tasks**
- Accept AgentState and use only accepted/verified context.
- Interpret “it”, “same quarter”, “break it down by region” and similar follow-ups.
- Implement `revise_plan` that responds to critic feedback and preserves validated intermediates where valid.
- Keep plan IDs/version and trace feedback.

**Acceptance criteria**
- [ ] Regional follow-up retains previously accepted quarter.
- [ ] Unverified prior result is not reused as a fact.
- [ ] REPLAN updates invalid steps without unnecessarily discarding valid context.
- [ ] Tests cover no prior state, matching workbook state and workbook fingerprint change.

---

# VS-P4 — Executor, tools and sandbox (Person 4)

## VS-P4-01 — Implement plan validation and allowlisted tool registry
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P3 AnalysisPlan contract, P2 profile fixture

**task:** As the system, I need every Planner step validated against known sheets/columns and approved tools before execution so model output cannot invoke arbitrary functionality.

**Technical tasks**
- Build registry for inspect_workbook, sample_rows, run_analysis and make_chart.
- Validate referenced sheet/column names against WorkbookProfile.
- Validate operation name, input schema, dependencies and action budget.
- Detect unknown tools, dependency cycles and missing prerequisites.

**Acceptance criteria**
- [ ] Unsupported operations are rejected before execution.
- [ ] Missing sheet/column is returned as structured ToolError.
- [ ] Dependency cycles are detected.
- [ ] Registry is closed/allowlisted; no dynamic import or model-selected Python callable.

## VS-P4-02 — Implement deterministic Pandas/DuckDB operations
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P4-01, P1 datasets

**task:** As the user, I need common analytical operations to produce correct structured results from my workbook.

**Technical tasks**
- Implement group aggregation, filter, top-N ranking, time aggregation, quarter comparison, grouped ratio and safe multi-sheet join.
- Validate aggregations and supported operators.
- Handle missing/null/empty groups and zero denominators.
- Apply completed-quarter, return/cancellation and currency rules.
- Check join cardinality, row counts and numeric totals.

**Acceptance criteria**
- [ ] Operations cover the frozen task bank's required analytical patterns.
- [ ] Wrong/many-to-many join does not silently inflate numeric results.
- [ ] Quarterly calculations disclose the observed-date assumption when used.
- [ ] Margin is ratio of sums.
- [ ] Zero/negative growth baseline convention is explicit.

**Outputs:** `tools/analysis.py`, deterministic unit tests.

## VS-P4-03 — Generate and execute chart artifacts from result tables
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P4-02

**task:** As the user, I need a chart that faithfully represents executed results so I can inspect the analytical result visually.

**Technical tasks**
- Implement ChartSpec validation and Matplotlib/Plotly rendering.
- Support bar, horizontal bar, line and scatter baseline chart types.
- Save image/HTML and machine-readable x/y arrays.
- Label title, reporting interval, units/currency, filters and aggregation where available.
- Enforce chronological ordering and ranking order; avoid misleading axis truncation.

**Acceptance criteria**
- [ ] Chart is derived from result table, not model-authored data.
- [ ] Plotted array is included in ExecutionResult.
- [ ] Chart title/axes/unit match ChartSpec.
- [ ] Wrong chart type/column is rejected or surfaced for Critic.
- [ ] Artifact path and hash are returned.

## VS-P4-04 — Implement restricted execution sandbox
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P4-01; platform/container availability

**task:** As the platform owner, I need generated scripts/approved operations executed in isolation so an uploaded workbook or model response cannot access host resources or secrets.

**Technical tasks**
- Run in separate unprivileged process/container.
- No network; no credentials; read-only input mount; writable isolated artifacts mount.
- Import allowlist and resource/time/memory limits.
- AST defense-in-depth against open/subprocess/socket/shell/reflection/dynamic execution.
- Capture exit code, bounded stdout/stderr, timeout, duration and failure category.

**Acceptance criteria**
- [ ] Sandbox cannot access network or environment secrets.
- [ ] Timeout/memory limits enforced by OS/container mechanism.
- [ ] Read-only inputs remain unchanged.
- [ ] Forbidden import/call tests rejected.
- [ ] Documentation explicitly states AST checks alone are not a security boundary.

## VS-P4-05 — Publish ExecutionResult and executor handover
**Priority:** P0 · **Estimate:** 2 SP · **Dependencies:** P4-01 through P4-04

**task:** As Person 5, I need a stable structured execution response with artifacts and provenance so I can verify and repair it without depending on Executor internals.

**Acceptance criteria**
- [ ] Every step returns ExecutionResult validated by shared schema.
- [ ] Failed operation includes ToolError code/category/retryability/step ID.
- [ ] Result table path, script path/hash, row counts, chart path/arrays and duration included where applicable.
- [ ] Another person can call executor with fixture AnalysisPlan without UI or Planner running.

---

# VS-P5 — Critic, independent verification, orchestration and state (Person 5)

## VS-P5-01 — Implement canonical independent numerical verifier
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P1 gold/business rules, P4 ExecutionResult contract

**task:** As the user, I need numeric outputs independently checked against source workbook data so an LLM or Executor mistake is not presented as verified.

**Technical tasks**
- Implement canonical reference calculations separately from Executor operation functions.
- Recompute from original workbook and approved metric/period/filter definitions.
- Check row/join grain, units, currency, numerator/denominator, date range and tolerances.
- Emit VerificationReport with evidence and discrepancy category.

**Acceptance criteria**
- [ ] Wrong SUM/MEAN is detected.
- [ ] Wrong quarter/date filter is detected.
- [ ] Join multiplication is detected.
- [ ] Missing/unavailable source metric returns not verified/clarify.
- [ ] If recomputation cannot be performed, `verified=false`.
- [ ] Qwen response is never accepted as numeric proof.

## VS-P5-02 — Implement chart-data fidelity verification
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P4 chart contract

**task:** As the user, I need the rendered chart to contain the same data as the verified table so the visual cannot contradict the numeric answer.

**Technical tasks**
- Read result table and Executor plotted arrays.
- Compare categories, sort/order, values and numeric tolerance.
- Validate x/y field mapping, unit/currency, time labels and chart category appropriateness.
- Emit chart findings into VerificationReport.

**Acceptance criteria**
- [ ] Deliberately altered plotted value fails verification.
- [ ] Missing/extra category fails verification.
- [ ] A top-five ranking plotted as an inappropriate line chart is flagged for semantic review.
- [ ] Chart verification is deterministic where possible.

## VS-P5-03 — Implement Qwen semantic Critic and decision policy
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** P3/P4 contracts, P5-01/02

**task:** As the system owner, I need a separate Critic role to assess intent/plan/chart fit and recommend a precise transition without being trusted for numeric correctness.

**Technical tasks**
- Create versioned `prompts/critic.txt` using shared Qwen client.
- Review metric, period, filters, join grain, chart appropriateness and answer-intent match.
- Combine semantic output with deterministic VerificationReport.
- Return ACCEPT, REPAIR, REPLAN or CLARIFY with failed step, error category, evidence and corrective instruction.

**Acceptance criteria**
- [ ] ACCEPT only when required deterministic checks and semantic requirements pass.
- [ ] Local code/chart issue routes to REPAIR.
- [ ] Wrong approach/period/metric routes to REPLAN.
- [ ] Missing inputs/definition routes to CLARIFY.
- [ ] Inability to independently verify never produces ACCEPT.

## VS-P5-04 — Implement bounded Orchestrator and state persistence
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P2/P3/P4/P5-03 interfaces

**task:** As a user, I need the agent roles coordinated over multiple turns while retaining only verified context and preventing endless retries.

**Technical tasks**
- Implement run flow: profile → retrieve → plan → execute → verify → critic → transition.
- Enforce at most 10 actions and 2 repairs per request.
- REPAIR only failed step and dependent artifacts; REPLAN asks Planner for replacement steps; CLARIFY returns a user question.
- Persist state by session ID/workbook fingerprint.
- Update accepted metric/period/filters only after verified response.
- Reset or isolate context when workbook fingerprint changes.

**Acceptance criteria**
- [ ] Full Planner→Executor→Critic loop observable.
- [ ] REPAIR, REPLAN and CLARIFY tested end-to-end.
- [ ] Follow-up retains verified quarter/filter context.
- [ ] Unverified response does not update accepted facts.
- [ ] Action and repair caps cannot be exceeded.

## VS-P5-05 — Publish AnswerResponse and trace events for UI
**Priority:** P0 · **Estimate:** 2 SP · **Dependencies:** P5-04 and P6 TraceEvent contract

**task:** As Person 6, I need one stable final response independent of transition path so the UI does not need to know internal agent details.

**Acceptance criteria**
- [ ] Every terminal path returns AnswerResponse.
- [ ] VERIFIED status has passing VerificationReport (also schema-enforced).
- [ ] Clarification response supplies clarification_question.
- [ ] Failure/not-verified response does not claim success.
- [ ] Trace ID joins all events/artifacts for the user request.

---

# VS-P6 — UI, observability, experiments and deployment (Person 6)

## VS-P6-01 — Implement workbook upload and analytical chat UI
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P2 WorkbookProfile and P5 AnswerResponse contracts; mock response can unblock

**task:** As an analyst, I need a simple interface to upload workbooks, ask multi-turn questions and inspect verified results so I can use the agent without writing code.

**Technical tasks**
- Implement Streamlit upload for XLSX/CSV and safe temporary storage.
- Display workbook sheet/column profile and quality warnings.
- Retain session/workbook reference across chat turns.
- Call orchestrator and render AnswerResponse, table, chart, assumptions, clarification/refusal and verification badge/status.
- Do not calculate analytics in Streamlit.

**Acceptance criteria**
- [ ] Upload accepts supported formats and shows profile.
- [ ] User can ask follow-up without re-uploading.
- [ ] UI distinguishes VERIFIED, NOT_VERIFIED, CLARIFICATION_REQUIRED and FAILED.
- [ ] Table/chart rendered only from backend artifacts.
- [ ] Errors are understandable and trace ID is visible.

## VS-P6-02 — Implement structured trace logging and dashboard
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P5 trace emission fields; mock JSONL unblocks UI

**task:** As the evaluator, I need real execution traces to understand agent decisions, reproduce failures and demonstrate self-repair.

**Technical tasks**
- Persist TraceEvent records as JSONL or another append-only format.
- Capture query/workbook fingerprint, plan JSON, step/tool events, script and artifact hashes, verification findings, Critic decision, model/prompt versions, tokens, latency and failure category.
- Build Streamlit trace viewer with event timeline and artifact links.
- Redact PII and bound summaries.

**Acceptance criteria**
- [ ] A trace can be loaded by trace ID and shown in timestamp order.
- [ ] Actual model/tool calls and decision transitions are visible.
- [ ] Token counts/latency/model/prompt versions appear when available.
- [ ] Failure category and verification evidence appear.
- [ ] No raw PII/API secrets are logged.

## VS-P6-03 — Implement five-variant experiment runner
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P1 frozen test set, P5 orchestrator and P4 tool contracts

**task:** As the evaluator, I need five controlled system variants run against the same frozen 80-question test set so I can compare the contribution of planning, critic and deterministic checks.

**Technical tasks**
- Implement E1 Direct, E2 Planner+Executor, E3 LLM Critic, E4 deterministic Critic, E5 Full hybrid.
- Keep model/version, workbook, question, temperature, tool library and test set consistent.
- Record prompt versions and run metadata.
- Limit actions/retries consistently.
- Provide CLI entrypoint `experiments/run.py --system ... --split ...`.

**Acceptance criteria**
- [ ] All five variants run on same held-out 80 questions.
- [ ] Variant configuration is recorded per trace.
- [ ] One run at course minimum; repeated runs can be added for stability.
- [ ] Model/prompt versions and token/latency are logged.

## VS-P6-04 — Implement scoring, ablation and 20-case injection suite
**Priority:** P0 · **Estimate:** 5 SP · **Dependencies:** P1 gold data and corruption key, P6-03 traces

**task:** As the evaluator, I need reproducible metrics and robustness cases so correctness, false verification and repair capability can be measured rather than demonstrated anecdotally.

**Technical tasks**
- Score numeric accuracy, task success, execution success, plot data accuracy, chart appropriateness, error detection recall, false verification rate + verified coverage, repair success, tool efficiency, median/p95 latency and token usage.
- Implement variant comparison/ablation script.
- Run at least 20 fault-injection cases, including wrong aggregation, wrong period, duplicated join, missing metric/sheet, invalid chart arrays and prompt injection.
- Save machine-readable summary and reproducibility metadata.

**Acceptance criteria**
- [ ] All requested metric definitions are present and documented.
- [ ] At least 20 robustness/error-injection cases are reported.
- [ ] False verification rate and verified coverage are both reported.
- [ ] Results identify test-set hash and model/prompt version.
- [ ] No fabricated or hand-entered experiment results.

## VS-P6-05 — Package deployment, report and final demo
**Priority:** P0 · **Estimate:** 3 SP · **Dependencies:** all prior tasks integrated

**task:** As the evaluator, I need a reproducible install/deployment and clear demonstration so the finished system can be reviewed from a clean environment.

**Technical tasks**
- Finalise `requirements.txt`, Dockerfile, `.env.example`, README and startup commands.
- Run unit, integration, security and acceptance tests in a clean environment.
- Produce 12-page technical report with architecture, prompt strategy, RAG, agent decisions, evaluation, failure taxonomy, security and limitations.
- Rehearse 10-minute demo in `docs/DEMO_RUNBOOK.md`.

**Acceptance criteria**
- [ ] Clean install instructions work on the target environment.
- [ ] No credentials embedded in image/source/repository.
- [ ] Original Superstore and Online Retail scenarios demonstrated.
- [ ] Follow-up context retained.
- [ ] One deliberate fault and Critic transition demonstrated.
- [ ] Trace dashboard shows actual execution, scripts, verification, tokens and latency.
- [ ] 12-page report and 10-minute demo deliverables are complete.

---

# Final Integration cross-task checkpoints

| Gate | Required evidence | Outcomes |
|---|---|---|
| G0 Contract freeze | Shared Pydantic schemas, fixtures and owner matrix | Allow parallel implementation |
| G1 Module completion | Each module's unit/contract tests, README and independent demo | Accept each person's module |
| G2 Data/profile integration | Real datasets profile and retrieval returns source-grounded context | Unlock full agent integration |
| G3 Agent loop integration | Real Planner/Executor/Critic with repair/replan/clarify | Unlock UI end-to-end |
| G4 Security and evaluation | Sandbox/security tests, frozen 80-question run, 20 injection cases | Accept research results |
| G5 Final delivery | Clean install, 12-page report, trace dashboard and demo | Project sign-off |
