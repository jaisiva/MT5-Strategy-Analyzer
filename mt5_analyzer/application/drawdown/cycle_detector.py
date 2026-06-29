"""
cycle_detector.py

Peak-to-Recovery Drawdown Cycle Detector.

Implements the Peak→Recovery rolling drawdown strategy.

Business Rules
--------------

A rolling peak is maintained while scanning trades
chronologically.

Whenever cumulative equity declines by the configured
percentage from the rolling peak:

    Peak
      │
      ▼
    Remember Peak
      │
      ▼
    Threshold Breached
      │
      ▼
Cycle starts FROM Peak Trade
      │
      ▼
Continue collecting trades
      │
      ▼
Recover previous peak
      │
      ▼
Close cycle

Unlike the previous implementation, the cycle starts
at the trade that created the rolling peak instead of
the threshold breach trade.

Characteristics
---------------

* O(n) single pass
* Non-overlapping cycles
* Rolling peak methodology
* Supports DD10/DD15/DD20/DD25/DD30

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
    Detect rolling Peak→Recovery drawdown cycles.
    """

    # ---------------------------------------------------------

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
            Drawdown percentage.

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

        rolling_peak_equity = 0.0

        rolling_peak_index = 0

        rolling_peak_time = trades[0].entry_time

        in_cycle = False

        cycle_number = 0

        cycle_start_index = 0

        peak_equity = 0.0

        peak_time: datetime | None = None

        trigger_equity = 0.0

        trigger_time: datetime | None = None

        # -----------------------------------------------------
        # Scan trades
        # -----------------------------------------------------

        for index, trade in enumerate(trades):

            cumulative_profit += trade.net_profit

            # ---------------------------------------------
            # Update rolling peak ONLY when not inside
            # an active drawdown cycle.
            # ---------------------------------------------

            if (
                not in_cycle
                and cumulative_profit > rolling_peak_equity
            ):

                rolling_peak_equity = cumulative_profit

                rolling_peak_index = index

                rolling_peak_time = trade.exit_time

            # ---------------------------------------------
            # Current drawdown
            # ---------------------------------------------

            drawdown = (

                rolling_peak_equity

                - cumulative_profit

            )

            if rolling_peak_equity <= 0:

                drawdown_pct = 0.0

            else:

                drawdown_pct = (

                    drawdown

                    / rolling_peak_equity

                ) * 100.0

            # ---------------------------------------------
            # Start drawdown cycle
            # ---------------------------------------------

            if (

                not in_cycle

                and drawdown_pct >= threshold

            ):

                in_cycle = True

                cycle_start_index = rolling_peak_index

                peak_equity = rolling_peak_equity

                peak_time = rolling_peak_time

                trigger_equity = cumulative_profit

                trigger_time = trade.entry_time

                #
                # Continue scanning.
                #
                # Trades will be collected from
                # cycle_start_index after recovery.
                #

                continue
				
			# ---------------------------------------------
            # Continue active drawdown cycle
            # ---------------------------------------------

            if not in_cycle:

                continue

            # ---------------------------------------------
            # Recovery?
            #
            # Recovery occurs when cumulative equity
            # reaches (or exceeds) the previous
            # rolling peak.
            # ---------------------------------------------

            if cumulative_profit < peak_equity:

                continue

            # ---------------------------------------------
            # Drawdown recovered
            # ---------------------------------------------

            cycle_number += 1

            cycle_trades = trades[
                cycle_start_index : index + 1
            ]

            cycles.append(

                DrawdownCycle(

                    cycle_number=cycle_number,

                    cycle_id=(
                        f"DD{int(threshold)}"
                        f"-{cycle_number:04d}"
                    ),

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

            # ---------------------------------------------
            # Reset detector
            #
            # Current trade becomes the beginning
            # of the next rolling-peak search.
            # ---------------------------------------------

            in_cycle = False

            rolling_peak_equity = cumulative_profit

            rolling_peak_index = index

            rolling_peak_time = trade.exit_time

            cycle_start_index = 0

            peak_equity = 0.0

            peak_time = None

            trigger_equity = 0.0

            trigger_time = None

        # -------------------------------------------------
        # End of trade scan
        #
        # If still inside a drawdown cycle,
        # create an unrecovered cycle.
        # -------------------------------------------------

        if not in_cycle:

            return cycles

        cycle_number += 1

        cycle_trades = trades[
            cycle_start_index :
        ]

        last_trade = cycle_trades[-1]
	
	    # -------------------------------------------------
        # Unrecovered cycle
        # -------------------------------------------------

        cycles.append(

            DrawdownCycle(

                cycle_number=cycle_number,

                cycle_id=(
                    f"DD{int(threshold)}"
                    f"-{cycle_number:04d}"
                ),

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

        # -------------------------------------------------
        # Return completed + unrecovered cycles
        # -------------------------------------------------

        return cycles
