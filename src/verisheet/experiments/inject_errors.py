"""Execute the controlled robustness/error-injection suite."""

import argparse


def run_injection_suite(suite_name: str, cases_file: str) -> list[dict]:
    """Run at least 20 controlled faults and record whether the system detects/repairs/refuses.

    Examples include wrong aggregation, wrong period, duplicated join key, malformed schema,
    missing profit column, mismatched chart arrays, prompt-injection cell text and unsafe code.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 6: implement error injection suite")


def main() -> None:
    """CLI entrypoint for `--suite 20_cases`."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", required=True)
    parser.add_argument("--cases", default="data/error_cases.jsonl")
    args = parser.parse_args()
    # ####CODE HERE
    raise NotImplementedError(f"Person 6: wire injection CLI for {args.suite}")


if __name__ == "__main__":
    main()
