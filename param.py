"""Parameter generator for selected sensor and scenario."""
from __future__ import annotations

from typing import Any, Dict


def generate(sensor: Dict[str, Any], scen: Dict[str, Any]) -> Dict[str, Any]:
    """Generate pipeline parameters for a given sensor and scenario.

    Parameters
    ----------
    sensor: dict
        Selected sensor record.
    scen: dict
        Parsed scenario configuration.

    Returns
    -------
    dict
        Parameter configuration dictionary.

    TODO
    ----
    - Derive exposure, gain, FPS and ISP settings from sensor capabilities.
    """
    # Placeholder implementation returning static parameters
    return {
        "exposure_ms": 3,
        "gain": 1.0,
        "fps": 30,
        "isp": {},
    }
