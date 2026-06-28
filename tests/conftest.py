"""
conftest.py

Shared pytest fixtures for MT5 Strategy Analyzer.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from mt5_analyzer.domain.enums import (
    Direction,
    PatternType,
    SessionType,
)
from mt5_analyzer.domain.trade import Trade


# ----------------------------------------------------------------------
# Temporary Output Directory
# ----------------------------------------------------------------------

@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """
    Temporary directory for generated reports.
    """

    return tmp_path


# ----------------------------------------------------------------------
# Sample MT5 Report
# ----------------------------------------------------------------------

@pytest.fixture
def sample_report_file() -> Path:
    """
    Sample MT5 report.

    Expected location:

        tests/data/sample_mt5_report.xlsx
    """

    return (
        Path(__file__).parent
        / "data"
        / "sample_mt5_report.xlsx"
    )


# ----------------------------------------------------------------------
# Trade Factory Fixture
# ----------------------------------------------------------------------

@pytest.fixture
def trade_factory():
    """
    Factory fixture used by tests to build Trade objects.
    """

    def _create_trade(
        *,
        ticket: int = 1,
        profit: float = 10.0,
        day: int = 1,
        pattern: PatternType = PatternType.NONE,
        session: SessionType = SessionType.LONDON,
        direction: Direction = Direction.BUY,
    ) -> Trade:

        entry = datetime(
            2024,
            1,
            day,
            9,
            0,
        )

        exit = entry + timedelta(hours=1)

        return Trade(

            ticket=ticket,

            symbol="XAUUSD",

            direction=direction,

            volume=0.01,

            entry_time=entry,

            exit_time=exit,

            entry_price=2000.0,

            exit_price=2010.0,

            stop_loss=1990.0,

            take_profit=2020.0,

            commission=0.0,

            swap=0.0,

            net_profit=profit,

            pattern=pattern,

            session=session,

        )

    return _create_trade


# ----------------------------------------------------------------------
# Single Trade
# ----------------------------------------------------------------------

@pytest.fixture
def sample_trade(trade_factory) -> Trade:
    """
    One profitable trade.
    """

    return trade_factory()


# ----------------------------------------------------------------------
# Winning Trades
# ----------------------------------------------------------------------

@pytest.fixture
def winning_trades(trade_factory) -> list[Trade]:
    """
    Ten profitable trades.
    """

    return [

        trade_factory(
            ticket=i + 1,
            profit=10.0,
            day=i + 1,
        )

        for i in range(10)

    ]


# ----------------------------------------------------------------------
# Losing Trades
# ----------------------------------------------------------------------

@pytest.fixture
def losing_trades(trade_factory) -> list[Trade]:
    """
    Ten losing trades.
    """

    return [

        trade_factory(
            ticket=i + 1,
            profit=-10.0,
            day=i + 1,
        )

        for i in range(10)

    ]


# ----------------------------------------------------------------------
# Mixed Trades
# ----------------------------------------------------------------------

@pytest.fixture
def mixed_trades(trade_factory) -> list[Trade]:
    """
    Mixed profitable and losing trades.
    """

    profits = [

        10,
        -8,
        12,
        -5,
        9,
        -7,
        14,
        -6,
        8,
        -4,

    ]

    return [

        trade_factory(

            ticket=i + 1,

            profit=profit,

            day=i + 1,

        )

        for i, profit in enumerate(profits)

    ]
