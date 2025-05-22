"""Command line interface for camera test tool."""
from __future__ import annotations

import argparse
from pathlib import Path

from scenario import load as load_scenario
from selector import rank
from param import generate
from capture import run as capture_run
from metric import evaluate
from report import make as make_report


def main(argv: list[str] | None = None) -> int:
    """Entry point for CLI.

    Parameters
    ----------
    argv: list[str] | None
        Optional list of CLI arguments.

    Returns
    -------
    int
        Exit status code.
    """
    parser = argparse.ArgumentParser(description="Camera test automation tool")
    parser.add_argument("scenario", type=Path, help="Path to scenario YAML")
    args = parser.parse_args(argv)

    scen = load_scenario(args.scenario)

    # TODO: Load real sensor database
    dummy_db = [{"id": "S1"}, {"id": "S2"}]
    ranked = rank(scen, dummy_db)
    best_sensor = dummy_db[0] if ranked else {}

    cfg = generate(best_sensor, scen)
    dataset_id = capture_run(cfg)
    metrics = evaluate(dataset_id, scen)
    report_path = make_report(dataset_id, metrics, scen)

    print(f"Report generated at {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
