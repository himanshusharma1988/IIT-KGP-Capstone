"""Executable contract tests: these should pass before module implementation begins."""

from verisheet.schemas import (
    AnswerResponse, AnalysisPlan, ExecutionResult, RetrievedContext,
    VerificationReport, WorkbookProfile,
)
from conftest import load_example


def test_workbook_profile_fixture_matches_schema():
    """Implementation test for workbook profile fixture matches schema; enable after its owning  task is implemented."""
    assert WorkbookProfile.model_validate(load_example("workbook_profile.json")).sheets[0].name == "Orders"


def test_retrieved_context_fixture_matches_schema():
    """Implementation test for retrieved context fixture matches schema; enable after its owning  task is implemented."""
    context = RetrievedContext.model_validate(load_example("retrieved_context.json"))
    assert context.items[0].source_path


def test_analysis_plan_fixture_matches_schema():
    """Implementation test for analysis plan fixture matches schema; enable after its owning  task is implemented."""
    plan = AnalysisPlan.model_validate(load_example("analysis_plan.json"))
    assert len(plan.steps) == 2
    assert plan.steps[1].depends_on == [plan.steps[0].step_id]


def test_execution_result_fixture_matches_schema():
    """Implementation test for execution result fixture matches schema; enable after its owning  task is implemented."""
    result = ExecutionResult.model_validate(load_example("execution_result.json"))
    assert result.status == "SUCCESS"


def test_verification_report_fixture_matches_schema():
    """Implementation test for verification report fixture matches schema; enable after its owning  task is implemented."""
    report = VerificationReport.model_validate(load_example("verification_report.json"))
    assert report.verified is False


def test_answer_response_cannot_claim_verified_without_report():
    """Implementation test for answer response cannot claim verified without report; enable after its owning  task is implemented."""
    import pytest
    with pytest.raises(ValueError):
        AnswerResponse(status="VERIFIED", answer="no evidence", trace_id="t1")
