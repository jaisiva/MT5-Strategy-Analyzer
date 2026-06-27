"""
statistics_engine.py

Core statistics engine for MT5 Strategy Analyzer.

Computes all performance metrics from a collection of Trade objects.

Every strategy engine (Original, L Pattern, DD, Portfolio) delegates
performance calculations to this module.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from itertools import accumulate

from mt5_analyzer.domain.statistics import StrategyStatistics
from mt5_analyzer.domain.trade import Trade


class StatisticsEngine:
    """
    Calculates strategy statistics.
    """

    @staticmethod
    def calculate(
        trades: list[Trade],
        *,
        strategy_name: str,
        pattern: str = "Original",
        timeframe: str = "",
        initial_equity: float = 100.0,
        margin_per_trade: float = 5.0,
    ) -> StrategyStatistics:
        """
        Calculate strategy statistics.
        """

        if not trades:

            return StrategyStatistics(
                strategy_name=strategy_name,
                pattern=pattern,
                timeframe=timeframe,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
            )

        # ---------------------------------------------------------
        # Basic statistics
        # ---------------------------------------------------------

        total = len(trades)

        wins = [t for t in trades if t.is_win]
        losses = [t for t in trades if t.is_loss]

        gross_profit = sum(t.net_profit for t in wins)
        gross_loss = sum(t.net_profit for t in losses)

        net_profit = gross_profit + gross_loss

        average_trade = net_profit / total

        largest_win = max((t.net_profit for t in wins), default=0.0)

        largest_loss = min((t.net_profit for t in losses), default=0.0)

        profit_factor = (
            gross_profit / abs(gross_loss)
            if gross_loss != 0
            else 0.0
        )

        expectancy = average_trade

        # ---------------------------------------------------------
        # Holding time
        # ---------------------------------------------------------

        holding = [t.holding_minutes for t in trades]

        avg_hold = sum(holding) / len(holding)

        longest_hold = max(holding)

        shortest_hold = min(holding)

        # ---------------------------------------------------------
        # Equity Curve
        # ---------------------------------------------------------

        equity_curve = [
            initial_equity + x
            for x in accumulate(
                t.net_profit for t in trades
            )
        ]

        peak_equity = max(equity_curve)

        ending_equity = equity_curve[-1]

        # ---------------------------------------------------------
        # Maximum Drawdown
        # ---------------------------------------------------------

        peak = initial_equity

        max_dd = 0.0

        for equity in equity_curve:

            peak = max(peak, equity)

            drawdown = peak - equity

            max_dd = max(max_dd, drawdown)

        # ---------------------------------------------------------
        # Margin
        # ---------------------------------------------------------

        concurrent = StatisticsEngine._max_concurrent(
            trades
        )

        peak_margin = (
            concurrent
            * margin_per_trade
        )

        capital_used = peak_margin + max_dd

        roe = (
            (net_profit / capital_used) * 100
            if capital_used > 0
            else 0.0
        )

        recovery = (
            net_profit / max_dd
            if max_dd > 0
            else 0.0
        )

        return_to_dd = recovery

        # ---------------------------------------------------------
        # Result
        # ---------------------------------------------------------

        return StrategyStatistics(

            strategy_name=strategy_name,

            pattern=pattern,

            timeframe=timeframe,

            total_trades=total,

            winning_trades=len(wins),

            losing_trades=len(losses),

            gross_profit=gross_profit,

            gross_loss=gross_loss,

            net_profit=net_profit,

            average_trade=average_trade,

            largest_win=largest_win,

            largest_loss=largest_loss,

            profit_factor=profit_factor,

            expectancy=expectancy,

            max_drawdown=max_dd,

            peak_equity=peak_equity,

            ending_equity=ending_equity,

            peak_margin=peak_margin,

            capital_used=capital_used,

            roe=roe,

            recovery_factor=recovery,

            return_to_drawdown=return_to_dd,

            average_holding_minutes=avg_hold,

            longest_holding_minutes=longest_hold,

            shortest_holding_minutes=shortest_hold,

            max_concurrent_trades=concurrent,
        )

    @staticmethod
    def _max_concurrent(
        trades: list[Trade],
    ) -> int:
        """
        Compute maximum concurrent open trades.
        """

        events = []

        for trade in trades:

            events.append(
                (
                    trade.entry_time,
                    1,
                )
            )

            events.append(
                (
                    trade.exit_time,
                    -1,
                )
            )

        events.sort()

        current = 0

        maximum = 0

        for _, delta in events:

            current += delta

            maximum = max(
                maximum,
                current,
            )

        return maximum
