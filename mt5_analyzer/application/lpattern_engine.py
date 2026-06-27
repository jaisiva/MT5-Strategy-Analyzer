"""
lpattern_engine.py

L Pattern Strategy Engine.

Implements the non-overlapping L Pattern strategy.

Supported patterns

    Original
    L
    LL
    LLL
    LLLL
    LLLLL
    ALL_L

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
    """
    L Pattern strategy engine.

    Non-overlapping implementation.
    """

    def __init__(
        self,
        pattern: PatternType,
    ) -> None:

        if pattern not in (
            PatternType.L,
            PatternType.LL,
            PatternType.LLL,
            PatternType.LLLL,
            PatternType.LLLLL,
            PatternType.ALL_L,
        ):
            raise ValueError(
                f"Unsupported L Pattern: {pattern}"
            )

        self._pattern = pattern

    def strategy_name(self) -> str:
        """
        Strategy name.
        """

        return f"{self._pattern.value} Pattern Strategy"

    def pattern_name(self) -> str:
        """
        Pattern name.
        """

        return self._pattern.value

    def select_trades(
        self,
        trades: list[Trade],
    ) -> list[Trade]:
        """
        Extract trades for requested L Pattern.
        """

        if self._pattern is PatternType.ALL_L:

            return self._extract_all_l(
                trades
            )

        length = len(
            self._pattern.value
        )

        return self._extract_pattern(
            trades,
            length,
        )

    # ------------------------------------------------------------
    # Pattern Extraction
    # ------------------------------------------------------------

    def _extract_pattern(
        self,
        trades: list[Trade],
        pattern_length: int,
    ) -> list[Trade]:

        selected: list[Trade] = []

        losses = 0

        for trade in trades:

            if trade.is_loss:

                losses += 1

                continue

            # Winning trade

            if losses == pattern_length:

                selected.append(
                    replace(
                        trade,
                        pattern=self._pattern,
                    )
                )

            losses = 0

        return selected

    # ------------------------------------------------------------

    def _extract_all_l(
        self,
        trades: list[Trade],
    ) -> list[Trade]:

        selected: list[Trade] = []

        losses = 0

        for trade in trades:

            if trade.is_loss:

                losses += 1

                continue

            if losses > 0:

                pattern = PatternType(
                    "L" * min(
                        losses,
                        5,
                    )
                )

                selected.append(

                    replace(
                        trade,
                        pattern=pattern,
                    )

                )

            losses = 0

        return selected
