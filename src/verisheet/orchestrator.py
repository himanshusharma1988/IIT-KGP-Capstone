"""Agent loop owned by Person 5; coordinates the Planner, Executor and Critic."""

from verisheet.schemas import AnswerResponse


class AgentOrchestrator:
    """Run the bounded Planner → Executor → Critic loop with state and structured trace events.

    Required transitions: ACCEPT returns; REPAIR retries the failed local step; REPLAN calls
    Planner with critic feedback; CLARIFY asks the user and stops. Enforce max 10 actions and
    at most 2 repairs by default. Never show unverified values as VERIFIED.
    """

    def __init__(self, profiler, retriever, planner, executor, critic, state_store, trace_logger):
        """Inject collaborators; use interfaces rather than importing their implementation details."""
        self.profiler = profiler
        self.retriever = retriever
        self.planner = planner
        self.executor = executor
        self.critic = critic
        self.state_store = state_store
        self.trace_logger = trace_logger
        # ####CODE HERE
        raise NotImplementedError("Person 5: initialise orchestrator")

    def answer_question(self, question: str, workbook_path: str, session_id: str) -> AnswerResponse:
        """Execute one user turn and return the canonical AnswerResponse.

        Steps: profile/fingerprint workbook; load matching state; retrieve definitions; plan;
        execute dependency steps; run independent verification; ask Critic for transition; repair,
        replan or clarify within budgets; persist only accepted verified context; return trace ID.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement bounded agent orchestration loop")

    def _handle_repair(self, plan, decision, prior_results, workbook_path, run_id):
        """Re-run only the affected operation and downstream dependent artifacts after REPAIR."""
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement targeted repair")

    def _make_failure_response(self, trace_id: str, message: str, workbook_id: str | None = None) -> AnswerResponse:
        """Build a safe FAILED/NOT_VERIFIED response without claiming numerical correctness."""
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement failure response")


def run_agent(
    question: str,
    workbook_reference: str,
    session_id: str,
    orchestrator: AgentOrchestrator | None = None,
) -> AnswerResponse:
    """Canonical application entrypoint returning one stable AnswerResponse.

    The UI calls this function (or an injected orchestrator service), not individual agents.
    It must preserve the bounded action/repair policy and trace all terminal outcomes.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 5: wire canonical run_agent entrypoint")
