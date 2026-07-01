"""
analysis_service.py

High-level application service for MT5 Strategy Analyzer.

Coordinates loading, validation, strategy execution and
Excel report generation.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from pathlib import Path

from mt5_analyzer.core.loader import MT5Loader

from mt5_analyzer.application.original_engine import OriginalStrategyEngine
from mt5_analyzer.application.lpattern_engine import LPatternEngine
from mt5_analyzer.application.drawdown.drawdown_engine import DrawdownEngine
from mt5_analyzer.application.portfolio_engine import PortfolioEngine

from mt5_analyzer.reports.excel.original_writer import OriginalReportWriter
from mt5_analyzer.reports.excel.lpattern_writer import LPatternReportWriter
from mt5_analyzer.reports.excel.drawdown_writer import DrawdownReportWriter
from mt5_analyzer.reports.excel.portfolio_writer import PortfolioReportWriter

from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.domain.portfolio_result import PortfolioResult
from mt5_analyzer.domain.portfolio_input import PortfolioInput


class AnalysisService:
    """
    Main application service.

    This class coordinates the complete analysis workflow.

    MT5 Report
        ↓
    Loader
        ↓
    Strategy Engine
        ↓
    Statistics
        ↓
    Excel Writer
    """

    def __init__(self) -> None:

        self.loader = MT5Loader()
        self.portfolio_engine = PortfolioEngine()
        self.portfolio_writer = PortfolioReportWriter()

    # -----------------------------------------------------------------

    def generate_original_report(
        self,
        *,
        input_file: str | Path,
        output_file: str | Path,
        timeframe: str,
    ) -> StrategyResult:
        """
        Generate Original Strategy report.
        """

        engine = OriginalStrategyEngine()

        writer = OriginalReportWriter()

        return self._run_strategy(
            input_file=input_file,
            output_file=output_file,
            timeframe=timeframe,
            engine=engine,
            writer=writer,
        )

    # -----------------------------------------------------------------

    def generate_lpattern_report(
        self,
        *,
        input_file: str | Path,
        output_file: str | Path,
        timeframe: str,
        pattern,
    ) -> StrategyResult:
        """
        Generate L Pattern report.
        """

        engine = LPatternEngine(pattern)

        writer = LPatternReportWriter()

        return self._run_strategy(
            input_file=input_file,
            output_file=output_file,
            timeframe=timeframe,
            engine=engine,
            writer=writer,
        )

    # -----------------------------------------------------------------

    def generate_drawdown_report(
        self,
        *,
        input_file: str | Path,
        output_file: str | Path,
        timeframe: str,
        threshold: float,
    ) -> StrategyResult:
        """
        Generate Drawdown report.
        """

        engine = DrawdownEngine(
            threshold=threshold,
        )

        writer = DrawdownReportWriter()

        return self._run_strategy(
            input_file=input_file,
            output_file=output_file,
            timeframe=timeframe,
            engine=engine,
            writer=writer,
        )

    # -----------------------------------------------------------------

    def generate_portfolio_report(
        self,
        *,
        input_file: str | Path,
        output_file: str | Path,
        timeframe: str,
        selected_strategies: list[str],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> PortfolioResult:
        """
        Generate Portfolio report.
        """

        return self._run_portfolio(
        input_file=input_file,
        output_file=output_file,
        timeframe=timeframe,
        selected_strategies=selected_strategies,
        portfolio_inputs=portfolio_inputs,
    )

    # -----------------------------------------------------------------

    def _run_strategy(
        self,
        *,
        input_file: str | Path,
        output_file: str | Path,
        timeframe: str,
        engine,
        writer,
    ) -> StrategyResult:
        """
        Common workflow used by all strategy reports.
        """

        loaded = self.loader.load(
            input_file,
        )

        result = engine.run(
            loaded.trades,
            timeframe=timeframe,
        )

        writer.write(
            result,
            output_file,
        )

        return result

    def _run_portfolio(
        self,
        *,
        input_file: str | Path,
        output_file: str | Path,
        timeframe: str,
        selected_strategies: list[str],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> PortfolioResult:
        """
        Common workflow used by Portfolio reports.
        """

        loaded = self.loader.load(
            input_file,
        )

        engine = self.portfolio_engine  
        writer = self.portfolio_writer

        result = engine.run(
            trades=loaded.trades,
            timeframe=timeframe,
            selected_strategies=selected_strategies,
            portfolio_inputs=portfolio_inputs,
        )

        writer.write(
            result,
            output_file,
        )

        return result
