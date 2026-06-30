"""
portfolio_statistics_engine.py

Portfolio Statistics Engine.

This module is responsible for calculating consolidated portfolio
statistics from one or more StrategyResult objects.

The Portfolio Statistics Engine is the ONLY component responsible for
calculating portfolio-level metrics.

Responsibilities
----------------

• Portfolio Trade Count
• Portfolio Wins
• Portfolio Losses
• Portfolio Net Profit
• Portfolio Average Profit
• Strategy Peak Margin
• Portfolio Peak Margin
• Portfolio Maximum Drawdown (MDD)
• Portfolio Capital
• Portfolio Return on Equity (ROE)
• Monthly Portfolio Statistics
• Yearly Portfolio Statistics

Portfolio Capital Formula
-------------------------

Portfolio Capital =
    Portfolio Peak Margin
    +
    Portfolio Maximum Drawdown

Portfolio ROE Formula
---------------------

Portfolio ROE =
    Portfolio Net Profit
    /
    Portfolio Capital
    × 100

Author
------
MT5 Strategy Analyzer

License
-------
MIT
"""

from __future__ import annotations

from collections import defaultdict

from mt5_analyzer.domain.portfolio_input import PortfolioInput
from mt5_analyzer.domain.portfolio_statistics import PortfolioStatistics
from mt5_analyzer.domain.portfolio_trade import PortfolioTrade
from mt5_analyzer.domain.strategy_result import StrategyResult


