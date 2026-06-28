"""
strategy_result.py

Domain model representing the result of a strategy analysis.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field

from mt5_analyzer.domain.statistics import StrategyStatistics
from mt5_analyzer.domain.trade import Trade


@dataclass(slots=True)
class StrategyResult:
    """
    Result returned by every strategy engine.
    """

    strategy_name: str

    statistics: StrategyStatistics

    trades: list[Trade] = field(default_factory=list)

    monthly_statistics: dict[str, StrategyStatistics] = field(
        default_factory=dict
    )

    yearly_statistics: dict[int, StrategyStatistics] = field(
        default_factory=dict
    )

    description: str = ""

    def to_dict(self) -> dict:
        """
        Serialize StrategyResult.
        """

        return {
            "strategy_name": self.strategy_name,
            "statistics": self.statistics.to_dict(),
            "trade_count": len(self.trades),
            "monthly_statistics": {
                key: value.to_dict()
                for key, value in self.monthly_statistics.items()
            },
            "yearly_statistics": {
                str(key): value.to_dict()
                for key, value in self.yearly_statistics.items()
            },
            "description": self.description,
        }
