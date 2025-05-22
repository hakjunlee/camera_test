"""Sensor selector based on scenario requirements."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SensorScore:
    sensor_id: str
    score: float


def rank(scen: Dict[str, Any], db: List[Dict[str, Any]]) -> List[SensorScore]:
    """Rank sensors from database according to scenario.

    Parameters
    ----------
    scen: dict
        Parsed scenario configuration.
    db: list of dict
        Sensor database records.

    Returns
    -------
    list of SensorScore
        Ranked sensor list.

    TODO
    ----
    - Implement weighted scoring based on scenario priorities.
    - Support reading DB from CSV or SQLite.
    """
    # Placeholder ranking by order in the db
    return [SensorScore(sensor['id'], index) for index, sensor in enumerate(db)]
