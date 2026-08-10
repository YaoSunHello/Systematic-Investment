from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def _as_corr(corr: Iterable[Iterable[float]], n: int) -> np.ndarray:
    matrix = np.asarray(corr, dtype=float)
    if matrix.shape != (n, n):
        raise ValueError(f"correlation matrix must be {n}x{n}")
    return matrix


def div_multiplier(
    weights: Iterable[float],
    corr: Iterable[Iterable[float]],
    cap: float = 2.5,
    floor_zero: bool = True,
) -> float:
    w = np.asarray(list(weights), dtype=float)
    if w.ndim != 1 or w.size == 0:
        raise ValueError("weights must be a non-empty vector")
    matrix = _as_corr(corr, w.size)
    if floor_zero:
        matrix = np.where(matrix < 0.0, 0.0, matrix)
    variance = float(w @ matrix @ w.T)
    if variance <= 0:
        return cap
    return min(1.0 / math.sqrt(variance), cap)


def average_offdiag_corr(corr: Iterable[Iterable[float]], floor_zero: bool = True) -> float:
    matrix = np.asarray(corr, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("corr must be square")
    if matrix.shape[0] < 2:
        return 1.0
    if floor_zero:
        matrix = np.where(matrix < 0.0, 0.0, matrix)
    mask = ~np.eye(matrix.shape[0], dtype=bool)
    return float(matrix[mask].mean())


def table18_approx_multiplier(
    n_assets: int,
    avg_corr: float,
    cap: float = 2.5,
    table_style_zero_corr: bool = True,
) -> float:
    """Approximate IDM/FDM from asset count and average correlation.

    The precise equal-weight formula is used as the baseline. The book's concept
    table rounds the zero-correlation two-asset case to 1.41, so that path is
    preserved for golden-test reconciliation.
    """
    if n_assets <= 0:
        raise ValueError("n_assets must be positive")
    if n_assets == 1:
        return 1.0
    corr = max(float(avg_corr), 0.0)
    if table_style_zero_corr and n_assets == 2 and abs(corr) < 1e-12:
        return min(math.sqrt(2.0), cap)
    variance = (1.0 / n_assets) + ((n_assets - 1.0) / n_assets) * corr
    return min(1.0 / math.sqrt(variance), cap)

