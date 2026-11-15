# Integration contracts — read before implementation

## Contract flow

| Producer | Contract | Consumer |
|---|---|---|
| P2 | `WorkbookProfile` | P3, P5, P6 |
| P2 | `RetrievedContext` | P3 |
| P3 | `AnalysisPlan` | P4, P5 |
| P4 | `ExecutionResult` | P5, P6 |
| P5 | `VerificationReport`, `CriticDecision`, `AgentState`, `AnswerResponse` | P3/P4 via loop, P6 |
| P6 | `TraceEvent` | P5 emits it; P6 persists/displays it |

## Canonical function signatures

```python
profile_workbook(file_path: str | Path) -> WorkbookProfile
retrieve_context(query: str, workbook_profile: WorkbookProfile) -> RetrievedContext
generate_plan(question: str, workbook_profile: WorkbookProfile,
               retrieved_context: RetrievedContext,
               previous_state: AgentState | None = None,
               feedback: dict | None = None) -> AnalysisPlan
execute_plan(plan: AnalysisPlan, workbook_path: str, run_id: str) -> list[ExecutionResult]
verify_result(workbook_path: str, plan: AnalysisPlan,
              execution_result: ExecutionResult,
              tolerance: float = 1e-9) -> VerificationReport
run_agent(question: str, workbook_reference: str, session_id: str) -> AnswerResponse
```

Some class methods in the starter are more detailed than this minimum function layer. Keep public signatures compatible or submit a shared-schema change proposal.

## Payload rules

- All public payloads are Pydantic models in `src/verisheet/schemas.py`.
- Use `model_dump(mode="json")` for JSON-safe serialisation and `model_validate()` on input.
- `WorkbookProfile.workbook_id` is the SHA-256 fingerprint of source bytes.
- `AnalysisPlan` contains only structured operations. It must not contain Python source or claimed results.
- `ExecutionResult` points to artifacts and includes hashes/dimensions/plot arrays; do not embed large tables in JSON.
- `VerificationReport.verified` is true only if all required deterministic checks pass.
- `AnswerResponse.status == VERIFIED` is schema-guarded and requires a passing VerificationReport.
- A clarification response includes `clarification_question` and does not pretend execution succeeded.
- A failure response must not display unverified numeric claims as verified.

## Error contract

Use `ToolError` with stable `code`, `category`, `message`, `retryable`, optional `failed_step_id`, and bounded `safe_details`. Do not return raw exception tracebacks to the user. Save full safe diagnostics in trace artifacts.

## Example fixtures

Use JSON payloads in `contracts/examples/`. Validate them before consuming. These values are synthetic interface examples, not benchmark gold answers.

## Compatibility process

1. Raise an issue describing the proposed field/signature change and reason.
2. Identify producer and all consumers.
3. Update Pydantic class, example JSON and docs in one pull request.
4. Add contract tests covering backward/forward compatibility as appropriate.
5. Require approvals from affected owners before merge.
