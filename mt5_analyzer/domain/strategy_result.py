"""
strategy_result.py

Common result returned by all strategy engines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mt5_analyzer.domain.statistics import StrategyStatistics
from mt5_analyzer.domain.trade import Trade


@dataclass(slots=True)
class StrategyResult:
    """
    Result produced by a strategy engine.

    Different strategies may populate different optional fields.
    """

    strategy_name: str

    statistics: StrategyStatistics

    trades: list[Trade]

    #
    # Original / L Pattern
    #
    monthly_statistics: dict[str, StrategyStatistics] = field(
        default_factory=dict
    )

    yearly_statistics: dict[str, StrategyStatistics] = field(
        default_factory=dict
    )

    #
    # Drawdown Strategy
    #
    cycles: list[Any] = field(
        default_factory=list
    )
