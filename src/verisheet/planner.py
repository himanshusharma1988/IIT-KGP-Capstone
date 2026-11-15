"""Planner agent owned by Person 3; produces AnalysisPlan, never numeric answers."""

from pathlib import Path
from verisheet.qwen_client import QwenClient
from verisheet.schemas import AgentState, AnalysisPlan, RetrievedContext, WorkbookProfile


class Planner:
    """Convert a natural-language analytical question into a dependency-aware AnalysisPlan.

    Inputs are user query, WorkbookProfile, RetrievedContext and previously accepted AgentState.
    Output must validate against `AnalysisPlan` from schemas.py. Planner must not calculate
    numeric answers, write arbitrary Python, or mark any output verified.
    """

    def __init__(self, client: QwenClient | None = None, prompt_path: str = "prompts/planner.txt"):
        """Create planner with shared Qwen client and versioned system prompt."""
        self.client = client or QwenClient()
        self.prompt_path = Path(prompt_path)
        # ####CODE HERE
        raise NotImplementedError("Person 3: load/validate planner prompt")

    def generate_plan(
        self,
        question: str,
        workbook_profile: WorkbookProfile,
        retrieved_context: RetrievedContext,
        previous_state: AgentState | None = None,
        feedback: dict | None = None,
    ) -> AnalysisPlan:
        """Ask Qwen for a strict JSON plan and validate it with the shared Pydantic schema.

        The prompt input must include workbook fingerprint/schema, retrieved source references,
        prior verified context, action budget and the requested question. Detect unanswerable
        metrics (e.g. Online Retail profit) and produce CLARIFY, not a proxy metric.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 3: implement generate_plan")

    def revise_plan(self, prior_plan: AnalysisPlan, critic_feedback: dict, state: AgentState) -> AnalysisPlan:
        """Produce a targeted revised plan after REPLAN; preserve validated steps where possible."""
        # ####CODE HERE
        raise NotImplementedError("Person 3: implement revise_plan")


def parse_plan_response(raw_content: str) -> AnalysisPlan:
    """Parse Qwen response into AnalysisPlan; reject prose, missing fields and extra fields."""
    # ####CODE HERE
    raise NotImplementedError("Person 3: implement strict JSON extraction and validation")


def generate_plan(
    question: str,
    workbook_profile: WorkbookProfile,
    retrieved_context: RetrievedContext,
    previous_state: AgentState | None = None,
    feedback: dict | None = None,
    planner: Planner | None = None,
) -> AnalysisPlan:
    """Canonical function wrapper around Planner.generate_plan for dependency injection.

    `planner` should be supplied by Orchestrator/tests; when omitted, construct the default
    Planner. The public input/output schema is the same as the Planner method.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 3: wire canonical generate_plan entrypoint")
