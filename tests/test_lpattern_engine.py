"""
test_lpattern_engine.py

Unit tests for LPatternEngine.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from mt5_analyzer.application.lpattern_engine import LPatternEngine
from mt5_analyzer.domain.enums import PatternType
from mt5_analyzer.domain.strategy_result import StrategyResult


class TestLPatternEngine:

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_returns_strategy_result(
        self,
        mixed_trades,
    ):

        trades = [

            replace(
                trade,
                pattern=PatternType.L,
            )

            for trade in mixed_trades

        ]

        engine = LPatternEngine(
            PatternType.L,
        )

        result = engine.run(
            trades,
            timeframe="H1",
        )

        assert isinstance(
            result,
            StrategyResult,
        )

    # ------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_filters_l_pattern(
        self,
        mixed_trades,
    ):

        trades = []

        for i, trade in enumerate(mixed_trades):

            pattern = (
                PatternType.L
                if i % 2 == 0
                else PatternType.LL
            )

            trades.append(
                replace(
                    trade,
                    pattern=pattern,
                )
            )

        engine = LPatternEngine(
            PatternType.L,
        )

        result = engine.run(
            trades,
            timeframe="H1",
        )

        assert all(
            trade.pattern is PatternType.L
            for trade in result.trades
        )

    # ------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_empty_result(self):

        engine = LPatternEngine(
            PatternType.LLL,
        )

        result = engine.run(
            [],
            timeframe="H1",
        )

        assert result.statistics.total_trades == 0

    # ------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_statistics_match_filtered_trades(
        self,
        mixed_trades,
    ):

        trades = [

            replace(
                trade,
                pattern=PatternType.L,
            )

            for trade in mixed_trades

        ]

        engine = LPatternEngine(
            PatternType.L,
        )

        result = engine.run(
            trades,
            timeframe="H1",
        )

        assert (
            result.statistics.total_trades
            == len(trades)
        )
