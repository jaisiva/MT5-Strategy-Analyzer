"""
trade.py

Domain model representing a single MT5 trade.

This module defines the immutable Trade entity used throughout the
MT5 Strategy Analyzer.

Every analysis engine operates on Trade objects.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import Optional

from mt5_analyzer.domain.enums import PatternType, SessionType, TradeSide


@dataclass(slots=True, frozen=True)
class Trade:
    """
    Immutable MT5 trade.

    Parameters
    ----------
    ticket
        MT5 ticket number.

    symbol
        Trading symbol.

    side
        BUY or SELL.

    volume
        Lot size.

    entry_time
        Trade entry datetime.

    exit_time
        Trade exit datetime.

    profit
        Trade profit excluding commission and swap.

    commission
        Commission charged.

    swap
        Swap charged.

    pattern
        Strategy pattern.

    session
        Trading session.
    """

    ticket: Optional[int]

    symbol: str

    side: TradeSide

    volume: float

    entry_time: datetime

    exit_time: datetime

    profit: float

    commission: float = 0.0

    swap: float = 0.0

    pattern: PatternType = PatternType.ORIGINAL

    session: Optional[SessionType] = None

    def __post_init__(self) -> None:
        """
        Validate immutable Trade object.
        """

        if self.entry_time > self.exit_time:
            raise ValueError("Entry time cannot be after exit time.")

        if self.volume <= 0:
            raise ValueError("Trade volume must be greater than zero.")

    @property
    def duration(self) -> timedelta:
        """
        Trade duration.
        """
        return self.exit_time - self.entry_time

    @property
    def holding_minutes(self) -> float:
        """
        Holding time in minutes.
        """
        return self.duration.total_seconds() / 60.0

    @property
    def net_profit(self) -> float:
        """
        Profit including commission and swap.
        """
        return self.profit + self.commission + self.swap

    @property
    def is_buy(self) -> bool:
        """
        True if BUY trade.
        """
        return self.side is TradeSide.BUY

    @property
    def is_sell(self) -> bool:
        """
        True if SELL trade.
        """
        return self.side is TradeSide.SELL

    @property
    def is_win(self) -> bool:
        """
        True if profitable trade.
        """
        return self.net_profit > 0

    @property
    def is_loss(self) -> bool:
        """
        True if losing trade.
        """
        return self.net_profit < 0

    def with_pattern(self, pattern: PatternType) -> "Trade":
        """
        Return a new Trade with a different pattern.

        Since Trade is immutable (frozen=True), analysis engines
        should never modify existing Trade objects.
        """

        return replace(self, pattern=pattern)

    def with_session(self, session: SessionType) -> "Trade":
        """
        Return a new Trade with assigned session.
        """

        return replace(self, session=session)

    def to_dict(self) -> dict:
        """
        Convert Trade to dictionary.
        """

        return {
            "ticket": self.ticket,
            "symbol": self.symbol,
            "side": self.side.value,
            "volume": self.volume,
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
            "profit": self.profit,
            "commission": self.commission,
            "swap": self.swap,
            "net_profit": self.net_profit,
            "pattern": self.pattern.value,
            "session": self.session.value if self.session else None,
        }

    def __str__(self) -> str:
        return (
            f"{self.symbol:<10}"
            f"{self.side.value:<5} "
            f"{self.entry_time:%d-%m-%Y %H:%M}  "
            f"{self.net_profit:>10.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"Trade("
            f"ticket={self.ticket}, "
            f"symbol='{self.symbol}', "
            f"side={self.side.value}, "
            f"net_profit={self.net_profit:.2f}"
            f")"
        )