class PortfolioStatisticsEngine:
    """
    Portfolio statistics calculator.

    This class consolidates statistics from multiple strategies into
    a single PortfolioStatistics object.

    Notes
    -----

    • Trades are NOT deduplicated.

    • The same MT5 trade may legitimately appear in multiple
      strategies.

    • Each strategy is considered an independent virtual trading
      system.

    • Portfolio metrics are calculated using the combined strategy
      results.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def calculate(
        self,
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> PortfolioStatistics:
        """
        Calculate portfolio statistics.

        Parameters
        ----------
        strategy_results

            Results returned from strategy engines.

        portfolio_inputs

            Global configuration supplied for each strategy.

        Returns
        -------
        PortfolioStatistics
        """

        statistics = PortfolioStatistics()

        if not strategy_results:

            return statistics

        #
        # Build consolidated portfolio trade list.
        #
        portfolio_trades = self._build_portfolio_trades(
            strategy_results
        )

        #
        # Basic portfolio statistics.
        #
        statistics.trade_count = len(portfolio_trades)

        statistics.wins = self._calculate_wins(
            portfolio_trades
        )

        statistics.losses = self._calculate_losses(
            portfolio_trades
        )

        statistics.net_profit = self._calculate_net_profit(
            portfolio_trades
        )

        statistics.average_profit = (
            self._calculate_average_profit(
                portfolio_trades
            )
        )

        #
        # Risk statistics.
        #
        statistics.peak_margin = (
            self._calculate_peak_margin(
                strategy_results,
                portfolio_inputs,
            )
        )

        #
        # Remaining calculations are performed
        # in the following sections.
        #
        return self._complete_statistics(
            statistics,
            portfolio_trades,
            strategy_results,
            portfolio_inputs,
        )

    # ---------------------------------------------------------
    # Portfolio construction
    # ---------------------------------------------------------

    def _build_portfolio_trades(
        self,
        strategy_results: list[StrategyResult],
    ) -> list[PortfolioTrade]:
        """
        Build consolidated portfolio trades.

        Trades are NOT deduplicated.

        If Original, L and DD10 all select Trade #120,
        then three PortfolioTrade objects are created.

        Returns
        -------
        list[PortfolioTrade]
        """

        portfolio_trades: list[PortfolioTrade] = []

        for result in strategy_results:

            strategy_name = result.strategy_name

            for trade in result.trades:

                portfolio_trades.append(

                    PortfolioTrade(

                        strategy=strategy_name,

                        trade=trade,

                    )

                )

        portfolio_trades.sort(

            key=lambda t: t.trade.entry_time

        )

        return portfolio_trades
		
    # ---------------------------------------------------------
    # Basic Portfolio Statistics
    # ---------------------------------------------------------

    def _calculate_wins(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> int:
        """
        Calculate portfolio wins.
        """

        return sum(

            1

            for portfolio_trade in portfolio_trades

            if portfolio_trade.trade.is_win

        )

    # ---------------------------------------------------------

    def _calculate_losses(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> int:
        """
        Calculate portfolio losses.
        """

        return sum(

            1

            for portfolio_trade in portfolio_trades

            if portfolio_trade.trade.is_loss

        )

    # ---------------------------------------------------------

    def _calculate_net_profit(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> float:
        """
        Calculate portfolio net profit.
        """

        return sum(

            portfolio_trade.trade.net_profit

            for portfolio_trade in portfolio_trades

        )

    # ---------------------------------------------------------

    def _calculate_average_profit(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> float:
        """
        Average profit per portfolio trade.
        """

        if not portfolio_trades:

            return 0.0

        return (

            self._calculate_net_profit(
                portfolio_trades
            )

            / len(portfolio_trades)

        )

    # ---------------------------------------------------------
    # Margin Calculations
    # ---------------------------------------------------------

    def _calculate_peak_margin(
        self,
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> float:
        """
        Calculate Portfolio Peak Margin.

        Portfolio Peak Margin is defined as the sum of
        each strategy's peak margin requirement.
        """

        portfolio_peak_margin = 0.0

        for result in strategy_results:

            strategy_name = result.strategy_name

            portfolio_input = portfolio_inputs.get(
                strategy_name
            )

            if portfolio_input is None:

                continue

            portfolio_peak_margin += (

                self._calculate_strategy_peak_margin(

                    result,

                    portfolio_input,

                )

            )

        return portfolio_peak_margin

    # ---------------------------------------------------------

    def _calculate_strategy_peak_margin(
        self,
        strategy_result: StrategyResult,
        portfolio_input: PortfolioInput,
    ) -> float:
        """
        Calculate Peak Margin for one strategy.

        Current implementation assumes one trade
        consumes one unit of margin.

        Future versions may calculate concurrent
        open positions instead.
        """

        trade_count = len(

            strategy_result.trades

        )

        if trade_count == 0:

            return 0.0

        #
        # Current implementation.
        #
        # Peak Margin =
        #
        # Maximum Open Trades
        # × Margin Per Trade
        #
        # Until concurrent position tracking
        # is implemented,
        # Maximum Open Trades = 1.
        #

        max_open_positions = 1

        return (

            max_open_positions

            * portfolio_input.margin_per_trade

        )

    # ---------------------------------------------------------
    # Remaining calculations
    # ---------------------------------------------------------

    def _complete_statistics(
        self,
        statistics: PortfolioStatistics,
        portfolio_trades: list[PortfolioTrade],
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> PortfolioStatistics:
        """
        Complete portfolio calculations.

        Remaining calculations:

        • Portfolio MDD
        • Portfolio Capital
        • Portfolio ROE
        • Monthly Statistics
        • Yearly Statistics
        """

        #
        # Implemented in Part-3.
        #

        return statistics

    # ---------------------------------------------------------
    # Portfolio Risk Statistics
    # ---------------------------------------------------------

    def _complete_statistics(
        self,
        statistics: PortfolioStatistics,
        portfolio_trades: list[PortfolioTrade],
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> PortfolioStatistics:
        """
        Complete remaining portfolio calculations.
        """

        #
        # Portfolio Maximum Drawdown
        #
        statistics.maximum_drawdown = (
            self._calculate_portfolio_mdd(
                portfolio_trades
            )
        )

        #
        # Portfolio Capital
        #
        statistics.capital = (
            statistics.peak_margin
            +
            statistics.maximum_drawdown
        )

        #
        # Portfolio ROE
        #
        statistics.return_on_equity = (
            self._calculate_portfolio_roe(
                statistics.net_profit,
                statistics.capital,
            )
        )

        return statistics

    # ---------------------------------------------------------

    def _calculate_portfolio_mdd(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> float:
        """
        Calculate Portfolio Maximum Drawdown.

        Uses rolling Peak→Recovery methodology.
        """

        if not portfolio_trades:

            return 0.0

        cumulative_profit = 0.0

        rolling_peak = 0.0

        maximum_drawdown = 0.0

        for portfolio_trade in portfolio_trades:

            cumulative_profit += (

                portfolio_trade.trade.net_profit

            )

            if cumulative_profit > rolling_peak:

                rolling_peak = cumulative_profit

            drawdown = (

                rolling_peak

                - cumulative_profit

            )

            if drawdown > maximum_drawdown:

                maximum_drawdown = drawdown

        return maximum_drawdown

    # ---------------------------------------------------------

    def _calculate_portfolio_roe(
        self,
        net_profit: float,
        capital: float,
    ) -> float:
        """
        Portfolio Return on Equity.
        """

        if capital <= 0:

            return 0.0

        return (

            net_profit

            / capital

        ) * 100.0

    # ---------------------------------------------------------
    # Monthly / Yearly Aggregation
    # ---------------------------------------------------------

    def calculate_monthly_statistics(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> dict[tuple[int, int], PortfolioStatistics]:
        """
        Calculate monthly portfolio statistics.

        Key

            (Year, Month)
        """

        monthly: dict[
            tuple[int, int],
            list[PortfolioTrade],
        ] = defaultdict(list)

        for portfolio_trade in portfolio_trades:

            dt = portfolio_trade.trade.entry_time

            monthly[(dt.year, dt.month)].append(

                portfolio_trade

            )

        monthly_statistics: dict[
            tuple[int, int],
            PortfolioStatistics,
        ] = {}

        for key, trades in monthly.items():

            statistics = PortfolioStatistics()

            statistics.trade_count = len(trades)

            statistics.wins = self._calculate_wins(trades)

            statistics.losses = self._calculate_losses(trades)

            statistics.net_profit = (

                self._calculate_net_profit(trades)

            )

            statistics.average_profit = (

                self._calculate_average_profit(trades)

            )

            statistics.maximum_drawdown = (

                self._calculate_portfolio_mdd(trades)

            )

            monthly_statistics[key] = statistics

        return monthly_statistics

    # ---------------------------------------------------------

    def calculate_yearly_statistics(
        self,
        portfolio_trades: list[PortfolioTrade],
    ) -> dict[int, PortfolioStatistics]:
        """
        Calculate yearly portfolio statistics.
        """

        yearly: dict[
            int,
            list[PortfolioTrade],
        ] = defaultdict(list)

        for portfolio_trade in portfolio_trades:

            yearly[
                portfolio_trade.trade.entry_time.year
            ].append(portfolio_trade)

        yearly_statistics: dict[
            int,
            PortfolioStatistics,
        ] = {}

        for year, trades in yearly.items():

            statistics = PortfolioStatistics()

            statistics.trade_count = len(trades)

            statistics.wins = self._calculate_wins(trades)

            statistics.losses = self._calculate_losses(trades)

            statistics.net_profit = (

                self._calculate_net_profit(trades)

            )

            statistics.average_profit = (

                self._calculate_average_profit(trades)

            )

            statistics.maximum_drawdown = (

                self._calculate_portfolio_mdd(trades)

            )

            yearly_statistics[year] = statistics

        return yearly_statistics

    # ---------------------------------------------------------
    # Monthly / Yearly Completion
    # ---------------------------------------------------------

    def complete_monthly_statistics(
        self,
        monthly_statistics: dict[
            tuple[int, int],
            PortfolioStatistics,
        ],
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> None:
        """
        Complete monthly portfolio statistics.

        Calculates:

        • Peak Margin
        • Portfolio Capital
        • Portfolio ROE
        """

        peak_margin = self._calculate_peak_margin(
            strategy_results,
            portfolio_inputs,
        )

        for statistics in monthly_statistics.values():

            statistics.peak_margin = peak_margin

            statistics.capital = (

                statistics.peak_margin

                +

                statistics.maximum_drawdown

            )

            statistics.return_on_equity = (

                self._calculate_portfolio_roe(

                    statistics.net_profit,

                    statistics.capital,

                )

            )

    # ---------------------------------------------------------

    def complete_yearly_statistics(
        self,
        yearly_statistics: dict[
            int,
            PortfolioStatistics,
        ],
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> None:
        """
        Complete yearly portfolio statistics.
        """

        peak_margin = self._calculate_peak_margin(

            strategy_results,

            portfolio_inputs,

        )

        for statistics in yearly_statistics.values():

            statistics.peak_margin = peak_margin

            statistics.capital = (

                statistics.peak_margin

                +

                statistics.maximum_drawdown

            )

            statistics.return_on_equity = (

                self._calculate_portfolio_roe(

                    statistics.net_profit,

                    statistics.capital,

                )

            )

    # ---------------------------------------------------------

    def validate(
        self,
        statistics: PortfolioStatistics,
    ) -> None:
        """
        Validate calculated portfolio statistics.
        """

        if statistics.trade_count < 0:

            raise ValueError(

                "Trade count cannot be negative."

            )

        if statistics.wins < 0:

            raise ValueError(

                "Wins cannot be negative."

            )

        if statistics.losses < 0:

            raise ValueError(

                "Losses cannot be negative."

            )

        if statistics.peak_margin < 0:

            raise ValueError(

                "Peak margin cannot be negative."

            )

        if statistics.maximum_drawdown < 0:

            raise ValueError(

                "Maximum drawdown cannot be negative."

            )

        if statistics.capital < 0:

            raise ValueError(

                "Portfolio capital cannot be negative."

            )

    # ---------------------------------------------------------

    def calculate_complete_statistics(
        self,
        strategy_results: list[StrategyResult],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> PortfolioStatistics:
        """
        High-level convenience API.

        This method is intended to be used by
        PortfolioEngine.
        """

        statistics = self.calculate(

            strategy_results,

            portfolio_inputs,

        )

        self.validate(

            statistics,

        )

        return statistics
