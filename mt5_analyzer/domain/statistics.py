"""
statistics.py

Domain models representing strategy performance statistics.

These immutable data models are shared across all analysis engines,
ensuring a consistent interface for reporting and comparison.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, frozen=True)
class StrategyStatistics:
    """
    Summary statistics for a trading strategy.
    """

    strategy_name: str

    pattern: str

    timeframe: str

    total_trades: int

    winning_trades: int

    losing_trades: int

    breakeven_trades: int = 0

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    net_profit: float = 0.0

    average_trade: float = 0.0

    largest_win: float = 0.0

    largest_loss: float = 0.0

    profit_factor: float = 0.0

    expectancy: float = 0.0

    max_drawdown: float = 0.0

    peak_equity: float = 0.0

    ending_equity: float = 0.0

    peak_margin: float = 0.0

    capital_used: float = 0.0

    roe: float = 0.0

    recovery_factor: float = 0.0

    return_to_drawdown: float = 0.0

    average_holding_minutes: float = 0.0

    longest_holding_minutes: float = 0.0

    shortest_holding_minutes: float = 0.0

    max_concurrent_trades: int = 1

    @property
    def win_rate(self) -> float:
        """
        Winning percentage.
        """

        if self.total_trades == 0:
            return 0.0

        return (self.winning_trades / self.total_trades) * 100.0

    @property
    def loss_rate(self) -> float:
        """
        Losing percentage.
        """

        if self.total_trades == 0:
            return 0.0

        return (self.losing_trades / self.total_trades) * 100.0

    @property
    def average_win(self) -> float:
        """
        Average winning trade.
        """

        if self.winning_trades == 0:
            return 0.0

        return self.gross_profit / self.winning_trades

    @property
    def average_loss(self) -> float:
        """
        Average losing trade.
        """

        if self.losing_trades == 0:
            return 0.0

        return abs(self.gross_loss) / self.losing_trades

    @property
    def payoff_ratio(self) -> float:
        """
        Average Win / Average Loss.
        """

        avg_loss = self.average_loss

        if avg_loss == 0:
            return 0.0

        return self.average_win / avg_loss

    @property
    def recovery_ratio(self) -> float:
        """
        Net Profit / Maximum Drawdown.
        """

        if self.max_drawdown == 0:
            return 0.0

        return self.net_profit / abs(self.max_drawdown)

    def to_dict(self) -> dict:
        """
        Convert statistics into dictionary.

        Useful for Excel export and DataFrame creation.
        """

        return {
            "Strategy": self.strategy_name,
            "Pattern": self.pattern,
            "Timeframe": self.timeframe,
            "Trades": self.total_trades,
            "Wins": self.winning_trades,
            "Losses": self.losing_trades,
            "Breakeven": self.breakeven_trades,
            "%Win": round(self.win_rate, 2),
            "%Loss": round(self.loss_rate, 2),
            "Gross Profit": self.gross_profit,
            "Gross Loss": self.gross_loss,
            "Net Profit": self.net_profit,
            "Average Trade": self.average_trade,
            "Largest Win": self.largest_win,
            "Largest Loss": self.largest_loss,
            "Profit Factor": self.profit_factor,
            "Expectancy": self.expectancy,
            "MDD": self.max_drawdown,
            "Peak Equity": self.peak_equity,
            "Ending Equity": self.ending_equity,
            "Peak Margin": self.peak_margin,
            "Capital Used": self.capital_used,
            "%ROE": self.roe,
            "Recovery Factor": self.recovery_factor,
            "Return/MDD": self.return_to_drawdown,
            "Avg Holding (Min)": self.average_holding_minutes,
            "Longest Holding (Min)": self.longest_holding_minutes,
            "Shortest Holding (Min)": self.shortest_holding_minutes,
            "Max Concurrent Trades": self.max_concurrent_trades,
        }

    def __str__(self) -> str:
        return (
            f"{self.strategy_name} | "
            f"Trades={self.total_trades} | "
            f"Net={self.net_profit:.2f} | "
            f"Win%={self.win_rate:.2f}"
        )
