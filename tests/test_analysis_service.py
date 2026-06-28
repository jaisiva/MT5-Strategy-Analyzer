"""
test_analysis_service.py

Integration tests for AnalysisService.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from mt5_analyzer.services.analysis_service import (
    AnalysisService,
)


class TestAnalysisService:

    @pytest.mark.integration
    def test_generate_original_report(
        self,
        sample_report_file,
        output_dir,
    ):

        service = AnalysisService()

        output = output_dir / "original.xlsx"

        result = service.generate_original_report(

            input_file=sample_report_file,

            output_file=output,

            timeframe="H1",

        )

        assert output.exists()

        assert result.statistics.total_trades > 0

    # ------------------------------------------------------------

    @pytest.mark.integration
    def test_generate_drawdown_report(
        self,
        sample_report_file,
        output_dir,
    ):

        service = AnalysisService()

        output = output_dir / "dd20.xlsx"

        result = service.generate_drawdown_report(

            input_file=sample_report_file,

            output_file=output,

            timeframe="H1",

            threshold=20,

        )

        assert output.exists()

        assert hasattr(result, "cycles")

    # ------------------------------------------------------------

    @pytest.mark.integration
    def test_generate_lpattern_report(
        self,
        sample_report_file,
        output_dir,
    ):

        from mt5_analyzer.domain.enums import PatternType

        service = AnalysisService()

        output = output_dir / "lll.xlsx"

        result = service.generate_lpattern_report(

            input_file=sample_report_file,

            output_file=output,

            timeframe="H1",

            pattern=PatternType.LLL,

        )

        assert output.exists()

        assert result.statistics is not None
