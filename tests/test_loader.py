"""
test_loader.py

Unit tests for MT5Loader.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mt5_analyzer.core.exceptions import (
    InvalidFileFormatError,
    MT5AnalyzerError,
)
from mt5_analyzer.core.loader import MT5Loader
from mt5_analyzer.domain.loader_result import LoaderResult


class TestMT5Loader:
    """
    Unit tests for MT5Loader.
    """

    def setup_method(self) -> None:
        """
        Create loader instance.
        """

        self.loader = MT5Loader()

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_load_valid_report(
        self,
        sample_report_file: Path,
    ) -> None:
        """
        Loader should successfully load a valid MT5 report.
        """

        result = self.loader.load(
            sample_report_file,
        )

        assert isinstance(
            result,
            LoaderResult,
        )

        assert len(result.trades) > 0

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_missing_file(self) -> None:
        """
        Loading a non-existing file should raise an exception.
        """

        with pytest.raises(
            FileNotFoundError,
        ):

            self.loader.load(
                "does_not_exist.xlsx",
            )

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_invalid_extension(
        self,
        tmp_path: Path,
    ) -> None:
        """
        Unsupported file extensions should be rejected.
        """

        file = tmp_path / "report.csv"

        file.write_text("dummy")

        with pytest.raises(
            InvalidFileFormatError,
        ):

            self.loader.load(file)

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_empty_workbook(
        self,
        tmp_path: Path,
    ) -> None:
        """
        Empty workbook should raise an analyzer error.
        """

        from openpyxl import Workbook

        workbook = Workbook()

        file = tmp_path / "empty.xlsx"

        workbook.save(file)

        with pytest.raises(
            MT5AnalyzerError,
        ):

            self.loader.load(file)

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_returns_trade_objects(
        self,
        sample_report_file: Path,
    ) -> None:
        """
        Loader should return Trade objects.
        """

        result = self.loader.load(
            sample_report_file,
        )

        assert len(result.trades) > 0

        first_trade = result.trades[0]

        assert hasattr(
            first_trade,
            "ticket",
        )

        assert hasattr(
            first_trade,
            "entry_time",
        )

        assert hasattr(
            first_trade,
            "exit_time",
        )

        assert hasattr(
            first_trade,
            "net_profit",
        )

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_trade_order(
        self,
        sample_report_file: Path,
    ) -> None:
        """
        Trades should be returned in chronological order.
        """

        result = self.loader.load(
            sample_report_file,
        )

        entry_times = [

            trade.entry_time

            for trade in result.trades

        ]

        assert entry_times == sorted(
            entry_times,
        )

    # ------------------------------------------------------------------

    @pytest.mark.loader
    @pytest.mark.unit
    def test_loader_result_contains_validation(
        self,
        sample_report_file: Path,
    ) -> None:
        """
        LoaderResult should include validation information.
        """

        result = self.loader.load(
            sample_report_file,
        )

        assert result.validation_report is not None
