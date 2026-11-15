"""Person 5 critic/verifier tests."""
import pytest

@pytest.mark.skip(reason="Person 5: independently detect SUM versus MEAN and enable")
def test_numeric_verifier_detects_wrong_aggregation():
    """Implementation test for numeric verifier detects wrong aggregation; enable after its owning Jira story is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 5: detect wrong reporting period and enable")
def test_verifier_detects_wrong_quarter():
    """Implementation test for verifier detects wrong quarter; enable after its owning Jira story is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 5: altered chart point must fail and enable")
def test_chart_verifier_detects_plotted_value_mismatch():
    """Implementation test for chart verifier detects plotted value mismatch; enable after its owning Jira story is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 5: critic must not trust LLM numeric assertion and enable")
def test_critic_never_accepts_without_deterministic_verification():
    """Implementation test for critic never accepts without deterministic verification; enable after its owning Jira story is implemented."""
    # ####CODE HERE
    raise NotImplementedError

@pytest.mark.skip(reason="Person 5: ensure repair/replan/clarify decisions are distinct and enable")
def test_critic_routes_error_to_correct_transition():
    """Implementation test for critic routes error to correct transition; enable after its owning Jira story is implemented."""
    # ####CODE HERE
    raise NotImplementedError
