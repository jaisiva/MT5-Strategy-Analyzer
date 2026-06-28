"""
test_session_engine.py

Unit tests for SessionEngine.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from mt5_analyzer.application.session_engine import SessionEngine
from mt5_analyzer.domain.enums import SessionType


class TestSessionEngine:

    @pytest.mark.unit
    def test_london_session(
        self,
        mixed_trades,
    ):

        trades = [

            replace(
                trade,
                session=SessionType.LONDON,
            )

            for trade in mixed_trades

        ]

        engine = SessionEngine(
            SessionType.LONDON,
        )

        result = engine.run(
            trades,
            timeframe="H1",
        )

        assert len(result.trades) == len(trades)

    @pytest.mark.unit
    def test_empty(self):

        engine = SessionEngine(
            SessionType.NEW_YORK,
        )

        result = engine.run(
            [],
            timeframe="H1",
        )

        assert result.statistics.total_trades == 0
