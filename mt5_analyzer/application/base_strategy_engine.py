"""
base_strategy_engine.py

Base class for all strategy engines.

Implements the common workflow used by every strategy:

    Input Trades
         │
         ▼
    Select Trades
         │
         ▼
    Sort Trades
         │
         ▼
    Statistics Engine
         │
         ▼
    StrategyResult

Derived classes only implement trade selection.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from mt5_analyzer.application.statistics_engine import StatisticsEngine
from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.domain.trade import Trade


class BaseStrategyEngine(ABC):
    """
    Abstract base class for all strategy engines.
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
        Execute the strategy.

        This method implements the common strategy workflow.
        """

        selected_trades = self.select_trades(trades)

        selected_trades.sort(
            key=lambda trade: trade.entry_time
        )

        statistics = StatisticsEngine.calculate(
            selected_trades,
            strategy_name=self.strategy_name(),
            pattern=self.pattern_name(),
            timeframe=timeframe,
            initial_equity=initial_equity,
            margin_per_trade=margin_per_trade,
        )

        return StrategyResult(
            strategy_name=self.strategy_name(),
            trades=selected_trades,
            statistics=statistics,
        )

    @abstractmethod
    def select_trades(
        self,
        trades: list[Trade],
    ) -> list[Trade]:
        """
        Return trades used by this strategy.
        """

    @abstractmethod
    def strategy_name(self) -> str:
        """
        Human-readable strategy name.
        """

    @abstractmethod
    def pattern_name(self) -> str:
        """
        Pattern name for reporting.
        """
