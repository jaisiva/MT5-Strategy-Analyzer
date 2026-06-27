"""
original_engine.py

Original Strategy Engine.

This engine represents the MT5 strategy exactly as executed.
No filtering or transformation is performed.

Responsibilities
----------------
- Sort trades chronologically
- Calculate strategy statistics
- Return a StrategyResult

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from mt5_analyzer.application.statistics_engine import StatisticsEngine
from mt5_analyzer.domain.enums import PatternType
from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.domain.trade import Trade


class OriginalStrategyEngine:
    """
    Original MT5 strategy.

    Uses every trade exactly as executed.
    """

    def run(
        self,
        trades: list[Trade],
        *,
        timeframe: str,
        initial_equity: float = 100.0,
        margin_per_trade: float = 5.0,
    ) -> StrategyResult:
        """
        Analyze the original MT5 strategy.

        Parameters
        ----------
        trades
            List of Trade objects.

        timeframe
            Strategy timeframe (e.g. "5 Minute", "1 Hour").

        initial_equity
            Starting capital.

        margin_per_trade
            Margin required per open trade.

        Returns
        -------
        StrategyResult
        """

        sorted_trades = sorted(
            trades,
            key=lambda t: t.entry_time,
        )

        statistics = StatisticsEngine.calculate(
            sorted_trades,
            strategy_name="Original Strategy",
            pattern=PatternType.ORIGINAL.value,
            timeframe=timeframe,
            initial_equity=initial_equity,
            margin_per_trade=margin_per_trade,
        )

        return StrategyResult(
            strategy_name="Original Strategy",
            trades=sorted_trades,
            statistics=statistics,
        )

    @staticmethod
    def strategy_name() -> str:
        """
        Returns strategy name.
        """

        return "Original Strategy"

    @staticmethod
    def pattern() -> PatternType:
        """
        Returns associated pattern.
        """

        return PatternType.ORIGINAL
