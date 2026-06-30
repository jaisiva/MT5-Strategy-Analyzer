"""
portfolio_engine.py

Portfolio Analysis Engine.

This engine executes one or more trading strategies and
consolidates their results into a PortfolioResult.

The Portfolio Engine DOES NOT perform any portfolio
calculations.

All calculations are delegated to
PortfolioStatisticsEngine.

Responsibilities
----------------

• Execute selected strategies

• Collect StrategyResult objects

• Build PortfolioResult

• Invoke PortfolioStatisticsEngine

• Calculate monthly statistics

• Calculate yearly statistics

• Return PortfolioResult

Author
------
MT5 Strategy Analyzer

License
-------
MIT
"""

from __future__ import annotations

from typing import Callable

from mt5_analyzer.application.drawdown_engine import (
    DrawdownEngine,
)
from mt5_analyzer.application.lpattern_engine import (
    LPatternEngine,
)
from mt5_analyzer.application.original_engine import (
    OriginalStrategyEngine,
)
from mt5_analyzer.application.portfolio_statistics_engine import (
    PortfolioStatisticsEngine,
)

from mt5_analyzer.domain.enums import (
    DrawdownType,
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

    Executes selected strategies and consolidates
    results into a PortfolioResult.
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
        trades: list[Trade],
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

        selected_strategies

            Strategy names selected by user.

        portfolio_inputs

            Strategy configuration.

        Returns
        -------
        PortfolioResult
        """

        strategy_results = (
            self._execute_strategies(
                trades,
                selected_strategies,
            )
        )

        statistics = (
            self._statistics_engine.calculate(
                strategy_results,
                portfolio_inputs,
            )
        )

        portfolio_result = PortfolioResult()

        portfolio_result.strategy_results = (
            strategy_results
        )

        portfolio_result.statistics = (
            statistics
        )

        #
        # Monthly / Yearly statistics
        # are calculated after the
        # PortfolioTrade collection
        # is built.
        #

        return self._complete_result(
            portfolio_result,
            portfolio_inputs,
        )

    # ---------------------------------------------------------
    # Engine Registry
    # ---------------------------------------------------------

    def _create_engine_factory(
        self,
    ) -> dict[
        str,
        Callable[[], object],
    ]:
        """
        Create strategy registry.

        Implemented in Part-2.
        """

        return {}

    # ---------------------------------------------------------
    # Strategy Registry
    # ---------------------------------------------------------

    def _create_engine_factory(
        self,
    ) -> dict[
        str,
        Callable[[], object],
    ]:
        """
        Create strategy factory.

        Returns
        -------
        Dictionary of strategy factories.
        """

        return {

            #
            # Original Strategy
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
            DrawdownType.DD10.value:

                lambda: DrawdownEngine(
                    DrawdownType.DD10
                ),

            DrawdownType.DD15.value:

                lambda: DrawdownEngine(
                    DrawdownType.DD15
                ),

            DrawdownType.DD20.value:

                lambda: DrawdownEngine(
                    DrawdownType.DD20
                ),

            DrawdownType.DD25.value:

                lambda: DrawdownEngine(
                    DrawdownType.DD25
                ),

            DrawdownType.DD30.value:

                lambda: DrawdownEngine(
                    DrawdownType.DD30
                ),

        }

    # ---------------------------------------------------------
    # Strategy Execution
    # ---------------------------------------------------------

    def _execute_strategies(
        self,
        trades: list[Trade],
        selected_strategies: list[str],
    ) -> list[StrategyResult]:
        """
        Execute selected strategies.

        Parameters
        ----------
        trades
            Original MT5 trades.

        selected_strategies
            User selected strategies.

        Returns
        -------
        list[StrategyResult]
        """

        results: list[StrategyResult] = []

        for strategy_name in selected_strategies:

            engine = self._create_engine(
                strategy_name
            )

            result = engine.run(
                trades
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

                f"Unknown strategy: {strategy_name}"

            )

        return factory()

    # ---------------------------------------------------------

    def available_strategies(
        self,
    ) -> list[str]:
        """
        Return available strategies.
        """

        return sorted(

            self._engine_factory.keys()

        )

    # ---------------------------------------------------------
    # Portfolio Result
    # ---------------------------------------------------------

    def _complete_result(
        self,
        portfolio_result: PortfolioResult,
        portfolio_inputs: dict[
            str,
            PortfolioInput,
        ],
    ) -> PortfolioResult:
        """
        Complete PortfolioResult.

        Calculates

        • Portfolio trades
        • Monthly statistics
        • Yearly statistics

        Returns
        -------
        PortfolioResult
        """

        #
        # Build portfolio trades.
        #
        portfolio_trades = (
            self._statistics_engine
            ._build_portfolio_trades(
                portfolio_result.strategy_results
            )
        )

        portfolio_result.portfolio_trades = (
            portfolio_trades
        )

        #
        # Monthly statistics.
        #
        monthly = (
            self._statistics_engine
            .calculate_monthly_statistics(
                portfolio_trades,
            )
        )

        self._statistics_engine.complete_monthly_statistics(
            monthly,
            portfolio_result.strategy_results,
            portfolio_inputs,
        )

        portfolio_result.monthly_statistics = (
            monthly
        )

        #
        # Yearly statistics.
        #
        yearly = (
            self._statistics_engine
            .calculate_yearly_statistics(
                portfolio_trades,
            )
        )

        self._statistics_engine.complete_yearly_statistics(
            yearly,
            portfolio_result.strategy_results,
            portfolio_inputs,
        )

        portfolio_result.yearly_statistics = (
            yearly
        )

        #
        # Final validation.
        #
        self._statistics_engine.validate(
            portfolio_result.statistics
        )

        return portfolio_result

    # ---------------------------------------------------------

    def portfolio_summary(
        self,
        portfolio_result: PortfolioResult,
    ):
        """
        Convenience method.

        Returns portfolio statistics.
        """

        return portfolio_result.statistics

    # ---------------------------------------------------------

    def strategy_results(
        self,
        portfolio_result: PortfolioResult,
    ) -> list[StrategyResult]:
        """
        Return individual strategy results.
        """

        return portfolio_result.strategy_results

    # ---------------------------------------------------------

    def portfolio_trades(
        self,
        portfolio_result: PortfolioResult,
    ):
        """
        Return portfolio trades.
        """

        return portfolio_result.portfolio_trades
