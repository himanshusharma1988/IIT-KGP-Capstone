"""Executor agent owned by Person 4; maps typed plans to allowlisted data tools."""

from pathlib import Path
from verisheet.schemas import AnalysisPlan, ExecutionResult


class Executor:
    """Run approved analysis steps and create result tables, scripts and chart artifacts.

    Do not use unrestricted eval/exec on model output. Planner operations must map to a fixed
    operation registry. Every step must validate sheet/column references and dependencies.
    """

    def __init__(self, artifact_dir: str = "artifacts", sandbox=None):
        """Configure artifact output and restricted execution backend."""
        self.artifact_dir = Path(artifact_dir)
        self.sandbox = sandbox
        # ####CODE HERE
        raise NotImplementedError("Person 4: initialise tool registry and artifact directories")

    def execute_plan(self, plan: AnalysisPlan, workbook_path: str, run_id: str) -> list[ExecutionResult]:
        """Execute plan steps in dependency order and return one result per completed step.

        Enforce action/time/resource budgets. Stop on failed dependencies. Save result tables,
        executable scripts, script hashes, chart files and machine-readable plotted arrays.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 4: implement execute_plan")

    def execute_step(self, step, workbook_path: str, run_id: str, prior_results: dict) -> ExecutionResult:
        """Execute one AnalysisStep using only registered tools and its validated dependencies."""
        # ####CODE HERE
        raise NotImplementedError("Person 4: implement execute_step")

    def validate_plan_references(self, plan: AnalysisPlan, workbook_profile) -> None:
        """Reject unknown sheets/columns, unsupported operations and dependency cycles."""
        # ####CODE HERE
        raise NotImplementedError("Person 4: implement plan reference validation")


def execute_plan(
    plan: AnalysisPlan,
    workbook_path: str,
    run_id: str,
    executor: Executor | None = None,
) -> list[ExecutionResult]:
    """Canonical function wrapper around Executor.execute_plan for module integration.

    Accepts the shared AnalysisPlan and returns a list of shared ExecutionResult payloads.
    `executor` is injected by Orchestrator/tests; no model-generated code is executed directly.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 4: wire canonical execute_plan entrypoint")
