"""
test_cycle_detector.py

Unit tests for CycleDetector.
"""

import pytest

from mt5_analyzer.application.drawdown.cycle_detector import (
    CycleDetector,
)


class TestCycleDetector:

    @pytest.mark.unit
    def test_returns_list(
        self,
        mixed_trades,
    ):

        detector = CycleDetector(
            threshold=20,
        )

        cycles = detector.detect(
            mixed_trades,
        )

        assert isinstance(
            cycles,
            list,
        )

    @pytest.mark.unit
    def test_cycle_ids_unique(
        self,
        mixed_trades,
    ):

        detector = CycleDetector(
            threshold=20,
        )

        cycles = detector.detect(
            mixed_trades,
        )

        ids = [
            c.cycle_id
            for c in cycles
        ]

        assert len(ids) == len(set(ids))
