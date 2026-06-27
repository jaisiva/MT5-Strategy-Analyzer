@dataclass(slots=True)
class StrategyResult:
    strategy_name: str
    statistics: StrategyStatistics
    trades: list[Trade]
