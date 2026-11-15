"""Deterministic verification tools owned by Person 5; independent from Qwen critique."""

from verisheet.schemas import AnalysisPlan, ExecutionResult, VerificationReport


def recompute_check(
    workbook_path: str,
    plan: AnalysisPlan,
    execution_result: ExecutionResult,
    tolerance: float = 1e-9,
) -> VerificationReport:
    """Independently recompute canonical numbers from source workbook and compare outputs.

    Use separately implemented canonical metric logic, not the Executor's cached result or
    Qwen's explanation. Validate metric definition, period, filters, aggregation, join grain,
    currency and denominator conventions. Return findings with expected/observed evidence.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 5: implement independent numerical recomputation")


def verify_chart_data(execution_result: ExecutionResult, tolerance: float = 1e-9) -> list[dict]:
    """Compare x/y arrays embedded in the chart artifact with the verified result table.

    Check labels, units, category ordering, baseline and that every plotted datum has a source
    row. Report discrepancies rather than adjusting or silently repairing plotted values.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 5: implement chart data verification")


def verify_plan_semantics(question: str, plan: AnalysisPlan, workbook_profile) -> list[dict]:
    """Run deterministic pre-execution checks on metric availability, date rules and join grain."""
    # ####CODE HERE
    raise NotImplementedError("Person 5: implement plan semantic checks")
