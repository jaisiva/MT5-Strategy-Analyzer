"""
cli.py

Command Line Interface for MT5 Strategy Analyzer.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

import argparse
import sys

from mt5_analyzer.domain.enums import PatternType
from mt5_analyzer.services.analysis_service import AnalysisService


def build_parser() -> argparse.ArgumentParser:
    """
    Create CLI parser.
    """

    parser = argparse.ArgumentParser(
        prog="mt5-analyzer",
        description="MT5 Strategy Analyzer",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # ---------------------------------------------------------
    # Original Strategy
    # ---------------------------------------------------------

    original = subparsers.add_parser(
        "original",
        help="Generate Original Strategy report",
    )

    original.add_argument(
        "--input",
        required=True,
        help="MT5 report (.xlsx)",
    )

    original.add_argument(
        "--output",
        required=True,
        help="Output Excel workbook",
    )

    original.add_argument(
        "--timeframe",
        default="H1",
        help="Timeframe",
    )

    # ---------------------------------------------------------
    # L Pattern Strategy
    # ---------------------------------------------------------

    lpattern = subparsers.add_parser(
        "lpattern",
        help="Generate L Pattern report",
    )

    lpattern.add_argument(
        "--input",
        required=True,
    )

    lpattern.add_argument(
        "--output",
        required=True,
    )

    lpattern.add_argument(
        "--timeframe",
        default="H1",
    )

    lpattern.add_argument(
        "--pattern",
        required=True,
        choices=[
            "L",
            "LL",
            "LLL",
            "LLLL",
            "LLLLL",
            "ALL_L",
        ],
    )

    # ---------------------------------------------------------
    # Drawdown Strategy
    # ---------------------------------------------------------

    dd = subparsers.add_parser(
        "drawdown",
        help="Generate Drawdown report",
    )

    dd.add_argument(
        "--input",
        required=True,
    )

    dd.add_argument(
        "--output",
        required=True,
    )

    dd.add_argument(
        "--timeframe",
        default="H1",
    )

    dd.add_argument(
        "--threshold",
        required=True,
        type=float,
    )

    return parser


# ---------------------------------------------------------------------


def run(argv: list[str] | None = None) -> int:
    """
    Execute CLI.
    """

    parser = build_parser()

    args = parser.parse_args(argv)

    service = AnalysisService()

    try:

        if args.command == "original":

            service.generate_original_report(

                input_file=args.input,

                output_file=args.output,

                timeframe=args.timeframe,

            )

        elif args.command == "lpattern":

            service.generate_lpattern_report(

                input_file=args.input,

                output_file=args.output,

                timeframe=args.timeframe,

                pattern=PatternType[args.pattern],

            )

        elif args.command == "drawdown":

            service.generate_drawdown_report(

                input_file=args.input,

                output_file=args.output,

                timeframe=args.timeframe,

                threshold=args.threshold,

            )

        else:

            parser.error(
                "Unknown command."
            )

        print()

        print("Analysis completed successfully.")

        print()

        print(f"Output: {args.output}")

        return 0

    except Exception as exc:

        print()

        print(f"ERROR: {exc}")

        return 1


# ---------------------------------------------------------------------


if __name__ == "__main__":

    sys.exit(
        run()
    )
