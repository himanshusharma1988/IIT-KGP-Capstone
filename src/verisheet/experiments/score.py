"""Compute evaluation metrics from structured traces and gold records."""

import argparse


def score_results(results_dir: str, gold_file: str, output_path: str) -> dict:
    """Calculate numeric accuracy, task success, execution success, plot accuracy,
    chart appropriateness, error-detection recall, false-verification rate, verified coverage,
    repair success, tool efficiency and median/p95 latency/token usage.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 6: implement scoring metrics")


def main() -> None:
    """CLI entrypoint for scoring experiment traces."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--gold", default="data/gold")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    # ####CODE HERE
    raise NotImplementedError("Person 6: wire scoring CLI")


if __name__ == "__main__":
    main()
