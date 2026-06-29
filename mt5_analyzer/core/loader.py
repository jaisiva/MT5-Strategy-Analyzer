"""
loader.py

MT5 Excel report loader.

The loader is responsible for:

- Reading MT5 Excel reports
- Normalizing column names
- Validating report contents
- Building immutable Trade objects

The loader does NOT:

- Calculate statistics
- Assign patterns
- Assign sessions
- Generate reports

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from mt5_analyzer.core.column_mapper import ColumnMapper
from mt5_analyzer.core.exceptions import (
    FileReadError,
    LoaderError,
    UnsupportedFileFormatError,
)
from mt5_analyzer.core.logger import get_logger
from mt5_analyzer.core.trade_factory import TradeFactory
from mt5_analyzer.core.validator import Validator
from mt5_analyzer.domain.trade import Trade
from mt5_analyzer.domain.validation_report import ValidationReport

logger = get_logger(__name__)


@dataclass(slots=True)
class LoaderResult:
    """
    Result returned by MT5Loader.
    """

    source_file: Path
    trades: list[Trade]
    validation: ValidationReport
    total_rows: int


class MT5Loader:
    """
    MT5 Excel Loader.
    """

    SUPPORTED_EXTENSIONS = {
        ".xlsx",
        ".xls",
    }

    # --------------------------------------------------------------

    def load(
        self,
        filename: str | Path,
    ) -> LoaderResult:
        """
        Load MT5 report.
        """

        path = Path(filename)

        logger.info(
            "Loading MT5 report: {}",
            path,
        )

        if not path.exists():

            raise FileReadError(
                f"File not found: {path}"
            )

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:

            raise UnsupportedFileFormatError(
                f"Unsupported file type: {path.suffix}"
            )

        # ----------------------------------------------------------
        # Read Excel
        # ----------------------------------------------------------

        try:

            df = pd.read_excel(path)

        except Exception as ex:

            raise LoaderError(
                str(ex)
            ) from ex

        logger.info(
            "Report contains {} rows.",
            len(df),

        logger.info(
            "Excel columns: {}",
            df.columns.tolist(),
        )

        # ----------------------------------------------------------
        # Normalize Columns
        # ----------------------------------------------------------

        mapping = ColumnMapper.rename_mapping(
            df.columns.tolist()
        )

        df = df.rename(
            columns=mapping
        )

        # ----------------------------------------------------------
        # Validate
        # ----------------------------------------------------------

        validation = Validator.validate(
            df
        )

        if not validation.passed:

            logger.error(
                "Validation failed."
            )

            logger.error(
                "{} error(s), {} warning(s)",
                validation.error_count,
                validation.warning_count,
            )

            # ----------------------------------------------
            # Errors
            # ----------------------------------------------

            for error in validation.errors:

                location = ""

                if error.row is not None:

                    location += (
                        f"Row {error.row}"
                    )

                if error.column is not None:

                    if location:

                        location += ", "

                    location += (
                        f"Column '{error.column}'"
                    )

                if location:

                    logger.error(
                        "{} -> {}",
                        location,
                        error.message,
                    )

                else:

                    logger.error(
                        "{}",
                        error.message,
                    )

            # ----------------------------------------------
            # Warnings
            # ----------------------------------------------

            for warning in validation.warnings:

                location = ""

                if warning.row is not None:

                    location += (
                        f"Row {warning.row}"
                    )

                if warning.column is not None:

                    if location:

                        location += ", "

                    location += (
                        f"Column '{warning.column}'"
                    )

                if location:

                    logger.warning(
                        "{} -> {}",
                        location,
                        warning.message,
                    )

                else:

                    logger.warning(
                        "{}",
                        warning.message,
                    )

            return LoaderResult(
                source_file=path,
                trades=[],
                validation=validation,
                total_rows=len(df),
            )

        logger.success(
            "Validation passed."
        )

        # ----------------------------------------------------------
        # Create Trades
        # ----------------------------------------------------------

        trades: list[Trade] = []

        for _, row in df.iterrows():

            trade = TradeFactory.create_from_mapping(
                row.to_dict()
            )

            trades.append(
                trade
            )

        logger.success(
            "Loaded {} trades.",
            len(trades),
        )

        return LoaderResult(
            source_file=path,
            trades=trades,
            validation=validation,
            total_rows=len(df),
        )

    # --------------------------------------------------------------

    @staticmethod
    def supported_extensions() -> list[str]:
        """
        Returns supported file extensions.
        """

        return sorted(
            MT5Loader.SUPPORTED_EXTENSIONS
        )
