"""
cycle_detector.py

Rolling Peak Drawdown Cycle Detector.

Detects drawdown cycles using the rolling-peak methodology.

A cycle starts when the equity drawdown percentage reaches the
configured threshold and ends when equity fully recovers to the
previous rolling peak.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from datetime import datetime

from mt5_analyzer.domain.drawdown_cycle import DrawdownCycle
from mt5_analyzer.domain.trade import Trade


class CycleDetector:
    """
    Detect rolling-peak drawdown cycles.
    """

    def detect(
        self,
        trades: list[Trade],
        threshold: float,
    ) -> list[DrawdownCycle]:
        """
        Detect drawdown cycles.

        Parameters
        ----------
        trades
            Trades sorted chronologically.

        threshold
            Drawdown percentage (10,15,20...)

        Returns
        -------
        list[DrawdownCycle]
        """

        if not trades:
            return []

        trades = sorted(
            trades,
            key=lambda t: t.entry_time,
        )

        cycles: list[DrawdownCycle] = []

        cumulative_profit = 0.0

        rolling_peak = 0.0
        rolling_peak_time = trades[0].entry_time

        cycle_number = 0

        in_cycle = False

        cycle_trades: list[Trade] = []

        trigger_equity = 0.0
        trigger_time: datetime | None = None

        peak_equity = 0.0
        peak_time: datetime | None = None

        # ----------------------------------------------------------

        for trade in trades:

            cumulative_profit += trade.net_profit

            # ------------------------------------------------------
            # Update rolling peak
            # ------------------------------------------------------

            if cumulative_profit > rolling_peak:

                rolling_peak = cumulative_profit
                rolling_peak_time = trade.exit_time

            # ------------------------------------------------------

            drawdown = rolling_peak - cumulative_profit

            if rolling_peak <= 0:

                drawdown_pct = 0.0

            else:

                drawdown_pct = (
                    drawdown
                    / rolling_peak
                ) * 100.0

            # ------------------------------------------------------
            # Cycle Start
            # ------------------------------------------------------

            if (
                not in_cycle
                and drawdown_pct >= threshold
            ):

                in_cycle = True

                cycle_trades = [trade]

                trigger_equity = cumulative_profit

                trigger_time = trade.entry_time

                peak_equity = rolling_peak

                peak_time = rolling_peak_time

                continue

            # ------------------------------------------------------
            # Continue Cycle
            # ------------------------------------------------------

            if in_cycle:

                cycle_trades.append(trade)

                # ----------------------------------------------
                # Recovery
                # ----------------------------------------------

                if cumulative_profit >= rolling_peak:

                    cycle_number += 1

                    cycles.append(

                        DrawdownCycle(

                            cycle_number=cycle_number,

                            cycle_id=f"DD{int(threshold)}-{cycle_number:04d}",

                            strategy=f"DD{int(threshold)}",

                            threshold=threshold,

                            year=trigger_time.year,

                            month=trigger_time.month,

                            peak_equity=peak_equity,

                            peak_datetime=peak_time,

                            trigger_equity=trigger_equity,

                            trigger_datetime=trigger_time,

                            recovery_equity=cumulative_profit,

                            recovery_datetime=trade.exit_time,

                            trades=tuple(cycle_trades),

                        )

                    )

                    in_cycle = False

                    cycle_trades = []

        # ----------------------------------------------------------
        # Unrecovered Cycle
        # ----------------------------------------------------------

        if in_cycle:

            cycle_number += 1

            last_trade = cycle_trades[-1]

            cycles.append(

                DrawdownCycle(

                    cycle_number=cycle_number,

                    cycle_id=f"DD{int(threshold)}-{cycle_number:04d}",

                    strategy=f"DD{int(threshold)}",

                    threshold=threshold,

                    year=trigger_time.year,

                    month=trigger_time.month,

                    peak_equity=peak_equity,

                    peak_datetime=peak_time,

                    trigger_equity=trigger_equity,

                    trigger_datetime=trigger_time,

                    recovery_equity=cumulative_profit,

                    recovery_datetime=None,

                    trades=tuple(cycle_trades),

                )

            )

        return cycles
