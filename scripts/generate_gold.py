"""Person 1 CLI: build gold answers using independent, deterministic reference scripts."""

import argparse


def generate_gold(config_path: str, output_dir: str = "data/gold") -> dict:
    """Calculate gold answer values/tables/chart specs for a frozen question-workbook bank.

    Gold generation must be independent of Planner/Executor code. It must validate workbook hash,
    metric rules, filters, date ranges, join cardinality and refusal conditions. Keep generated gold
    answers/scripts outside model prompts, application RAG corpus and ordinary trace logs.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 1: implement gold-answer generation")


def main() -> None:
    """Parse `--config` and `--output-dir` then generate gold answers."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", default="data/gold")
    args = parser.parse_args()
    # ####CODE HERE
    raise NotImplementedError("Person 1: wire generate_gold CLI")


if __name__ == "__main__":
    main()
