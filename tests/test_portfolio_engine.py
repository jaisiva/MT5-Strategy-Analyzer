"""
test_portfolio_engine.py

Unit tests for PortfolioEngine.
"""

import pytest

from mt5_analyzer.application.original_engine import (
    OriginalStrategyEngine,
)
from mt5_analyzer.application.portfolio.portfolio_engine import (
    PortfolioEngine,
)


class TestPortfolioEngine:

    @pytest.mark.unit
    def test_build_portfolio(
        self,
        mixed_trades,
    ):

        original = OriginalStrategyEngine()

        strategy = original.run(
            mixed_trades,
            timeframe="H1",
        )

        engine = PortfolioEngine()

        result = engine.build(

            portfolio_name="Test",

            strategies=[strategy],

            description="Unit Test",

        )

        assert result.strategy_count == 1

    @pytest.mark.unit
    def test_trade_count(
        self,
        mixed_trades,
    ):

        original = OriginalStrategyEngine()

        strategy = original.run(
            mixed_trades,
            timeframe="H1",
        )

        engine = PortfolioEngine()

        result = engine.build(

            portfolio_name="Test",

            strategies=[strategy],

        )

        assert result.trade_count == len(
            mixed_trades
        )
