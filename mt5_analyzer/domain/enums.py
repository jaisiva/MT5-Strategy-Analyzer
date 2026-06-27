"""
enums.py

Project-wide enumerations used throughout the MT5 Strategy Analyzer.

Using Enum classes instead of raw strings provides:

- Type safety
- IDE auto-completion
- Better validation
- Cleaner code
- Fewer typing mistakes

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from enum import Enum


class TradeSide(str, Enum):
    """
    Trade direction.
    """

    BUY = "BUY"
    SELL = "SELL"

    @classmethod
    def from_string(cls, value: str) -> "TradeSide":
        """
        Convert string to TradeSide.
        """
        value = value.strip().upper()

        if value in ("BUY", "LONG"):
            return cls.BUY

        if value in ("SELL", "SHORT"):
            return cls.SELL

        raise ValueError(f"Unknown trade side: {value}")


class PatternType(str, Enum):
    """
    Strategy pattern.
    """

    ORIGINAL = "Original"

    L = "L"

    LL = "LL"

    LLL = "LLL"

    LLLL = "LLLL"

    LLLLL = "LLLLL"

    ALL_L = "All L"


class SessionType(str, Enum):
    """
    Trading session.
    """

    ASIA = "Asia"

    EUROPE = "Europe"

    US_OVERLAP = "US Overlap"

    LATE_US = "Late US"


class StrategyType(str, Enum):
    """
    Strategy family.
    """

    ORIGINAL = "Original"

    LPATTERN = "L Pattern"

    DRAWDOWN = "Drawdown"

    PORTFOLIO = "Portfolio"


class DrawdownType(str, Enum):
    """
    Drawdown strategies.
    """

    DD10 = "DD10"

    DD15 = "DD15"

    DD20 = "DD20"

    DD25 = "DD25"

    DD30 = "DD30"


class DirectionFilter(str, Enum):
    """
    Trade direction filter.
    """

    BOTH = "Both"

    LONG = "Long"

    SHORT = "Short"


class ReportType(str, Enum):
    """
    Output workbook type.
    """

    SUMMARY = "Summary"

    MONTHLY = "Monthly"

    YEARLY = "Yearly"

    SESSION = "Session"

    TRADE_DETAILS = "Trade Details"

    DD_CYCLES = "DD Cycles"

    PORTFOLIO = "Portfolio"

    OPTIMIZATION = "Optimization"


class TimeFrame(str, Enum):
    """
    MT5 timeframe.
    """

    M1 = "1 Minute"

    M3 = "3 Minute"

    M5 = "5 Minute"

    H1 = "1 Hour"

    H4 = "4 Hour"

    D1 = "Daily"


class TradeStatus(str, Enum):
    """
    Trade outcome.
    """

    WIN = "Win"

    LOSS = "Loss"

    BREAKEVEN = "Breakeven"


class CycleStatus(str, Enum):
    """
    DD cycle state.
    """

    OPEN = "Open"

    RECOVERED = "Recovered"


class SortOrder(str, Enum):
    """
    Report sorting.
    """

    ASCENDING = "Ascending"

    DESCENDING = "Descending"
