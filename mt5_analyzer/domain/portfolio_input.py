"""
portfolio_input.py

Configuration for an individual strategy within a portfolio.

Each selected strategy has its own trading parameters.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PortfolioInput:
    """
    User supplied inputs for a strategy.

    Attributes
    ----------
    strategy
        Strategy name (Original, L, LL, DD10...)

    lot_size
        Trading lot size.

    margin_per_trade
        Margin required per trade.
    """

    strategy: str

    lot_size: float

    margin_per_trade: float
