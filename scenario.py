"""Scenario parser for camera test tool.

This module provides utilities to load and validate scenario YAML files
that describe environment conditions and priorities for the camera test
pipeline. The actual validation logic is yet to be implemented.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import yaml


def load(path: str | Path) -> Dict[str, Any]:
    """Load a scenario YAML file into a dictionary.

    Parameters
    ----------
    path: str | Path
        Path to the scenario YAML file.

    Returns
    -------
    dict
        Parsed scenario configuration.

    TODO
    ----
    - Validate schema and required fields.
    - Provide dataclass representation for type safety.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data
