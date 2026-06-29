"""
lpattern_engine.py

L Pattern Strategy Engine.

Implements non-overlapping L Pattern strategies.

Business Rules
--------------

Each pattern strategy is evaluated independently.

L
    Look for 1 consecutive losing trade.
    Select the immediately following trade.
    Restart scanning after the selected trade.

LL
    Look for 2 consecutive losing trades.
    Select the immediately following trade.
    Restart scanning after the selected trade.

LLL
    Look for 3 consecutive losing trades.
    Select the immediately following trade.
    Restart scanning after the selected trade.

LLLL
    Look for 4 consecutive losing trades.
    Select the immediately following trade.
    Restart scanning after the selected trade.

LLLLL
    Look for 5 consecutive losing trades.
    Select the immediately following trade.
    Restart scanning after the selected trade.

ALL_L
    Executes every individual strategy independently and
    returns the union of all selected trades.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import replace

from mt5_analyzer.application.base_strategy_engine import BaseStrategyEngine
from mt5_analyzer.domain.enums import PatternType
from mt5_analyzer.domain.trade import Trade


class LPatternEngine(BaseStrategyEngine):

    def __init__(
        self,
        pattern: PatternType,
    ) -> None:

        supported = (
            PatternType.L,
            PatternType.LL,
            PatternType.LLL,
            PatternType.LLLL,
            PatternType.LLLLL,
            PatternType.ALL_L,
        )

        if pattern not in supported:

            raise ValueError(
                f"Unsupported pattern: {pattern}"
            )

        self._pattern = pattern

    # -------------------------------------------------------------

    def strategy_name(self) -> str:

        return f"{self._pattern.value} Pattern Strategy"

    # -------------------------------------------------------------

    def pattern_name(self) -> str:

        return self._pattern.value

    # -------------------------------------------------------------

    def select_trades(
        self,
        trades: list[Trade],
    ) -> list[Trade]:

        if self._pattern is PatternType.ALL_L:

            return self._extract_all_patterns(
                trades
            )

        pattern_length = len(
            self._pattern.value
        )

        return self._scan_pattern(
            trades,
            pattern_length,
            self._pattern,
        )

    # -------------------------------------------------------------
    # Generic Scanner
    # -------------------------------------------------------------

    def _scan_pattern(
        self,
        trades: list[Trade],
        losses_required: int,
        pattern: PatternType,
    ) -> list[Trade]:

        selected: list[Trade] = []

        i = 0

        n = len(trades)

        while i < n:

            # Need enough trades remaining
            if i + losses_required >= n:

                break

            matched = True

            # Verify consecutive losses
            for j in range(losses_required):

                if not trades[i + j].is_loss:

                    matched = False
                    break

            if matched:

                selected_trade = trades[
                    i + losses_required
                ]

                selected.append(

                    replace(
                        selected_trade,
                        pattern=pattern,
                    )

                )

                #
                # Non-overlapping
                #
                i = i + losses_required + 1

            else:

                i += 1

        return selected

    # -------------------------------------------------------------

    def _extract_all_patterns(
        self,
        trades: list[Trade],
    ) -> list[Trade]:

        selected: list[Trade] = []

        seen: set[int] = set()

        patterns = [

            (1, PatternType.L),

            (2, PatternType.LL),

            (3, PatternType.LLL),

            (4, PatternType.LLLL),

            (5, PatternType.LLLLL),

        ]

        for losses, pattern in patterns:

            matches = self._scan_pattern(
                trades,
                losses,
                pattern,
            )

            for trade in matches:

                #
                # Prevent duplicate trade selection
                #
                if trade.ticket in seen:

                    continue

                seen.add(
                    trade.ticket
                )

                selected.append(
                    trade
                )

        #
        # Preserve chronological order
        #
        selected.sort(
            key=lambda t: t.entry_time
        )

        return selected
