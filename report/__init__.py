"""Report builder.

This package generates Markdown and PDF reports from metric results. The
PDF generation is left as a TODO.
"""
from __future__ import annotations

from typing import Any, Dict
from pathlib import Path


def make(dataset_id: str, metrics: Dict[str, Any], scen: Dict[str, Any]) -> Path:
    """Create report from evaluated metrics.

    Parameters
    ----------
    dataset_id: str
        Identifier of the captured dataset.
    metrics: dict
        Metric results returned by :func:`metric.evaluate`.
    scen: dict
        Parsed scenario configuration.

    Returns
    -------
    pathlib.Path
        Path to the generated Markdown report.

    TODO
    ----
    - Format results into Markdown tables.
    - Convert Markdown to PDF.
    """
    report_path = Path(f"{dataset_id}_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Report\n")
        f.write(str(metrics))
    return report_path
