"""
portfolio_engine.py

Portfolio Engine.

Combines one or more StrategyResult objects into a single portfolio.

Responsibilities
----------------
- Merge trades
- Sort trades
- Calculate portfolio statistics
- Build monthly summaries
- Build yearly summaries
- Return PortfolioResult

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from collections import defaultdict

from mt5_analyzer.application.statistics_engine import StatisticsEngine
from mt5_analyzer.domain.portfolio_result import PortfolioResult
from mt5_analyzer.domain.statistics import StrategyStatistics
from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.domain.trade import Trade


class PortfolioEngine:
    """
    Portfolio Analysis Engine.
    """

    def build(
        self,
        *,
        portfolio_name: str,
        strategies: list[StrategyResult],
        description: str = "",
        initial_equity: float = 100.0,
        margin_per_trade: float = 5.0,
    ) -> PortfolioResult:
        """
        Build a portfolio from multiple strategies.
        """

        if not strategies:

            return PortfolioResult(
                portfolio_name=portfolio_name,
                description=description,
            )

        # ----------------------------------------------------------
        # Merge Trades
        # ----------------------------------------------------------

        trades: list[Trade] = []

        for strategy in strategies:

            trades.extend(strategy.trades)

        trades.sort(
            key=lambda trade: trade.entry_time
        )

        # ----------------------------------------------------------
        # Overall Statistics
        # ----------------------------------------------------------

        statistics = StatisticsEngine.calculate(
            trades,
            strategy_name=portfolio_name,
            pattern="Portfolio",
            timeframe="Portfolio",
            initial_equity=initial_equity,
            margin_per_trade=margin_per_trade,
        )

        # ----------------------------------------------------------
        # Monthly Statistics
        # ----------------------------------------------------------

        monthly_statistics = self._monthly_statistics(
            trades,
            initial_equity,
            margin_per_trade,
        )

        # ----------------------------------------------------------
        # Yearly Statistics
        # ----------------------------------------------------------

        yearly_statistics = self._yearly_statistics(
            trades,
            initial_equity,
            margin_per_trade,
        )

        # ----------------------------------------------------------
        # Portfolio Result
        # ----------------------------------------------------------

        return PortfolioResult(

            portfolio_name=portfolio_name,

            description=description,

            strategies=tuple(strategies),

            trades=tuple(trades),

            statistics=statistics,

            monthly_statistics=monthly_statistics,

            yearly_statistics=yearly_statistics,
        )

    # --------------------------------------------------------------

    def _monthly_statistics(
        self,
        trades: list[Trade],
        initial_equity: float,
        margin_per_trade: float,
    ) -> dict[str, StrategyStatistics]:
        """
        Build month-wise statistics.
        """

        groups: dict[str, list[Trade]] = defaultdict(list)

        for trade in trades:

            key = trade.entry_time.strftime("%Y-%m")

            groups[key].append(trade)

        results = {}

        for key in sorted(groups):

            results[key] = StatisticsEngine.calculate(

                groups[key],

                strategy_name=key,

                pattern="Portfolio",

                timeframe="Monthly",

                initial_equity=initial_equity,

                margin_per_trade=margin_per_trade,

            )

        return results

    # --------------------------------------------------------------

    def _yearly_statistics(
        self,
        trades: list[Trade],
        initial_equity: float,
        margin_per_trade: float,
    ) -> dict[int, StrategyStatistics]:
        """
        Build year-wise statistics.
        """

        groups: dict[int, list[Trade]] = defaultdict(list)

        for trade in trades:

            groups[
                trade.entry_time.year
            ].append(trade)

        results = {}

        for year in sorted(groups):

            results[year] = StatisticsEngine.calculate(

                groups[year],

                strategy_name=str(year),

                pattern="Portfolio",

                timeframe="Yearly",

                initial_equity=initial_equity,

                margin_per_trade=margin_per_trade,

            )

        return results
