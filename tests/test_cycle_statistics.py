"""
test_cycle_statistics.py

Unit tests for CycleStatisticsEngine.
"""

import pytest

from mt5_analyzer.application.drawdown.cycle_statistics import (
    CycleStatisticsEngine,
)


class TestCycleStatistics:

    @pytest.mark.unit
    def test_statistics_created(
        self,
        mixed_trades,
    ):

        engine = CycleStatisticsEngine()

        stats = engine.calculate(
            mixed_trades,
        )

        assert stats is not None
