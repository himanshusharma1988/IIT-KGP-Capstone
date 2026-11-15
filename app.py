"""Streamlit front end owned by Person 6; uses AnswerResponse as the backend contract."""

import streamlit as st


def render_app() -> None:
    """Render upload, workbook profile, chat, result/chart display and verification status.

    The UI should call the orchestrator service rather than reimplementing business logic.
    Retain session ID across turns; retain workbook reference until user replaces the upload.
    Display assumptions, clarification/refusal messages and trace ID. Render chart only when
    the backend provides a real chart artifact. Provide a link/expander to the trace dashboard.
    """
    st.set_page_config(page_title="VeriSheet", layout="wide")
    st.title("VeriSheet — Agentic Spreadsheet Analysis")
    st.caption("Contract-first starter application")
    uploaded = st.file_uploader("Upload an XLSX or CSV workbook", type=["xlsx", "csv"])
    if uploaded is not None:
        st.success(f"Selected file: {uploaded.name}")
        st.info("Person 6: connect quarantined upload storage, profile service and chat/orchestrator here.")
    st.text_input("Ask a question about the uploaded workbook", key="question_input")
    st.button("Analyse", disabled=True, help="Enabled when the orchestrator service is connected")
    st.warning("Starter scaffold: backend integration is not yet implemented.")
    # ####CODE HERE
    # Person 6: connect upload persistence, profile rendering, multi-turn chat and AnswerResponse.


if __name__ == "__main__":
    render_app()
