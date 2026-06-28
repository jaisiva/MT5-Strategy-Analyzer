"""
drawdown_engine.py

Drawdown Strategy Engine.

Implements the rolling-peak drawdown strategy.

Workflow

    Trades
        │
        ▼
    CycleDetector
        │
        ▼
    DrawdownCycle
        │
        ▼
    CycleStatistics
        │
        ▼
    Merge Trades
        │
        ▼
    StatisticsEngine
        │
        ▼
    StrategyResult

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from mt5_analyzer.application.base_strategy_engine import BaseStrategyEngine
from mt5_analyzer.application.drawdown.cycle_detector import CycleDetector
from mt5_analyzer.application.drawdown.cycle_statistics import CycleStatistics
from mt5_analyzer.application.statistics_engine import StatisticsEngine
from mt5_analyzer.domain.drawdown_cycle import DrawdownCycle
from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.domain.trade import Trade


class DrawdownEngine(BaseStrategyEngine):
    """
    Rolling Peak Drawdown Strategy.
    """

    def __init__(
        self,
        threshold: float,
    ) -> None:

        self._threshold = threshold

        self._cycles: list[DrawdownCycle] = []

    # -------------------------------------------------------------

    def strategy_name(self) -> str:

        return f"DD{int(self._threshold)} Strategy"

    # -------------------------------------------------------------

    def pattern_name(self) -> str:

        return f"DD{int(self._threshold)}"

    # -------------------------------------------------------------

    @property
    def cycles(self) -> list[DrawdownCycle]:

        return self._cycles

    # -------------------------------------------------------------

    def run(
        self,
        trades: list[Trade],
        *,
        timeframe: str,
        initial_equity: float = 100.0,
        margin_per_trade: float = 5.0,
    ) -> StrategyResult:
        """
        Execute drawdown strategy.
        """

        detector = CycleDetector()

        calculator = CycleStatistics()

        # ---------------------------------------------------------
        # Detect cycles
        # ---------------------------------------------------------

        cycles = detector.detect(
            trades,
            threshold=self._threshold,
        )

        completed_cycles: list[DrawdownCycle] = []

        selected_trades: list[Trade] = []

        # ---------------------------------------------------------
        # Calculate cycle statistics
        # ---------------------------------------------------------

        for cycle in cycles:

            completed = calculator.calculate(
                cycle,
                margin_per_trade=margin_per_trade,
            )

            completed_cycles.append(
                completed
            )

            selected_trades.extend(
                completed.trades
            )

        selected_trades.sort(
            key=lambda trade: trade.entry_time
        )

        # ---------------------------------------------------------
        # Overall statistics
        # ---------------------------------------------------------

        statistics = StatisticsEngine.calculate(

            selected_trades,

            strategy_name=self.strategy_name(),

            pattern=self.pattern_name(),

            timeframe=timeframe,

            initial_equity=initial_equity,

            margin_per_trade=margin_per_trade,

        )

        self._cycles = completed_cycles

        # ---------------------------------------------------------
        # Result
        # ---------------------------------------------------------

        return StrategyResult(

            strategy_name=self.strategy_name(),

            trades=selected_trades,

            statistics=statistics,

            cycles=completed_cycles,

        )

    # -------------------------------------------------------------

    def select_trades(
        self,
        trades: list[Trade],
    ) -> list[Trade]:
        """
        Required by BaseStrategyEngine.

        DrawdownEngine overrides run(), therefore this method
        is not used.
        """

        return trades
