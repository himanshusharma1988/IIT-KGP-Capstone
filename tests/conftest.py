"""Shared fixture paths and validated sample contracts for module tests."""

import json
from pathlib import Path
import pytest
from verisheet.schemas import (
    AnswerResponse, AnalysisPlan, ExecutionResult, RetrievedContext,
    VerificationReport, WorkbookProfile,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "contracts" / "examples"


def load_example(name: str) -> dict:
    """Read one version-controlled JSON contract fixture."""
    with (EXAMPLES / name).open("r", encoding="utf-8") as stream:
        return json.load(stream)


@pytest.fixture
def workbook_profile():
    """Validated WorkbookProfile example for Planner and RAG tests."""
    return WorkbookProfile.model_validate(load_example("workbook_profile.json"))


@pytest.fixture
def retrieved_context():
    """Validated RetrievedContext example for Planner tests."""
    return RetrievedContext.model_validate(load_example("retrieved_context.json"))


@pytest.fixture
def analysis_plan():
    """Validated AnalysisPlan example for Executor/Critic tests."""
    return AnalysisPlan.model_validate(load_example("analysis_plan.json"))


@pytest.fixture
def execution_result():
    """Validated ExecutionResult example for Critic tests."""
    return ExecutionResult.model_validate(load_example("execution_result.json"))


@pytest.fixture
def verification_report():
    """Validated VerificationReport example for Orchestrator/UI tests."""
    return VerificationReport.model_validate(load_example("verification_report.json"))


@pytest.fixture
def answer_response():
    """Validated AnswerResponse example for UI tests."""
    return AnswerResponse.model_validate(load_example("answer_response.json"))
