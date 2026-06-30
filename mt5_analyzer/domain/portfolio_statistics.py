"""
portfolio_statistics.py

Portfolio level statistics.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PortfolioStatistics:
    """
    Portfolio statistics.

    Attributes
    ----------
    trade_count
    wins
    losses
    peak_margin
    maximum_drawdown
    average_profit
    net_profit
    capital
    return_on_equity
    """

    trade_count: int = 0

    wins: int = 0

    losses: int = 0

    peak_margin: float = 0.0

    maximum_drawdown: float = 0.0

    average_profit: float = 0.0

    net_profit: float = 0.0

    capital: float = 0.0

    return_on_equity: float = 0.0
