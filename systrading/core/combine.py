from __future__ import annotations

from typing import Iterable

import numpy as np

from systrading.core.diversification import div_multiplier
from systrading.core.models import Forecast


def combine_forecasts(
    forecasts: Iterable[Forecast],
    weights: Iterable[float] | None = None,
    corr: Iterable[Iterable[float]] | None = None,
    cap: float = 20.0,
    fdm_cap: float = 2.5,
    floor_zero: bool = True,
) -> tuple[float, dict[str, float]]:
    values = np.asarray([f.value for f in forecasts], dtype=float)
    if values.size == 0:
        raise ValueError("at least one forecast is required")
    if weights is None:
        w = np.full(values.size, 1.0 / values.size)
    else:
        w = np.asarray(list(weights), dtype=float)
    if w.shape != values.shape:
        raise ValueError("weights must match forecasts")
    if np.any(w < 0):
        raise ValueError("forecast weights must be non-negative")
    if not np.isclose(w.sum(), 1.0):
        raise ValueError("forecast weights must sum to 1")
    raw = float(w @ values)
    if values.size == 1:
        fdm = 1.0
    else:
        if corr is None:
            corr = np.eye(values.size)
        fdm = div_multiplier(w, corr, cap=fdm_cap, floor_zero=floor_zero)
    combined = float(np.clip(raw * fdm, -cap, cap))
    return combined, {"raw_combined": raw, "fdm": fdm, "combined_forecast": combined}

