"""
cycle_statistics.py

Calculates statistics for a DrawdownCycle.

The CycleDetector identifies cycle boundaries.
CycleStatistics computes all performance and risk metrics.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import replace
from itertools import accumulate

from mt5_analyzer.domain.drawdown_cycle import DrawdownCycle


class CycleStatistics:
    """
    Calculates statistics for a DrawdownCycle.
    """

    @staticmethod
    def calculate(
        cycle: DrawdownCycle,
        *,
        margin_per_trade: float = 5.0,
    ) -> DrawdownCycle:
        """
        Calculate statistics for a drawdown cycle.

        Parameters
        ----------
        cycle
            Detected drawdown cycle.

        margin_per_trade
            Margin required per open trade.

        Returns
        -------
        DrawdownCycle
            Updated immutable DrawdownCycle.
        """

        trades = list(cycle.trades)

        if not trades:
            return cycle

        # ---------------------------------------------------------
        # Trade Statistics
        # ---------------------------------------------------------

        trade_count = len(trades)

        wins = [t for t in trades if t.is_win]
        losses = [t for t in trades if t.is_loss]

        winning_trades = len(wins)
        losing_trades = len(losses)

        gross_profit = sum(t.net_profit for t in wins)
        gross_loss = sum(t.net_profit for t in losses)

        net_profit = gross_profit + gross_loss

        average_trade = (
            net_profit / trade_count
            if trade_count
            else 0.0
        )

        # ---------------------------------------------------------
        # Maximum Drawdown (within cycle)
        # ---------------------------------------------------------

        equity = list(
            accumulate(
                (
                    t.net_profit
                    for t in trades
                ),
                initial=cycle.trigger_equity,
            )
        )

        peak = equity[0]
        maximum_drawdown = 0.0

        for value in equity:

            peak = max(
                peak,
                value,
            )

            maximum_drawdown = max(
                maximum_drawdown,
                peak - value,
            )

        # ---------------------------------------------------------
        # Peak Margin
        # ---------------------------------------------------------

        peak_margin = (
            CycleStatistics._max_concurrent(
                trades
            )
            * margin_per_trade
        )

        # ---------------------------------------------------------
        # Capital Used
        # ---------------------------------------------------------

        capital_used = (
            peak_margin
            + maximum_drawdown
        )

        # ---------------------------------------------------------
        # ROE
        # ---------------------------------------------------------

        if capital_used > 0:

            roe = (
                net_profit
                / capital_used
            ) * 100.0

        else:

            roe = 0.0

        # ---------------------------------------------------------
        # Concurrent Trades
        # ---------------------------------------------------------

        concurrent = (
            CycleStatistics._max_concurrent(
                trades
            )
        )

        # ---------------------------------------------------------
        # Return updated immutable cycle
        # ---------------------------------------------------------

        return replace(

            cycle,

            trade_count=trade_count,

            winning_trades=winning_trades,

            losing_trades=losing_trades,

            gross_profit=gross_profit,

            gross_loss=gross_loss,

            net_profit=net_profit,

            average_trade=average_trade,

            maximum_drawdown=maximum_drawdown,

            peak_margin=peak_margin,

            capital_used=capital_used,

            roe=roe,

            max_concurrent_trades=concurrent,

        )

    # -------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------

    @staticmethod
    def _max_concurrent(
        trades,
    ) -> int:
        """
        Calculate maximum concurrent trades.
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
