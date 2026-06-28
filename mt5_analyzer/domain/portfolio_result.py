"""
portfolio_result.py

Domain model representing a portfolio analysis result.

A portfolio combines one or more strategy results into a single
performance report.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field

from mt5_analyzer.domain.statistics import StrategyStatistics
from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.domain.trade import Trade


@dataclass(slots=True, frozen=True)
class PortfolioResult:
    """
    Represents the result of a portfolio analysis.
    """

    # ------------------------------------------------------------------
    # Portfolio Information
    # ------------------------------------------------------------------

    portfolio_name: str

    description: str = ""

    # ------------------------------------------------------------------
    # Strategies
    # ------------------------------------------------------------------

    strategies: tuple[StrategyResult, ...] = field(
        default_factory=tuple
    )

    # ------------------------------------------------------------------
    # Combined Trades
    # ------------------------------------------------------------------

    trades: tuple[Trade, ...] = field(
        default_factory=tuple
    )

    # ------------------------------------------------------------------
    # Overall Statistics
    # ------------------------------------------------------------------

    statistics: StrategyStatistics | None = None

    # ------------------------------------------------------------------
    # Monthly / Yearly Statistics
    # ------------------------------------------------------------------

    monthly_statistics: dict[str, StrategyStatistics] = field(
        default_factory=dict
    )

    yearly_statistics: dict[int, StrategyStatistics] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def strategy_count(self) -> int:
        """
        Number of strategies in the portfolio.
        """

        return len(self.strategies)

    @property
    def trade_count(self) -> int:
        """
        Total trades in the portfolio.
        """

        return len(self.trades)

    @property
    def monthly_count(self) -> int:
        """
        Number of monthly summaries.
        """

        return len(self.monthly_statistics)

    @property
    def yearly_count(self) -> int:
        """
        Number of yearly summaries.
        """

        return len(self.yearly_statistics)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def strategy_names(self) -> list[str]:
        """
        Return strategy names.
        """

        return [
            strategy.strategy_name
            for strategy in self.strategies
        ]

    def to_dict(self) -> dict:
        """
        Convert portfolio summary to dictionary.
        """

        return {

            "Portfolio": self.portfolio_name,

            "Description": self.description,

            "Strategies": self.strategy_count,

            "Trades": self.trade_count,

            "Net Profit": (
                self.statistics.net_profit
                if self.statistics
                else 0.0
            ),

            "MDD": (
                self.statistics.max_drawdown
                if self.statistics
                else 0.0
            ),

            "Peak Margin": (
                self.statistics.peak_margin
                if self.statistics
                else 0.0
            ),

            "Capital Used": (
                self.statistics.capital_used
                if self.statistics
                else 0.0
            ),

            "%ROE": (
                self.statistics.roe
                if self.statistics
                else 0.0
            ),
        }

    def __str__(self) -> str:

        if self.statistics is None:

            return (
                f"{self.portfolio_name} "
                f"({self.strategy_count} strategies)"
            )

        return (
            f"{self.portfolio_name} | "
            f"Strategies={self.strategy_count} | "
            f"Trades={self.trade_count} | "
            f"Net={self.statistics.net_profit:.2f}"
        )
