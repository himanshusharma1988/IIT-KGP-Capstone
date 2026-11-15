"""Export canonical Pydantic models as JSON Schema for non-Python consumers."""

import json
from pathlib import Path
from verisheet import schemas
from verisheet.schemas import (
    WorkbookProfile, RetrievedContext, AnalysisPlan, ExecutionResult,
    VerificationReport, CriticDecision, AgentState, AnswerResponse, TraceEvent,
)


def export_schemas(output_dir: str = "contracts/schemas") -> list[str]:
    """Write JSON Schema files for public contract classes from schemas.py.

    `schemas.py` is the source of truth. Never hand-edit generated schema JSON independently;
    regenerate this folder after a reviewed Pydantic contract change.

    Args:
        output_dir: Directory receiving one JSON Schema file per public contract.
    Returns:
        list[str]: Paths written to disk.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    models = {
        "workbook_profile": WorkbookProfile,
        "retrieved_context": RetrievedContext,
        "analysis_plan": AnalysisPlan,
        "execution_result": ExecutionResult,
        "verification_report": VerificationReport,
        "critic_decision": CriticDecision,
        "agent_state": AgentState,
        "answer_response": AnswerResponse,
        "trace_event": TraceEvent,
    }
    written: list[str] = []
    for name, model in models.items():
        path = output / f"{name}.schema.json"
        path.write_text(json.dumps(model.model_json_schema(), indent=2), encoding="utf-8")
        written.append(str(path))
    return written


if __name__ == "__main__":
    export_schemas()
