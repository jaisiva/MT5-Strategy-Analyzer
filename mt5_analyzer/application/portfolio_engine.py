"""
portfolio_engine.py

Portfolio Analysis Engine.

Executes one or more trading strategies and consolidates
their results into a PortfolioResult.

The PortfolioEngine performs NO business calculations.

All portfolio calculations are delegated to
PortfolioStatisticsEngine.

Author
------
MT5 Strategy Analyzer

License
-------
MIT
"""

from __future__ import annotations

from typing import Callable

from mt5_analyzer.application.original_engine import (
    OriginalStrategyEngine,
)
from mt5_analyzer.application.lpattern_engine import (
    LPatternEngine,
)
from mt5_analyzer.application.drawdown.drawdown_engine import (
    DrawdownEngine,
)
from mt5_analyzer.application.portfolio_statistics_engine import (
    PortfolioStatisticsEngine,
)

from mt5_analyzer.domain.enums import (
    PatternType,
    StrategyType,
)

from mt5_analyzer.domain.portfolio_input import (
    PortfolioInput,
)

from mt5_analyzer.domain.portfolio_result import (
    PortfolioResult,
)

from mt5_analyzer.domain.strategy_result import (
    StrategyResult,
)

from mt5_analyzer.domain.trade import (
    Trade,
)


