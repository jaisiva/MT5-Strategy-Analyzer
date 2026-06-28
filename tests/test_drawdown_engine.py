"""
test_drawdown_engine.py

Unit tests for DrawdownEngine.
"""

import pytest

from mt5_analyzer.application.drawdown.drawdown_engine import (
    DrawdownEngine,
)


class TestDrawdownEngine:

    @pytest.mark.unit
    def test_returns_cycles(
        self,
        mixed_trades,
    ):

        engine = DrawdownEngine(
            threshold=20,
        )

        result = engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert hasattr(
            result,
            "cycles",
        )

    @pytest.mark.unit
    def test_statistics_created(
        self,
        mixed_trades,
    ):

        engine = DrawdownEngine(
            threshold=20,
        )

        result = engine.run(
            mixed_trades,
            timeframe="H1",
        )

        assert result.statistics is not None
