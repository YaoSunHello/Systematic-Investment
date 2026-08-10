from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


PACKAGE_ROOT = Path(__file__).resolve().parent
CONFIG_ROOT = PACKAGE_ROOT / "config"


def load_yaml(path: str | Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load systrading config files")
    with Path(path).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def load_defaults() -> dict[str, Any]:
    return load_yaml(CONFIG_ROOT / "defaults.yaml")


def load_correlations() -> dict[str, Any]:
    return load_yaml(CONFIG_ROOT / "correlations.yaml")

