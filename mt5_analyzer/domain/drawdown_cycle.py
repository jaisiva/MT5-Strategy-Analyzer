"""
drawdown_cycle.py

Domain model representing a single rolling-peak drawdown cycle.

A DrawdownCycle begins when the equity drawdown reaches a configured
threshold (e.g. DD10, DD15, DD20) and ends when the equity fully
recovers to the previous rolling peak.

This model is immutable and contains all information required for
reporting and portfolio analysis.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from mt5_analyzer.domain.trade import Trade


@dataclass(slots=True, frozen=True)
class DrawdownCycle:
    """
    Represents a single drawdown cycle.
    """

    # ------------------------------------------------------------
    # Strategy
    # ------------------------------------------------------------

    strategy: str

    threshold: float

    cycle_number: int
    cycle_id: str
    year: int
    month: int    
    # ------------------------------------------------------------
    # Peak Information
    # ------------------------------------------------------------

    peak_equity: float

    peak_datetime: datetime

    trigger_equity: float

    trigger_datetime: datetime

    recovery_equity: float

    recovery_datetime: Optional[datetime]

    # ------------------------------------------------------------
    # Trades
    # ------------------------------------------------------------

    trades: tuple[Trade, ...] = field(default_factory=tuple)

    # ------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------

    trade_count: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    net_profit: float = 0.0

    average_trade: float = 0.0

    # ------------------------------------------------------------
    # Risk Metrics
    # ------------------------------------------------------------

    maximum_drawdown: float = 0.0

    peak_margin: float = 0.0

    capital_used: float = 0.0

    roe: float = 0.0

    max_concurrent_trades: int = 1

    # ------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------

    @property
    def recovered(self) -> bool:
        """
        Returns True if cycle recovered.
        """

        return self.recovery_datetime is not None

    @property
    def duration(self):
        """
        Duration of cycle.
        """

        if self.recovery_datetime is None:
            return None

        return self.recovery_datetime - self.trigger_datetime

    @property
    def recovery_days(self) -> int:
        """
        Recovery duration in days.
        """

        if self.duration is None:
            return 0

        return self.duration.days

    @property
    def win_rate(self) -> float:
        """
        Winning percentage.
        """

        if self.trade_count == 0:
            return 0.0

        return (
            self.winning_trades
            / self.trade_count
            * 100.0
        )

    @property
    def loss_rate(self) -> float:
        """
        Losing percentage.
        """

        if self.trade_count == 0:
            return 0.0

        return (
            self.losing_trades
            / self.trade_count
            * 100.0
        )

    def to_dict(self) -> dict:
        """
        Convert cycle to dictionary.
        """

        return {

            "Strategy": self.strategy,

            "Threshold": self.threshold,

            "Peak Equity": self.peak_equity,

            "Peak Date": self.peak_datetime,

            "Trigger Equity": self.trigger_equity,

            "Trigger Date": self.trigger_datetime,

            "Recovery Equity": self.recovery_equity,

            "Recovery Date": self.recovery_datetime,

            "Recovered": self.recovered,

            "Recovery Days": self.recovery_days,

            "Trades": self.trade_count,

            "Wins": self.winning_trades,

            "Losses": self.losing_trades,

            "Win %": round(
                self.win_rate,
                2,
            ),

            "Loss %": round(
                self.loss_rate,
                2,
            ),

            "Gross Profit": self.gross_profit,

            "Gross Loss": self.gross_loss,

            "Net Profit": self.net_profit,

            "Avg Trade": self.average_trade,

            "MDD": self.maximum_drawdown,

            "Peak Margin": self.peak_margin,

            "Capital Used": self.capital_used,

            "%ROE": self.roe,

            "Max Concurrent": self.max_concurrent_trades,

        }

    def __str__(self) -> str:

        return (
            f"{self.strategy} | "
            f"DD{self.threshold:.0f} | "
            f"Trades={self.trade_count} | "
            f"Net={self.net_profit:.2f}"
        )
