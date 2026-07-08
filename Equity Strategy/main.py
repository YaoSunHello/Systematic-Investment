import argparse
from pathlib import Path

from src.data_loader import load_valuation_input
from src.dcf_engine import calculate_dcf
from src.report_generator import write_reports


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Run FCFF DCF equity valuation.")
    parser.add_argument(
        "--input",
        default=str(base_dir / "data" / "raw" / "sample_company.json"),
        help="Path to valuation input JSON.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(base_dir / "outputs"),
        help="Directory for generated valuation and validation reports.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    valuation_input = load_valuation_input(args.input)
    result = calculate_dcf(valuation_input)
    write_reports(valuation_input, result, args.output_dir)
    print(f"{result.company.ticker} fair value: {result.fair_value_per_share:.2f} {result.company.currency}")
    print(f"Valuation gap: {result.valuation_gap:.1%}")
    print(f"Recommendation: {result.recommendation}")
    print(f"Confidence: {result.confidence_level} ({result.confidence_score}/100)")
    print(f"Reports written to: {Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()

