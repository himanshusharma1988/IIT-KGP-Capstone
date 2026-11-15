"""Chart rendering from executed result tables; no values may be invented or changed."""

from pathlib import Path
from verisheet.schemas import ChartSpec


def make_chart(result_table_path: str, chart_spec: ChartSpec, output_dir: str = "artifacts/charts") -> dict:
    """Render a Matplotlib/Plotly chart and return image path plus exact plotted arrays.

    Chart type, x/y columns, labels, units, category ordering and baseline must be validated.
    Values must be loaded from the result table. The returned `plotted_data` is later compared
    byte-for-byte or within an explicit numeric tolerance against the verified result data.
    """
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement make_chart")


def validate_chart_spec(columns: list[str], chart_spec: ChartSpec) -> None:
    """Reject missing columns, unsupported chart/axis combinations and inconsistent units."""
    # ####CODE HERE
    raise NotImplementedError("Person 4: implement chart specification validation")