class PortfolioEngine:
    """
    Portfolio Analysis Engine.

    Executes multiple independent strategies and
    consolidates them into a single PortfolioResult.
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(self) -> None:

        self._statistics_engine = (
            PortfolioStatisticsEngine()
        )

        self._engine_factory = (
            self._create_engine_factory()
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def run(
        self,
        *,
        trades: list[Trade],
        timeframe: str,
        selected_strategies: list[str],
        portfolio_inputs: dict[
            str,
            PortfolioInput,
        ],
    ) -> PortfolioResult:
        """
        Execute selected strategies.

        Parameters
        ----------
        trades
            Original MT5 trades.

        timeframe
            Report timeframe.

        selected_strategies
            Strategies selected by user.

        portfolio_inputs
            Per-strategy configuration.

        Returns
        -------
        PortfolioResult
        """

        strategy_results = self._execute_strategies(

            trades=trades,

            timeframe=timeframe,

            selected_strategies=selected_strategies,

            portfolio_inputs=portfolio_inputs,

        )

        statistics = self._statistics_engine.calculate(

            strategy_results,

            portfolio_inputs,

        )

        result = PortfolioResult()

        result.strategy_results = strategy_results

        result.statistics = statistics

        return self._complete_result(

            result,

            portfolio_inputs,

        )

    # ---------------------------------------------------------
    # Strategy Registry
    # ---------------------------------------------------------

    def _create_engine_factory(
        self,
    ) -> dict[str, Callable[[], object]]:
        """
        Create strategy engine factory.
        """

        return {

            #
            # Original
            #
            StrategyType.ORIGINAL.value:

                lambda: OriginalStrategyEngine(),

            #
            # L Pattern Strategies
            #
            PatternType.L.value:

                lambda: LPatternEngine(
                    PatternType.L
                ),

            PatternType.LL.value:

                lambda: LPatternEngine(
                    PatternType.LL
                ),

            PatternType.LLL.value:

                lambda: LPatternEngine(
                    PatternType.LLL
                ),

            PatternType.LLLL.value:

                lambda: LPatternEngine(
                    PatternType.LLLL
                ),

            PatternType.LLLLL.value:

                lambda: LPatternEngine(
                    PatternType.LLLLL
                ),

            PatternType.ALL_L.value:

                lambda: LPatternEngine(
                    PatternType.ALL_L
                ),

            #
            # Drawdown Strategies
            #
            "DD10":

                lambda: DrawdownEngine(10),

            "DD15":

                lambda: DrawdownEngine(15),

            "DD20":

                lambda: DrawdownEngine(20),

            "DD25":

                lambda: DrawdownEngine(25),

            "DD30":

                lambda: DrawdownEngine(30),

        }

    # ---------------------------------------------------------
    # Strategy Execution
    # ---------------------------------------------------------

    def _execute_strategies(
        self,
        *,
        trades: list[Trade],
        timeframe: str,
        selected_strategies: list[str],
        portfolio_inputs: dict[
            str,
            PortfolioInput,
        ],
    ) -> list[StrategyResult]:
        """
        Execute all selected strategies.
        """

        results: list[StrategyResult] = []

        for strategy_name in selected_strategies:

            engine = self._create_engine(
                strategy_name
            )

            config = portfolio_inputs.get(
                strategy_name
            )

            if config is None:

                raise ValueError(

                    f"Missing PortfolioInput for "

                    f"'{strategy_name}'."

                )

            result = engine.run(

                trades=trades,

                timeframe=timeframe,

                margin_per_trade=config.margin_per_trade,

            )

            results.append(
                result
            )

        return results

    # ---------------------------------------------------------

    def _create_engine(
        self,
        strategy_name: str,
    ):
        """
        Create strategy engine.
        """

        factory = self._engine_factory.get(
            strategy_name
        )

        if factory is None:

            raise ValueError(

                f"Unknown strategy: "

                f"{strategy_name}"

            )

        return factory()

    # ---------------------------------------------------------

    def available_strategies(
        self,
    ) -> list[str]:
        """
        Return supported strategy names.
        """

        return sorted(
            self._engine_factory.keys()
        )

    # ---------------------------------------------------------
    # Portfolio Result
    # ---------------------------------------------------------

    def _complete_result(
        self,
        result: PortfolioResult,
        portfolio_inputs: dict[
            str,
            PortfolioInput,
        ],
    ) -> PortfolioResult:
        """
        Complete PortfolioResult.

        Calculates

        • Portfolio Trades
        • Monthly Statistics
        • Yearly Statistics

        Returns
        -------
        PortfolioResult
        """

        #
        # Build portfolio trade list.
        #
        # NOTE:
        # If PortfolioStatisticsEngine exposes a public
        # build_portfolio_trades() method, use that.
        #
        portfolio_trades = (
            self._statistics_engine
            .build_portfolio_trades(
                result.strategy_results
            )
        )

        result.portfolio_trades = portfolio_trades

        #
        # Monthly statistics
        #
        monthly_statistics = (
            self._statistics_engine
            .calculate_monthly_statistics(
                portfolio_trades,
            )
        )

        self._statistics_engine.complete_monthly_statistics(

            monthly_statistics,

            result.strategy_results,

            portfolio_inputs,

        )

        result.monthly_statistics = (
            monthly_statistics
        )

        #
        # Yearly statistics
        #
        yearly_statistics = (
            self._statistics_engine
            .calculate_yearly_statistics(
                portfolio_trades,
            )
        )

        self._statistics_engine.complete_yearly_statistics(

            yearly_statistics,

            result.strategy_results,

            portfolio_inputs,

        )

        result.yearly_statistics = (
            yearly_statistics
        )

        #
        # Validate portfolio statistics.
        #
        self._statistics_engine.validate(
            result.statistics
        )

        return result

    # ---------------------------------------------------------
    # Convenience Methods
    # ---------------------------------------------------------

    @staticmethod
    def portfolio_summary(
        result: PortfolioResult,
    ):
        """
        Return PortfolioStatistics.
        """

        return result.statistics

    # ---------------------------------------------------------

    @staticmethod
    def strategy_results(
        result: PortfolioResult,
    ) -> list[StrategyResult]:
        """
        Return StrategyResults.
        """

        return result.strategy_results

    # ---------------------------------------------------------

    @staticmethod
    def portfolio_trades(
        result: PortfolioResult,
    ):
        """
        Return PortfolioTrade list.
        """

        return result.portfolio_trades
		
    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate_inputs(
        self,
        selected_strategies: list[str],
        portfolio_inputs: dict[str, PortfolioInput],
    ) -> None:
        """
        Validate portfolio configuration.
        """

        if not selected_strategies:

            raise ValueError(
                "At least one strategy must be selected."
            )

        for strategy_name in selected_strategies:

            if strategy_name not in self._engine_factory:

                raise ValueError(
                    f"Unsupported strategy: {strategy_name}"
                )

            if strategy_name not in portfolio_inputs:

                raise ValueError(
                    f"Missing PortfolioInput for "
                    f"'{strategy_name}'."
                )

            config = portfolio_inputs[strategy_name]

            if config.margin_per_trade <= 0:

                raise ValueError(
                    f"Invalid margin_per_trade for "
                    f"'{strategy_name}'."
                )

            if config.lot_size <= 0:

                raise ValueError(
                    f"Invalid lot_size for "
                    f"'{strategy_name}'."
                )

    # ---------------------------------------------------------

    @staticmethod
    def supported_strategies() -> list[str]:
        """
        Return all supported strategy names.

        This helper is useful for CLI validation.
        """

        return [

            StrategyType.ORIGINAL.value,

            PatternType.L.value,

            PatternType.LL.value,

            PatternType.LLL.value,

            PatternType.LLLL.value,

            PatternType.LLLLL.value,

            PatternType.ALL_L.value,

            "DD10",

            "DD15",

            "DD20",

            "DD25",

            "DD30",

        ]

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            "("
            f"strategies={len(self._engine_factory)}"
            ")"
        )
