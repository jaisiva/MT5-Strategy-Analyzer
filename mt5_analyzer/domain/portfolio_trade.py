"""
portfolio_trade.py

Portfolio trade.

A portfolio trade represents one trade selected by one strategy.

The same MT5 trade may appear multiple times if selected by
different strategies.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass

from mt5_analyzer.domain.trade import Trade


@dataclass(slots=True, frozen=True)
class PortfolioTrade:
    """
    Portfolio trade.

    Attributes
    ----------
    strategy
        Strategy name.

    trade
        Original MT5 trade.
    """

    strategy: str

    trade: Trade
