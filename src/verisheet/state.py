"""Session/workbook state management owned by Person 5."""

from pathlib import Path
from verisheet.schemas import AgentState, AnswerResponse


class StateStore:
    """Persist per-session context keyed by session ID and workbook fingerprint.

    Store only verified metric/period/filter context as accepted facts. Preserve enough recent
    turn summaries for multi-turn follow-up, but do not persist unverified answer text as truth.
    """

    def __init__(self, root_dir: str = "artifacts/sessions"):
        """Create the state directory and configure JSON persistence or another approved store."""
        self.root_dir = Path(root_dir)
        # ####CODE HERE
        raise NotImplementedError("Person 5: initialise state store")

    def load(self, session_id: str, workbook_id: str | None = None) -> AgentState:
        """Load state and ensure workbook fingerprint matches the active workbook context."""
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement state load")

    def save(self, state: AgentState) -> None:
        """Persist validated AgentState atomically to avoid partial/corrupt state files."""
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement state save")

    def update_from_verified_response(self, state: AgentState, response: AnswerResponse, plan) -> AgentState:
        """Update reusable metric/period/filter state only when response is VERIFIED."""
        # ####CODE HERE
        raise NotImplementedError("Person 5: implement verified state update")
