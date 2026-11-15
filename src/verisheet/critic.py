"""Hybrid Critic owned by Person 5: deterministic checks plus a separate Qwen critic prompt."""

from pathlib import Path
from verisheet.qwen_client import QwenClient
from verisheet.schemas import (
    AnalysisPlan, CriticDecision, ExecutionResult, VerificationReport, WorkbookProfile,
)


class Critic:
    """Evaluate intent/plan semantics and independently verified execution evidence.

    Qwen may assess semantic match and chart appropriateness. Deterministic verification must
    control numeric correctness. Critic may ACCEPT only after all mandatory checks pass.
    """

    def __init__(self, client: QwenClient | None = None, prompt_path: str = "prompts/critic.txt"):
        """Initialise shared Qwen client and versioned critic prompt."""
        self.client = client or QwenClient()
        self.prompt_path = Path(prompt_path)
        # ####CODE HERE
        raise NotImplementedError("Person 5: load critic prompt and verification policy")

    def evaluate(
        self,
        question: str,
        plan: AnalysisPlan,
        execution_results: list[ExecutionResult],
        verification: VerificationReport,
        workbook_profile: WorkbookProfile,
    ) -> CriticDecision:
        """Return ACCEPT/REPAIR/REPLAN/CLARIFY with precise step and evidence.

        Never trust LLM arithmetic. NOT_VERIFIED must be returned when independent recomputation
        cannot be completed. REPAIR is for local execution/artifact defects; REPLAN is for a wrong
        analytical approach; CLARIFY is for missing/ambiguous source information.
        """
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement hybrid critic evaluation")

    def semantic_review(self, question: str, plan: AnalysisPlan, answer_summary: dict) -> dict:
        """Use Qwen critic prompt to judge intent match, assumptions and chart appropriateness."""
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement semantic review")
