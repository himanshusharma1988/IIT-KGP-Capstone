"""Append-only structured trace logging owned by Person 6; consumed by the Orchestrator."""

from pathlib import Path
from verisheet.schemas import TraceEvent


class TraceLogger:
    """Persist trace events as JSONL, one event per line, indexed by trace ID.

    Required fields include actor/event type, model/prompt version, tool/step status, token
    counts, latency, generated artifact references, verification verdict and failure category.
    Store bounded summaries and artifact paths/hashes rather than raw PII or whole workbooks.
    """

    def __init__(self, root_dir: str = "results/traces"):
        """Configure trace output directory and retention policy."""
        self.root_dir = Path(root_dir)
        # ####CODE HERE
        raise NotImplementedError("Person 6: initialise trace logger")

    def log_event(self, event: TraceEvent) -> None:
        """Append and flush one validated TraceEvent to the trace file for its trace ID."""
        # ####CODE HERE
        raise NotImplementedError("Person 6: implement structured event persistence")

    def load_trace(self, trace_id: str) -> list[TraceEvent]:
        """Load and validate all events belonging to a trace ID in timestamp order."""
        # ####CODE HERE
        raise NotImplementedError("Person 6: implement trace loading")
