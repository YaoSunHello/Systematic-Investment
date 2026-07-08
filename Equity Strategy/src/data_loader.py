import json
from pathlib import Path
from typing import Any

from src.models import (
    CompanyProfile,
    ForecastAssumptions,
    HistoricalYear,
    MarketInputs,
    ValuationInput,
)


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_valuation_input(path: str | Path) -> ValuationInput:
    raw = load_json(path)
    return ValuationInput(
        company=CompanyProfile(**raw["company"]),
        history=[HistoricalYear(**row) for row in raw["history"]],
        market=MarketInputs(**raw["market"]),
        assumptions=ForecastAssumptions(**raw["assumptions"]),
    )


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")

