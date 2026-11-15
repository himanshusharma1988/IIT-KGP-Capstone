"""Person 1 CLI: acquire/standardise datasets and create the synthetic/corrupted workbooks."""

import argparse


def prepare_datasets(seed: int = 42, output_dir: str = "data") -> dict:
    """Prepare immutable public-source copies, standardised derivatives and FinanceOps synthetic data.

    Must record original URL, retrieval date, licence notice, SHA-256 and row count in the manifest.
    Generate the FinanceOps workbook from a fixed seed with README, Orders, Product_Costs, Expenses,
    Returns, Budget and Definitions sheets; at least four completed quarters and a partial fifth.
    Generate clean.xlsx plus corrupt_01.xlsx … corrupt_20.xlsx with a separate master key.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 1: implement dataset acquisition and generation")


def main() -> None:
    """Parse the required `--seed` option and call prepare_datasets."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="data")
    args = parser.parse_args()
    # ####CODE HERE
    raise NotImplementedError("Person 1: wire prepare_data CLI")


if __name__ == "__main__":
    main()
