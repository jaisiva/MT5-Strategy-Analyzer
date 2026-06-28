"""
test_statistics_engine.py

Unit tests for StatisticsEngine.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

import pytest

from mt5_analyzer.application.statistics_engine import StatisticsEngine
from mt5_analyzer.domain.statistics import Statistics


class TestStatisticsEngine:
    """
    Unit tests for StatisticsEngine.
    """

    def setup_method(self) -> None:
        self.engine = StatisticsEngine()

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_returns_statistics_object(
        self,
        mixed_trades,
    ) -> None:
        """
        Engine should return a Statistics object.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        assert isinstance(
            statistics,
            Statistics,
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_total_trades(
        self,
        mixed_trades,
    ) -> None:
        """
        Total trades should equal input length.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        assert statistics.total_trades == len(
            mixed_trades
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_winning_trades(
        self,
        mixed_trades,
    ) -> None:
        """
        Winning trade count should be correct.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        expected = sum(
            trade.net_profit > 0
            for trade in mixed_trades
        )

        assert statistics.winning_trades == expected

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_losing_trades(
        self,
        mixed_trades,
    ) -> None:
        """
        Losing trade count should be correct.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        expected = sum(
            trade.net_profit < 0
            for trade in mixed_trades
        )

        assert statistics.losing_trades == expected

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_net_profit(
        self,
        mixed_trades,
    ) -> None:
        """
        Net profit should equal sum of trade profits.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        expected = sum(
            trade.net_profit
            for trade in mixed_trades
        )

        assert statistics.net_profit == pytest.approx(
            expected
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_gross_profit(
        self,
        mixed_trades,
    ) -> None:
        """
        Gross profit should equal sum of winning trades.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        expected = sum(
            trade.net_profit
            for trade in mixed_trades
            if trade.net_profit > 0
        )

        assert statistics.gross_profit == pytest.approx(
            expected
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_gross_loss(
        self,
        mixed_trades,
    ) -> None:
        """
        Gross loss should equal sum of losing trades.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        expected = sum(
            trade.net_profit
            for trade in mixed_trades
            if trade.net_profit < 0
        )

        assert statistics.gross_loss == pytest.approx(
            expected
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_all_winning_trades(
        self,
        winning_trades,
    ) -> None:
        """
        All winning trades.
        """

        statistics = self.engine.calculate(
            winning_trades,
        )

        assert statistics.winning_trades == len(
            winning_trades
        )

        assert statistics.losing_trades == 0

        assert statistics.gross_loss == 0

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_all_losing_trades(
        self,
        losing_trades,
    ) -> None:
        """
        All losing trades.
        """

        statistics = self.engine.calculate(
            losing_trades,
        )

        assert statistics.winning_trades == 0

        assert statistics.losing_trades == len(
            losing_trades
        )

        assert statistics.gross_profit == 0

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_empty_trade_list(
        self,
    ) -> None:
        """
        Empty trade list should produce zeroed statistics.
        """

        statistics = self.engine.calculate(
            [],
        )

        assert statistics.total_trades == 0

        assert statistics.net_profit == 0

        assert statistics.gross_profit == 0

        assert statistics.gross_loss == 0

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_profit_factor_non_negative(
        self,
        mixed_trades,
    ) -> None:
        """
        Profit factor should never be negative.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        assert statistics.profit_factor >= 0

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_expectancy_is_float(
        self,
        mixed_trades,
    ) -> None:
        """
        Expectancy should be numeric.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        assert isinstance(
            statistics.expectancy,
            float,
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    @pytest.mark.strategy
    def test_statistics_serialization(
        self,
        mixed_trades,
    ) -> None:
        """
        Statistics should be serializable.
        """

        statistics = self.engine.calculate(
            mixed_trades,
        )

        data = statistics.to_dict()

        assert isinstance(
            data,
            dict,
        )

        assert "total_trades" in data

        assert "net_profit" in data
