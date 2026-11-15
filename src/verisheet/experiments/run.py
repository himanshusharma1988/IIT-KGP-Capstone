"""Run one system variant against the frozen development or held-out test questions."""

import argparse
from verisheet.schemas import ExperimentConfig


def run_experiment(config: ExperimentConfig) -> list[dict]:
    """Execute every question in the selected split using one consistent system variant.

    Keep model version, temperature, prompt versions, tool library and test set consistent
    across E1–E5. Persist one structured trace/result record per question.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 6: implement experiment runner")


def main() -> None:
    """Parse `--system` and `--split` arguments and call run_experiment."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", choices=["direct", "planner_executor", "llm_critic", "deterministic_critic", "full"], required=True)
    parser.add_argument("--split", choices=["dev", "test"], required=True)
    args = parser.parse_args()
    # ####CODE HERE
    raise NotImplementedError(f"Person 6: wire CLI for {args.system}/{args.split}")


if __name__ == "__main__":
    main()
