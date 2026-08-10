from __future__ import annotations

from itertools import permutations
from typing import Mapping, Sequence


TABLE8_THREE_ASSET_PATTERNS = {
    (0.0, 0.5, 0.0): (0.30, 0.40, 0.30),
    (0.0, 0.9, 0.0): (0.27, 0.46, 0.27),
    (0.5, 0.0, 0.5): (0.37, 0.26, 0.37),
    (0.0, 0.5, 0.9): (0.45, 0.45, 0.10),
    (0.9, 0.0, 0.9): (0.39, 0.22, 0.39),
    (0.5, 0.9, 0.5): (0.29, 0.42, 0.29),
    (0.9, 0.5, 0.9): (0.42, 0.16, 0.42),
}


def _nearest_pattern_corr(value: float) -> float:
    value = max(float(value), 0.0)
    return min((0.0, 0.5, 0.9), key=lambda x: abs(x - value))


def three_asset_table8_weights(corr_ab: float, corr_ac: float, corr_bc: float) -> tuple[float, float, float]:
    triple = (
        _nearest_pattern_corr(corr_ab),
        _nearest_pattern_corr(corr_ac),
        _nearest_pattern_corr(corr_bc),
    )
    if triple[0] == triple[1] == triple[2]:
        return (1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
    indices = (0, 1, 2)
    for perm in permutations(indices):
        pairs = {
            frozenset((perm[0], perm[1])): triple[0],
            frozenset((perm[0], perm[2])): triple[1],
            frozenset((perm[1], perm[2])): triple[2],
        }
        ordered = (
            pairs[frozenset((0, 1))],
            pairs[frozenset((0, 2))],
            pairs[frozenset((1, 2))],
        )
        if ordered in TABLE8_THREE_ASSET_PATTERNS:
            weights_ordered = TABLE8_THREE_ASSET_PATTERNS[ordered]
            mapped = [0.0, 0.0, 0.0]
            for new_idx, old_idx in enumerate(perm):
                mapped[old_idx] = weights_ordered[new_idx]
            return tuple(mapped)  # type: ignore[return-value]
    raise ValueError(f"unsupported three-asset correlation pattern: {triple}")


def handcraft(groups: Mapping[str, Sequence[str]] | Sequence[str], correlations: Mapping[tuple[str, str], float] | None = None) -> dict[str, float]:
    """Bottom-up handcrafted weights for simple groups.

    For a flat 3-asset sequence this applies Table 8 directly. For a mapping of
    groups, capital is split equally across groups and then equally within each
    group unless a group has exactly three assets and correlations are supplied.
    """
    correlations = correlations or {}
    if not isinstance(groups, Mapping):
        assets = list(groups)
        if len(assets) == 1:
            return {assets[0]: 1.0}
        if len(assets) == 2:
            return {assets[0]: 0.5, assets[1]: 0.5}
        if len(assets) == 3:
            a, b, c = assets
            weights = three_asset_table8_weights(
                correlations.get((a, b), correlations.get((b, a), 0.0)),
                correlations.get((a, c), correlations.get((c, a), 0.0)),
                correlations.get((b, c), correlations.get((c, b), 0.0)),
            )
            return dict(zip(assets, weights))
        equal = 1.0 / len(assets)
        return {asset: equal for asset in assets}

    group_count = len(groups)
    if group_count == 0:
        raise ValueError("groups cannot be empty")
    result: dict[str, float] = {}
    group_weight = 1.0 / group_count
    for members in groups.values():
        inner = handcraft(list(members), correlations)
        for asset, weight in inner.items():
            result[asset] = group_weight * weight
    total = sum(result.values())
    return {asset: weight / total for asset, weight in result.items()}


def apply_sr_adjustment(weights: Mapping[str, float], adjustments: Mapping[str, float]) -> dict[str, float]:
    adjusted = {asset: float(weight) * float(adjustments.get(asset, 1.0)) for asset, weight in weights.items()}
    total = sum(adjusted.values())
    if total <= 0:
        raise ValueError("adjusted weights must have positive total")
    return {asset: value / total for asset, value in adjusted.items()}

