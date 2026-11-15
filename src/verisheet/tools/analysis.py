"""Allowlisted deterministic Pandas/DuckDB operations used by the Executor."""

from typing import Any


def run_analysis(operation: str, frames: dict[str, Any], inputs: dict[str, Any]) -> Any:
    """Dispatch a validated operation name to a registered implementation.

    Supported baseline operation names should include: `group_aggregate`, `filter_rows`,
    `top_n`, `time_aggregate`, `quarter_comparison`, `safe_join`, and `grouped_ratio`.
    Unknown operations must fail closed. Return a pandas DataFrame plus a machine-readable
    operation summary; do not return model-authored numeric literals.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement operation dispatcher")


def group_aggregate(frame, group_by: list[str], metrics: dict[str, str]):
    """Group rows by columns and apply approved aggregations (sum/mean/count/min/max/nunique)."""
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement group_aggregate")


def filter_rows(frame, filters: list[dict[str, Any]]):
    """Apply validated typed filter predicates; reject unsupported operators/columns."""
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement filter_rows")


def top_n(frame, by: str, n: int, ascending: bool = False):
    """Return the requested ranking with deterministic tie/order behavior."""
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement top_n")


def time_aggregate(frame, date_column: str, frequency: str, metrics: dict[str, str]):
    """Aggregate approved metrics by calendar month/quarter/year with chronological ordering."""
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement time_aggregate")


def safe_join(left, right, join_spec):
    """Join two frames only after validating key uniqueness and expected cardinality.

    Compare row counts and relevant numeric totals before/after. Aggregate the right frame at
    the required grain first when instructed; fail rather than silently multiply measures.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement safe_join")


def quarter_comparison(frame, date_column: str, metric_column: str, aggregation: str = "sum"):
    """Compute current/previous completed-quarter comparison using documented date policy.

    Disclose observed-date assumption when there is no explicit reporting-close metadata.
    Handle zero/negative prior-period baseline with a documented convention.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement quarter_comparison")
