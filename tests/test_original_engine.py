"""
test_original_engine.py

Unit tests for OriginalStrategyEngine.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

import pytest

from mt5_analyzer.application.original_engine import OriginalStrategyEngine
from mt5_analyzer.domain.strategy_result import StrategyResult


class TestOriginalStrategyEngine:
    """
    Unit tests for OriginalStrategyEngine.
    """

    def setup_method(self) -> None:
        """
        Create engine instance.
        """

        self.engine = OriginalStrategyEngine()

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_returns_strategy_result(
        self,
        mixed_trades,
    ) -> None:
        """
        Engine should return a StrategyResult.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert isinstance(
            result,
            StrategyResult,
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_strategy_name(
        self,
        mixed_trades,
    ) -> None:
        """
        Strategy name should be Original.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert result.strategy_name == "Original"

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_trade_count(
        self,
        mixed_trades,
    ) -> None:
        """
        All trades should be included.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert len(result.trades) == len(
            mixed_trades
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_statistics_created(
        self,
        mixed_trades,
    ) -> None:
        """
        Statistics should be generated.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert result.statistics is not None

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_statistics_trade_count(
        self,
        mixed_trades,
    ) -> None:
        """
        Statistics should contain correct trade count.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert (
            result.statistics.total_trades
            == len(mixed_trades)
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_empty_trade_list(
        self,
    ) -> None:
        """
        Empty trade list should produce an empty result.
        """

        result = self.engine.run(
            [],
            timeframe="H1",
        )

        assert isinstance(
            result,
            StrategyResult,
        )

        assert len(result.trades) == 0

        assert (
            result.statistics.total_trades == 0
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_single_trade(
        self,
        sample_trade,
    ) -> None:
        """
        Single trade should be handled correctly.
        """

        result = self.engine.run(
            [sample_trade],
            timeframe="H1",
        )

        assert len(result.trades) == 1

        assert (
            result.statistics.total_trades == 1
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_all_winning_trades(
        self,
        winning_trades,
    ) -> None:
        """
        Winning-only strategy.
        """

        result = self.engine.run(
            winning_trades,
            timeframe="H1",
        )

        assert (
            result.statistics.winning_trades
            == len(winning_trades)
        )

        assert (
            result.statistics.losing_trades
            == 0
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_all_losing_trades(
        self,
        losing_trades,
    ) -> None:
        """
        Losing-only strategy.
        """

        result = self.engine.run(
            losing_trades,
            timeframe="H1",
        )

        assert (
            result.statistics.winning_trades
            == 0
        )

        assert (
            result.statistics.losing_trades
            == len(losing_trades)
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_monthly_statistics_exists(
        self,
        mixed_trades,
    ) -> None:
        """
        Monthly statistics should exist.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert hasattr(
            result,
            "monthly_statistics",
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_yearly_statistics_exists(
        self,
        mixed_trades,
    ) -> None:
        """
        Yearly statistics should exist.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert hasattr(
            result,
            "yearly_statistics",
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_result_serialization(
        self,
        mixed_trades,
    ) -> None:
        """
        StrategyResult should be serializable.
        """

        result = self.engine.run(
            mixed_trades,
            timeframe="H1",
        )

        data = result.to_dict()

        assert isinstance(
            data,
            dict,
        )

        assert "strategy_name" in data

        assert "statistics" in data

        assert "trades" in data
