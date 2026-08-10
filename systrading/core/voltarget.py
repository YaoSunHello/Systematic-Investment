from __future__ import annotations

from systrading.core.models import VolTarget


VOL_TARGET_TABLE = [
    (0.25, 0.12, 0.06),
    (0.40, 0.20, 0.10),
    (0.50, 0.25, 0.12),
    (0.75, 0.37, 0.19),
    (1.00, 0.50, 0.25),
]


def cash_vol_targets(trading_capital: float, percentage_vol_target: float, annualisation_factor: float = 16.0) -> VolTarget:
    if trading_capital <= 0:
        raise ValueError("trading_capital must be positive")
    if percentage_vol_target <= 0:
        raise ValueError("percentage_vol_target must be positive")
    annual = float(trading_capital) * float(percentage_vol_target)
    return VolTarget(
        trading_capital=float(trading_capital),
        percentage_vol_target=float(percentage_vol_target),
        annualised_cash_vol_target=annual,
        daily_cash_vol_target=annual / float(annualisation_factor),
    )


def recommend_vol_target(realistic_sr: float, skew_sign: str = "nonnegative", persona: str = "staunch") -> float:
    sr = max(float(realistic_sr), 0.0)
    if persona == "asset_allocator":
        sr = min(sr, 0.40)
    elif persona == "semi_auto":
        sr = min(sr, 0.50)
    else:
        sr = min(sr, 1.00)
    row = VOL_TARGET_TABLE[-1]
    for candidate in VOL_TARGET_TABLE:
        if sr <= candidate[0]:
            row = candidate
            break
    target = row[2] if skew_sign.lower().startswith("neg") else row[1]
    return min(target, 0.50)

