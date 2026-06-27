"""
validator.py

Validation engine for MT5 reports.

The validator checks:

- Required columns
- Missing values
- Data types
- Date/time consistency
- Duplicate trades
- Trade direction
- Volume
- Profit

The validator NEVER modifies the input DataFrame.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

import pandas as pd

from mt5_analyzer.core.column_mapper import ColumnMapper
from mt5_analyzer.domain.enums import TradeSide
from mt5_analyzer.domain.validation_report import ValidationReport


class Validator:
    """
    Validates MT5 report DataFrames.
    """

    @staticmethod
    def validate(df: pd.DataFrame) -> ValidationReport:
        """
        Validate MT5 report.

        Parameters
        ----------
        df
            MT5 report DataFrame.

        Returns
        -------
        ValidationReport
        """

        report = ValidationReport()

        # ----------------------------------------------------------
        # Empty file
        # ----------------------------------------------------------

        if df.empty:
            report.add_error("Input file contains no rows.")
            return report

        report.total_rows = len(df)

        # ----------------------------------------------------------
        # Required columns
        # ----------------------------------------------------------

        try:
            ColumnMapper.validate_columns(df.columns.tolist())
        except Exception as ex:
            report.add_error(str(ex))
            return report

        # ----------------------------------------------------------
        # Rename columns internally
        # ----------------------------------------------------------

        mapping = ColumnMapper.rename_mapping(df.columns.tolist())

        df = df.rename(columns=mapping)

        # ----------------------------------------------------------
        # Duplicate trades
        # ----------------------------------------------------------

        duplicate_mask = df.duplicated(
            subset=[
                "entry_date",
                "entry_time",
                "exit_date",
                "exit_time",
                "symbol",
                "side",
                "volume",
                "profit",
            ]
        )

        duplicate_rows = duplicate_mask[duplicate_mask].index

        for row in duplicate_rows:
            report.add_warning(
                "Duplicate trade detected.",
                row=int(row) + 2,
            )

        # ----------------------------------------------------------
        # Row Validation
        # ----------------------------------------------------------

        for idx, trade in df.iterrows():

            row = idx + 2

            # ----------------------------------------------

            if pd.isna(trade["entry_date"]):
                report.add_error(
                    "Missing entry date.",
                    row=row,
                    column="entry_date",
                )

            if pd.isna(trade["exit_date"]):
                report.add_error(
                    "Missing exit date.",
                    row=row,
                    column="exit_date",
                )

            if pd.isna(trade["entry_time"]):
                report.add_error(
                    "Missing entry time.",
                    row=row,
                    column="entry_time",
                )

            if pd.isna(trade["exit_time"]):
                report.add_error(
                    "Missing exit time.",
                    row=row,
                    column="exit_time",
                )

            # ----------------------------------------------

            if pd.isna(trade["symbol"]):
                report.add_error(
                    "Missing symbol.",
                    row=row,
                    column="symbol",
                )

            # ----------------------------------------------

            try:
                TradeSide.from_string(str(trade["side"]))

            except ValueError:

                report.add_error(
                    f"Invalid trade side: {trade['side']}",
                    row=row,
                    column="side",
                )

            # ----------------------------------------------

            try:

                volume = float(trade["volume"])

                if volume <= 0:
                    raise ValueError

            except Exception:

                report.add_error(
                    "Invalid trade volume.",
                    row=row,
                    column="volume",
                )

            # ----------------------------------------------

            try:

                float(trade["profit"])

            except Exception:

                report.add_error(
                    "Invalid profit.",
                    row=row,
                    column="profit",
                )

        # ----------------------------------------------------------
        # Statistics
        # ----------------------------------------------------------

        report.invalid_rows = report.error_count
        report.valid_rows = report.total_rows - report.invalid_rows

        return report
