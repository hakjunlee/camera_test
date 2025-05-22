import tempfile
from pathlib import Path

from cli import main


def test_cli_runs(tmp_path: Path):
    scen_path = tmp_path / "scenario.yml"
    scen_path.write_text("scenario_id: TEST\n")
    assert main([str(scen_path)]) == 0
